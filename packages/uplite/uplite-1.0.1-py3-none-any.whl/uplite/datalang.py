import re
from dataclasses import dataclass, field
from typing import Any, Type, TypeVar, cast, get_args

from pyspark import StorageLevel
from pyspark.sql import Column, DataFrame, SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import (
    DataType,
    DateType,
    DoubleType,
    FloatType,
    IntegerType,
    LongType,
    StringType,
    StructField,
    StructType,
)


TColumnSpecCustomAttrib = TypeVar("TColumnSpecCustomAttrib")


@dataclass(eq=False)
class ColumnSpec:
    data_type: str | DataType
    description: str = ""
    is_partition: bool = False
    custom_attributes: list[Any] = field(default_factory=list)

    _name: str = field(init=False)
    table: type["TableSpec"] = field(init=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ColumnSpec({self.name})"

    def __eq__(self, other):
        if isinstance(other, ColumnSpec):
            # Equal if table and name match
            return (self.table is other.table) and (self.name == other.name)
        elif isinstance(other, str):
            # Equal if string matches our name
            return self.name == other
        else:
            return NotImplemented

    def __hash__(self):
        # Hash using table and name to safely use as a key
        return hash(self.name)

    @property
    def name(self) -> str:
        return self._name

    def __set_name__(self, owner, name):
        if hasattr(self, "_name") or hasattr(self, "table"):
            raise AttributeError(
                f"""
                ColumnSpec attributes are not meant to be reused across different classes.
                It's already used by {self.table.__name__}.{self._name}
                You're trying to use it again in {owner.__name__}.{name}
                """
            )

        self._name = name
        self.table = owner

        if owner.__bases__:  # If the class has at least one parent
            if isinstance(owner.__bases__[0], TableSpec):
                self.table = owner.__bases__[0]  # Direct parent

    def custom(self, t: Type[TColumnSpecCustomAttrib]) -> list[TColumnSpecCustomAttrib]:
        return [ca for ca in self.custom_attributes if type(ca) is t]

    def attr(self, t: Type[TColumnSpecCustomAttrib]) -> TColumnSpecCustomAttrib:
        if len(self.custom(t)) > 0:
            return self.custom(t)[0]

        raise AttributeError(f"Custom Attribute {t} not found in {self.name}")

    @property
    def alias(self) -> str:
        return f"{self.table.alias()}.{self._name}"

    @property
    def col_alias(self) -> Column:
        return col(self.alias)

    @property
    def col(self) -> Column:
        return col(self.name)

    @property
    def col_(self) -> Column:
        return col(self.name)


class MetaTableSpec(type):
    def __contains__(cls, x: str):
        dataset = cast(TableSpec, cls)
        return any(map(lambda f: f.name == x, dataset.fields()))

    def __iter__(cls):
        dataset = cast(TableSpec, cls)
        yield from dataset.fields()

    def __getitem__(cls, item: str) -> ColumnSpec:
        dataset = cast(TableSpec, cls)
        potential_columns = [f for f in dataset.fields() if f.name == item]

        if len(potential_columns) > 1:
            raise AttributeError(
                f"Multiple fields with the same name {item} in dataset {dataset.table_id()}"
            )

        if len(potential_columns) == 1:
            return potential_columns[0]

        raise AttributeError(
            f"Cannot find field {item} in dataset {dataset.table_id()}"
        )

    def __getattribute__(self, item: str):
        attrib = super().__getattribute__(item)

        # Override ColumnSpec associated table to support derived Table Specs
        if isinstance(attrib, ColumnSpec):
            attrib.table = self

        return attrib


class TableSpec(metaclass=MetaTableSpec):
    _enable_cdc: bool = False
    _table_description: str = ""

    @classmethod
    def fields(cls) -> list[ColumnSpec]:
        field_list = []
        for base_class in cls.__mro__:
            if base_class is object:  # Add any other base class you wish to exclude
                continue

            field_list.extend(
                [v for k, v in base_class.__dict__.items() if isinstance(v, ColumnSpec)]
            )

        return field_list

    @classmethod
    def fields_names(cls) -> list[str]:
        return [f.name for f in cls.fields()]

    @classmethod
    def partition_columns(cls) -> list[str]:
        return [f.name for f in cls.fields() if f.is_partition]

    @classmethod
    def non_partition_columns(cls) -> list[ColumnSpec]:
        return [f for f in cls.fields() if not f.is_partition]

    @classmethod
    def table_name(cls) -> str:
        camel_case_name = cls.__name__
        # covert from CamelCase to snake_case
        return re.sub("([A-Z0-9])", r"_\1", camel_case_name).lower().lstrip("_")

    @classmethod
    def table_description(cls):
        return cls._table_description

    @classmethod
    def alias_df(cls, df: DataFrame) -> DataFrame:
        return df.alias(cls.alias())

    @classmethod
    def alias(cls) -> str:
        return f"{cls.table_zone()}_{cls.table_name()}"

    @classmethod
    def table_zone(cls) -> str:
        packages = cls.__module__.split(".")
        return packages[
            -min(len(packages), 2)
        ]  # previous to last or the first one if only one package

    @classmethod
    def table_id(cls) -> str:
        return f"{cls.table_zone()}.{cls.table_name()}"


TTableSpec = TypeVar("TTableSpec", bound=TableSpec)
TTableSpecOther = TypeVar("TTableSpecOther", bound=TableSpec)
TJoinedTableSpec = TTableSpec | TTableSpecOther


class TypedDataFrame[TTableSpec](DataFrame):
    def __init__(self, df: DataFrame, spec: Type[TTableSpec] = None):
        self._df = df
        self._spec = spec

    def eq_join(
        self,
        other: "TypedDataFrame[TTableSpecOther]",
        left_on: ColumnSpec,
        right_on: ColumnSpec,
        how="left",
    ) -> "JoinedDataFrame[TJoinedTableSpec]":
        """
        Joins two TypedDataFrames based on specified columns equality.

        :param other: The other TypedDataFrame to join with.
        :param left_on: The column specification in the current DataFrame to join on.
        :param right_on: The column specification in the other DataFrame to join on.
        :param how: The type of join operation to perform. Defaults to "left".
        :return: A new TypedDataFrame that is the result of the join operation.
        """
        # Validate inputs
        failed_validations = []

        if left_on not in self.spec.fields():
            failed_validations.append(
                f"Left column {left_on.name} not found in current {self.spec.__name__}"
            )

        if right_on not in other.spec.fields():
            failed_validations.append(
                f"Right column {right_on.name} not found in other {other.spec.__name__}"
            )

        if failed_validations:
            raise ValueError(". ".join(failed_validations))

        # join dataframes and drop right on column
        joined = self.alias_df.join(
            how=how,
            other=other.alias_df,
            on=left_on.col_alias.__eq__(right_on.col_alias),
        )

        return JoinedDataFrame(joined, left_spec=self.spec, right_spec=other.spec)

    def filter(self, condition: Column | str) -> "TypedDataFrame[TTableSpec]":
        return typed(self._df.filter(condition), self.spec)

    def union(
        self, other: "TypedDataFrame[TTableSpec]"
    ) -> "TypedDataFrame[TTableSpec]":
        return typed(self._df.union(other._df), self.spec)

    def dropDuplicates(
        self, subset: list[str] | None = None
    ) -> "TypedDataFrame[TTableSpec]":
        return typed(self._df.dropDuplicates(subset), self.spec)

    def cache(self) -> "TypedDataFrame[TTableSpec]":
        return typed(self._df.cache(), self.spec)

    def persist(
        self,
        storageLevel: StorageLevel = StorageLevel.MEMORY_AND_DISK_DESER,
    ) -> "TypedDataFrame[TTableSpec]":
        return typed(self._df.persist(storageLevel), self.spec)

    def verify_schema(self):
        # additional_columns = set(self._df.columns) - set(self.spec.fields_names())
        # if len(additional_columns) > 0:
        #     raise ValueError("DataFrame has more fields than schema")

        missing_fields = [
            f"{schema_field.name} is missing from DataFrame"
            for schema_field in self.spec.fields()
            if schema_field.name not in self._df.columns
        ]
        if missing_fields:
            missing_msg = str.join("\n", missing_fields)
            raise ValueError(
                f"DataFrame is missing fields from schema {self.spec.alias()}:\n{missing_msg}"
            )

        mismatched_types = [
            f"{schema_field.name} has type {self._df.schema[schema_field.name].dataType} instead of {schema_field.data_type}"
            for schema_field in self.spec.fields()
            if self._df.schema[schema_field.name].dataType != schema_field.data_type
        ]
        if mismatched_types:
            mismatch_msg = str.join("\n", mismatched_types)
            raise ValueError(
                f"DataFrame has incorrect data types from schema {self.spec.alias()}:\n{mismatch_msg}"
            )

    def __getattribute__(self, item):
        if (
            item
            in [
                "_df",
                "_spec",
                "_context",  # <- this is super hacky: it's acknowledges the method in the CheckpointedDataFrame
                "original_df",
                "alias_df",
                "verify_schema",
                "filter",
                "union",
                "cache",
                "persist",
                "eq_join",
                "__getattribute__",
                "__orig_class__",
            ]
        ):
            return object.__getattribute__(self, item)

        if item == "spec":
            return self._spec or get_args(self.__orig_class__)[0]

        # For all other attributes, delegate to the _df object
        return object.__getattribute__(self._df, item)

    @property
    def spec(self) -> Type[TTableSpec]:
        return self._spec

    @property
    def original_df(self) -> DataFrame:
        return self._df

    @property
    def alias_df(self) -> "TypedDataFrame[TTableSpec]":
        return typed(self.spec.alias_df(self._df), self.spec)


UnionTableSpec = Type[TTableSpec] | Type[TTableSpecOther]


class JoinedDataFrame[TTableSpec](TypedDataFrame[TTableSpec]):
    def __init__(
        self,
        df: DataFrame,
        left_spec: Type[TTableSpec],
        right_spec: Type[TTableSpecOther],
    ):
        # Dynamically create a new TableSpec subclass combining fields from self._spec and other._spec
        joined_spec = cast(
            Type[TJoinedTableSpec],
            type(
                f"{left_spec.__name__}Joined{right_spec.__name__}",
                (left_spec, right_spec, TableSpec),
                {},
            ),
        )

        super().__init__(df, left_spec)
        self._left_spec = left_spec
        self._right_spec = right_spec

    @property
    def left_spec(self) -> Type[TTableSpec]:
        return self._left_spec

    @property
    def right_spec(self) -> Type[TTableSpecOther]:
        return self._right_spec

    @property
    def spec(self) -> UnionTableSpec:
        return super().spec


def typed(df: DataFrame, spec: Type[TTableSpec]) -> TypedDataFrame[TTableSpec]:
    """
    The typed function is a utility function that is used to create a TypedDataFrame object which enforces the schema defined by spec on the DataFrame.
    It adds additional methods and properties to the DataFrame, such as filter, where, union, and verify_schema.
    The TypedDataFrame class uses Python's type hinting and generics features to enforce the schema at the type level.
    This means that you can use static type checkers to catch schema mismatches at compile time, rather than at runtime.

    :param df: This is the DataFrame that you want to convert into a TypedDataFrame.
    :param spec: This is the type specification for the DataFrame. It is used to enforce a specific schema on the DataFrame.
    :return: The function returns a TypedDataFrame object that wraps the original DataFrame.
    """
    return TypedDataFrame(df, spec)


def fill_missing_columns_with_empty_values_without_column_removal(
    df: DataFrame, spec: Type[TTableSpec]
) -> DataFrame:
    """
    All the columns from table specification that are missing from the data frame are added populated with empty values.
    The existing columns that are not in the table specification are NOT removed from the data frame.

    :param df: the DataFrame to fill missing columns with empty values
    :param spec: the table specification that defines the expected columns and their data types
    :return: the DataFrame with missing columns filled with empty values

    """
    missing_columns = set(spec.fields_names()) - set(df.columns)
    for column in missing_columns:
        df = df.withColumn(column, lit(None).cast(spec[column].data_type))

    return df


def fill_missing_columns_with_empty_values(
    df: DataFrame, spec: Type[TTableSpec]
) -> TypedDataFrame[TTableSpec]:
    """
    The fill_missing_columns_with_empty_values function is a utility function that is used to fill missing columns in a DataFrame with empty values.
    It takes a DataFrame and a type specification as input, and returns a TypedDataFrame object that enforces the schema defined by the type specification.
    If a column is missing in the DataFrame but is present in the type specification, the function adds the missing column to the DataFrame and fills it with empty values.

    :param df: This is the DataFrame that you want to fill missing columns in.
    :param spec: This is the type specification for the DataFrame. It is used to enforce a specific schema on the DataFrame.
    :return: The function returns a TypedDataFrame object that wraps the original DataFrame with missing columns filled with empty values.
    """

    # First add missing columns
    df = fill_missing_columns_with_empty_values_without_column_removal(df, spec)

    # Remove the excess columns
    return typed(df.select(*spec.fields_names()), spec)


def auto_cast(df: DataFrame, spec: Type[TTableSpec]) -> TypedDataFrame[TTableSpec]:
    """
    The auto_cast_columns function is a utility function that is used to automatically cast columns in a DataFrame to the correct data type.
    It takes a DataFrame and a type specification as input, and returns a TypedDataFrame object that enforces the schema defined by the type specification.
    The function iterates over the columns in the DataFrame and casts them to the correct data type based on the type specification.

    :param df: This is the DataFrame that you want to automatically cast columns in.
    :param spec: This is the type specification for the DataFrame. It is used to enforce a specific schema on the DataFrame.
    :return: The function returns a TypedDataFrame object that wraps the original DataFrame with columns automatically cast to the correct data type.
    """
    for f in spec.fields():
        if f.name in df.columns:
            df = df.withColumn(f.name, col(f.name).cast(f.data_type))

    return typed(df, spec)


def conform_to_spec(
    df: DataFrame, spec: Type[TTableSpec]
) -> TypedDataFrame[TTableSpec]:
    """
    The conform_to_spec function is a utility function that is used to conform a DataFrame to a type specification.
    It takes a DataFrame and a type specification as input, and returns a TypedDataFrame object that enforces the schema defined by the type specification.
    The function first fills missing columns in the DataFrame with empty values, and then automatically casts columns to the correct data type based on the type specification.
    Then selects only the columns that are present in the type specification.

    :param df: This is the DataFrame that you want to conform to the type specification.
    :param spec: This is the type specification for the DataFrame. It is used to enforce a specific schema on the DataFrame.
    :return: The function returns a TypedDataFrame object that wraps the original DataFrame conformed to the type specification.
    """
    conformed = auto_cast(
        fill_missing_columns_with_empty_values(df, spec),
        spec,
    ).select(*spec.fields_names())

    return typed(conformed, spec)


def spark_schema_from_columns(*cols: ColumnSpec) -> StructType:
    """
    The spark_schema function is a utility function that is used to convert a list of ColumnSpec objects into a PySpark StructType schema.
    It takes a variable number of ColumnSpec objects as input, and returns a PySpark StructType schema that represents the columns defined by the ColumnSpec objects.

    :param cols: This is a variable number of ColumnSpec objects that define the columns in the schema.
    :return: The function returns a PySpark StructType schema that represents the columns defined by the ColumnSpec objects.
    """
    _type_to_pyspark_map = {
        "string": StringType(),
        "date": DateType(),
        "int": IntegerType(),
        "bigint": LongType(),
        "float": FloatType(),
        "double": DoubleType(),
        "timestamp": StringType(),
    }

    return StructType(
        [
            StructField(
                name=column.name,
                dataType=(
                    column.data_type
                    if isinstance(column.data_type, DataType)
                    else _type_to_pyspark_map[column.data_type]
                ),
                nullable=True,
            )
            for column in cols
        ]
    )


def spark_schema(spec: Type[TableSpec]) -> StructType:
    """
    The spark_schema function is a utility function that is used to convert a TableSpec object into a PySpark StructType schema.
    It takes a TableSpec object as input, and returns a PySpark StructType schema that represents the columns defined by the TableSpec object.

    :param spec: This is the TableSpec object that defines the columns in the schema.
    :return: The function returns a PySpark StructType schema that represents the columns defined by the TableSpec object.
    """
    return spark_schema_from_columns(*spec.fields())


def empty_df(spark: SparkSession, spec: Type[TTableSpec]) -> TypedDataFrame[TTableSpec]:
    """
    The empty_df function is a utility function that is used to create an empty DataFrame that conforms to a type specification.

    :param spark: This is the SparkSession object that is used to create the DataFrame.
    :param spec: This is the type specification for the DataFrame. It is used to enforce a specific schema on the DataFrame.
    """
    return typed(spark.createDataFrame([], spark_schema(spec)), spec)
