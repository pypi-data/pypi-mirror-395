import logging
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Type, TypeVar, cast, get_args, overload

from delta.tables import DeltaTable
from pyspark.errors import IllegalArgumentException
from pyspark.sql import DataFrame, SparkSession, Window
from pyspark.sql.functions import col, current_timestamp, row_number
from pyspark.sql.types import IntegerType, StringType
from typing_extensions import get_original_bases

from uplite.datalang import (
    ColumnSpec,
    TableSpec,
    TTableSpec,
    TypedDataFrame,
    empty_df,
    spark_schema,
    typed,
)


class Checkpoint(TableSpec):
    @classmethod
    def table_description(cls):
        return "Table stores checkpoint for CDC applied in Elysia"

    owner = ColumnSpec(
        data_type=StringType(),
        description="Process which created the checkpoint",
    )

    elysia_table_name = ColumnSpec(
        data_type=StringType(),
        description="Full table name of the table for which checkpoint is stored",
    )

    latest_version = ColumnSpec(
        data_type=IntegerType(),
        description="Latest version of the table",
    )


TPipelineDescriptor = TypeVar("TPipelineDescriptor")


class FlowStep[TPipelineDescriptor]:
    logger = logging.getLogger(__name__)

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._children = {}
        instance._parent = None
        instance._custom_dependencies = []
        return instance

    @property
    def id(self) -> str:
        return self.__class__.__name__

    @property
    def desc(self) -> Type[TPipelineDescriptor]:
        for base in get_original_bases(self.__class__):
            if "FlowStep" in str(base) or "IngestionFlow" in str(base):
                return get_args(base)[0]

        raise ValueError("Descriptor not found")

    @property
    def parent(self) -> "FlowStep | None":
        return self._parent

    @property
    def root(self) -> "FlowStep":
        if self.parent is None:
            return self

        return self.parent.root

    @property
    def children(self) -> dict[Type, "FlowStep"]:
        return self._children

    def register_dependency(self, deps: list["FlowStep"]) -> None:
        self._custom_dependencies.extend(deps)

    @property
    def dependencies(self) -> dict[Type, "FlowStep"]:
        attrib_dependencies = {
            type(value): value
            for attr, value in self.__dict__.items()
            if not attr.startswith("__")
            and attr != "_parent"
            and isinstance(value, FlowStep)
        }

        custom_deps = {type(dep): dep for dep in self._custom_dependencies}
        result = attrib_dependencies | custom_deps
        return result

    def define(self, spark: SparkSession) -> None:
        """
        Define the pipeline base on and :class:`pyspark.sql.session.SparkSession` and :class:`elysia.core.Pipeline` context

        :param spark: spark session from outside context
        :return:
        """

        # disable case sensitivity as it's enabled by default in Databricks
        spark.conf.set("park.sql.caseSensitive", False)

        for child in self.children.values():
            self.logger.info(f"Running {child.id}")
            child.define(spark)
            self.logger.info(f"Completed {child.id}")

    def register_sub_flow(self, *child: "FlowStep") -> None:
        """
        Register a FlowStep instance as a child of this flow - sub-flow
        :param child: FlowStep instance to register
        """
        for c in child:
            c._parent = self
            self.children[type(c)] = c
            c._when_registered_with_parent()

    def standalone(self, sub_flow: Type["FlowStep"]) -> "FlowStep | None":
        """
        Provides standalone instance for any child
        :param sub_flow: subflow type
        :return:
        """
        # check if it's not me
        if isinstance(self, sub_flow) is sub_flow:
            return self

        # check if it's one of my children
        step = self.children.get(sub_flow)

        if step is None:
            for child in self.children.values():
                step = child.standalone(sub_flow)

                if step is not None:
                    return step

        return step

    def _when_registered_with_parent(self) -> None:
        """
        Custom logic to be executed when the flow step is registered with a parent flow step
        """
        pass


DELTA_LAKE_START_VERSION = 1

override_params: dict[str, Any] = {}

# This is a workaround for https://github.com/delta-io/delta/issues/2434
LOCAL_MODE = True


@dataclass
class CheckpointedDataFrameContext:
    owner: str
    latest_version: int
    ops: "JobOps"


class CheckpointedDataFrame[TTableSpec](TypedDataFrame[TTableSpec]):
    def __init__(
        self,
        df: DataFrame,
        spec: Type[TTableSpec],
        context: CheckpointedDataFrameContext = None,
    ):
        super().__init__(df, spec)
        self._context = context

    def __enter__(self) -> "CheckpointedDataFrame[TTableSpec]":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._context is None:
            return  # don't do anything if there is no context; it means the dataframe doesn't need to be checkpointed

        if exc_type is not None or exc_val is not None or exc_tb is not None:
            # an exception occurred, don't checkpoint
            return

        # update checkpoint with the latest version instead
        self._context.ops.update_checkpoint(
            self._df.sparkSession,
            self._context.owner,
            self.spec.alias(),
            self._context.latest_version,
        )


class JobOps:
    def __init__(self, step: "FlowStep"):
        self.step = step

    def get_param(self, name: str) -> Any:
        if (param := override_params.get(name)) is not None:
            return param

        raise ValueError(f"Parameter {name} is not set")

    def get_catalog(self):
        return self.get_param("catalog")

    def get_database(self):
        return self.get_param("schema")

    def resolve_table(self, table_name: str) -> str:
        target_catalog = self.get_catalog()
        target_schema = self.get_database()

        return (
            f"`{target_schema}`.`{table_name}`"
            if LOCAL_MODE
            else f"`{target_catalog}`.`{target_schema}`.`{table_name}`"
        )

    @overload
    def full_table_name(self, df: TypedDataFrame[TTableSpec]) -> str: ...

    @overload
    def full_table_name(self, spec: Type[TTableSpec]) -> str: ...

    def full_table_name(
        self, spec_entry: TypedDataFrame[TTableSpec] | Type[TTableSpec]
    ) -> str:
        spec = None
        if isinstance(spec_entry, TypedDataFrame):
            spec = spec_entry.spec
        elif isinstance(spec_entry, type):
            spec = cast(Type[TableSpec], spec_entry)

        return self.resolve_table(spec.alias())

    def read_or_empty(
        self, spark: SparkSession, table: Type[TTableSpec]
    ) -> TypedDataFrame[TTableSpec]:
        if spark.catalog.tableExists(self.full_table_name(table)):
            return self.read(spark, table)

        return empty_df(spark, table)

    def read(
        self,
        spark: SparkSession,
        table: Type[TTableSpec],
        prefix: str = None,
    ) -> TypedDataFrame[TTableSpec]:
        prefix = prefix or ""
        target_table_name = f"{prefix}{self.full_table_name(table)}"
        return TypedDataFrame(spark.read.table(target_table_name), table)

    def read_since_latest_checkpoint(
        self, spark: SparkSession, table: Type[TTableSpec], owner: str = None
    ) -> CheckpointedDataFrame[TTableSpec]:
        owner = owner or self.step.id

        latest_version = self.get_latest_checkpoint_version(
            spark, owner, table_name=table.alias()
        )

        full_table_name = self.full_table_name(table)

        try:
            changes_df = (
                spark.read.format("delta")
                .option("readChangeFeed", "true")
                .option("startingVersion", latest_version)
                .table(f"{full_table_name}")
                .filter(col("_change_type").isin("insert", "update_postimage"))
                .select(*table.fields_names())
            )
        except IllegalArgumentException:
            # this means we that there are no new changes in the source table. we need to return an empty dataframe
            empty_df = spark.createDataFrame([], spark_schema(table))
            return CheckpointedDataFrame(empty_df, table)

        return CheckpointedDataFrame(
            changes_df,
            table,
            CheckpointedDataFrameContext(owner, latest_version + 1, self),
        )

    def read_as_delta(self, spark: SparkSession, table: Type[TTableSpec]) -> DeltaTable:
        return DeltaTable.forName(spark, self.full_table_name(table))

    def write(
        self,
        df: TypedDataFrame[TTableSpec],
        mode: str = None,
        overwrite_schema=True,
        merge_schema=True,
        prefix: str = None,
    ) -> None:
        """
        Write the dataframe to the target table in the catalog with the specified mode and schema overwrite option.
        Enforces the partitioning and schema according to the table spec.
        :param df: input dataframe
        :param mode: write mode
        :param overwrite_schema: overwrite schema option
        :param merge_schema: merge schema option
        :param prefix: prefix to add to the table name
        """

        df.verify_schema()
        self.create_table_if_not_exists(df)

        prefix = prefix or ""
        target_table_name = f"{prefix}{self.full_table_name(df)}"

        (
            df.write.mode(mode)
            .option("mergeSchema", str(merge_schema).lower())
            .option("overwriteSchema", str(overwrite_schema).lower())
            # .option("parquet.block.size", 134217728)  # 128MB
            .partitionBy(df.spec.partition_columns())
            .saveAsTable(target_table_name)
        )

    def merge(
        self,
        df: TypedDataFrame[TTableSpec],
        matching_columns: list[ColumnSpec],
        order_by: list[ColumnSpec] = None,
        except_columns: list[ColumnSpec] = None,
        ascending: bool = True,
    ) -> None:
        """
        Merge the input dataframe with the target table in the catalog using the specified matching columns.
        :param df: input dataframe
        :param matching_columns: list of columns to match on for the merge operation
        :param order_by: list of columns to order the records in case of duplicates in the input dataframe
        :param except_columns: list of columns to exclude from the merge operation to the target table
        :param ascending: determines the order of the records in case of duplicates in the input dataframe
        :return:
        """
        if df.limit(1).count() == 0:
            print(
                f"Source DataFrame {df.spec.alias()} is empty. Skipping merge operation."
            )
            return None

        except_columns = except_columns or []
        order_by = order_by or matching_columns

        df.verify_schema()
        self.create_table_if_not_exists(df)

        def deduplicate() -> TypedDataFrame[TTableSpec]:
            window_spec = Window.partitionBy([c.col for c in matching_columns]).orderBy(
                [c.col.asc() if ascending else c.col.desc() for c in order_by]
            )

            deduplicated_df = (
                df.withColumn("rank", row_number().over(window_spec))
                .filter(col("rank") == 1)
                .drop("rank")
            )

            # some columns used for ordering may not be present in the target table, so they need to be dropped
            deduplicated_df = deduplicated_df.drop(*[c.name for c in except_columns])

            return typed(deduplicated_df, df.spec)

        deduplicate_source = deduplicate()

        matching_condition = " AND ".join(
            f"target.{c.name} = source.{c.name}" for c in matching_columns
        )
        print(f"Matching condition: {matching_condition}")

        update_condition = " OR ".join(
            f"target.{c} != source.{c}"
            for c in (
                set(df.spec.fields_names()) - set([c.name for c in matching_columns])
            )
        )

        # if there are no columns to update, set update_condition to None or error will be thrown
        if not update_condition:
            update_condition = None

        print(f"Update condition: {update_condition}")

        (
            self.read_as_delta(df.sparkSession, df.spec)
            .alias("target")
            .merge(
                source=deduplicate_source.alias("source"),
                condition=matching_condition,
            )
            .whenMatchedUpdateAll(condition=update_condition)
            .whenNotMatchedInsertAll()
            .execute()
        )

    def create_table_if_not_exists(
        self, df: TypedDataFrame[TTableSpec], enable_cdc: bool = False
    ) -> DeltaTable:
        return self.create_table_if_not_exists_from_spec(
            df.sparkSession,
            df.spec,
            enable_cdc,
        )

    def create_table_if_not_exists_from_spec(
        self, spark: SparkSession, spec: Type[TableSpec], enable_cdc: bool = False
    ) -> DeltaTable:
        full_table_name = self.resolve_table(spec.alias())
        enable_cdc = spec._enable_cdc or enable_cdc

        builder = (
            DeltaTable.createIfNotExists(spark)
            .tableName(full_table_name)
            .partitionedBy(*spec.partition_columns())
            .property("delta.enableChangeDataFeed", str(enable_cdc).lower())
        )

        for field in spec.fields():
            builder = builder.addColumn(field.name, field.data_type)

        return builder.execute()

    def get_latest_checkpoint_version(
        self, spark: SparkSession, owner: str, table_name: str
    ) -> int:
        self.create_table_if_not_exists_from_spec(spark, Checkpoint, enable_cdc=False)

        latest_versions = (
            self.read(spark, Checkpoint)
            .filter(
                (Checkpoint.elysia_table_name.col_ == table_name)
                & (Checkpoint.owner.col_ == owner)
            )
            .select(Checkpoint.latest_version.name)
            .collect()
        )

        return latest_versions[0][0] if latest_versions else DELTA_LAKE_START_VERSION

    def update_checkpoint(
        self, spark: SparkSession, owner: str, table_name: str, latest_version: int
    ) -> None:
        self.create_table_if_not_exists_from_spec(spark, Checkpoint, enable_cdc=False)

        checkpoint_row_to_upsert = spark.createDataFrame(
            [(owner, table_name, latest_version)],
            spark_schema(Checkpoint),
        )

        self.read_as_delta(spark, Checkpoint).alias("target").merge(
            checkpoint_row_to_upsert.alias("source"),
            f"""
            target.{Checkpoint.owner.name} = source.{Checkpoint.owner.name} and
            target.{Checkpoint.elysia_table_name.name} = source.{Checkpoint.elysia_table_name.name}
            """,
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

    def merge_with_scd4(
        self,
        df: TypedDataFrame[TTableSpec],
        matching_columns: list[ColumnSpec],
        order_by: list[ColumnSpec] = None,
        except_columns: list[ColumnSpec] = None,
        ascending: bool = True,
        overwrite_schema=True,
        merge_schema=True,
    ) -> None:
        """
        Merge the input dataframe with the target table in the catalog using the specified matching columns.
        :param df: input dataframe
        :param matching_columns: the columns to match on for the merge operation
        :param order_by: the columns to order the records in case of duplicates in the input dataframe
        :param except_columns: list of columns to exclude from the merge operation to the target table
        :param ascending: determines the order of the records in case of duplicates in the input dataframe
        :param overwrite_schema: overwrite schema option in the target table
        :param merge_schema: merge schema option in the target table
        :return:
        """
        merge_owner_name = "merge_scd4"
        spark = df.sparkSession
        table = df.spec
        target_table_name = table.alias()

        self.create_table_if_not_exists(df, enable_cdc=True)

        # Perform the merge to update and insert records in the target table
        self.merge(df, matching_columns, order_by, except_columns, ascending)

        # Fetch changes from the CDF table of the target table, including the previous MERGE
        with self.read_since_latest_checkpoint(
            spark, table, merge_owner_name
        ) as changes_since_last_merge:
            history_changes_to_append = changes_since_last_merge.withColumn(
                "update_timestamp", current_timestamp()
            ).select(*(table.fields_names() + ["update_timestamp"]))

            # Append changes to the historical table
            full_history_table_name = self.resolve_table(f"{target_table_name}_history")
            (
                history_changes_to_append.write.mode("append")
                .option("overwriteSchema", str(overwrite_schema).lower())
                .option("mergeSchema", str(merge_schema).lower())
                .saveAsTable(
                    full_history_table_name,
                    partitionBy=table.partition_columns(),
                )
            )

    def truncate_table(self, spark: SparkSession, table_spec: Type[TableSpec]) -> None:
        spark.sql(f"TRUNCATE TABLE {self.full_table_name(table_spec)};")


class JobFlowMixin:
    """
    Mixin that provides data operations specific for Databricks pyspark job

    Example:
        class MyFlowStep(FlowStep[MyFlowStepResult], JobFlowMixin):
            def define(self, spark: SparkSession):
                df = self.data.read(spark, raw.Demographics)
                ...
    """

    @property
    def data(self) -> JobOps:
        return JobOps(self)


class WorkflowOps:
    def if_else(self) -> FlowStep: ...


class WorkflowMixin:
    """
    Mixin that provides operations specific for Databricks Workflow

    Example:
        class MyFlowStep(FlowStep[MyFlowStepResult], WorkflowMixin):
            def define(self, spark: SparkSession):
                next_step = self.data.if_else(...)
                ...
    """

    @property
    def data(self) -> WorkflowOps:
        return WorkflowOps()


class SubFlowMixin:
    def register_sub_flow(self, *child: "FlowStep") -> None:
        """
        Delegate child registration to the parent as SubFlow indicates that no job or workflow in dbx is created
        :param child: FlowStep instance to register
        """
        if not self.parent:
            return

        self.parent.register_sub_flow(*child)

        for c in child:
            self.children[type(c)] = c

    def _when_registered_with_parent(self) -> None:
        self.register_children()

    def register_children(self) -> None:
        pass
