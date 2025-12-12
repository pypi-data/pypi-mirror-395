uplite — typed data workflows on Spark + Delta Lake

### Overview
uplite helps you build small, testable PySpark jobs with a strongly-typed feel:

- Describe datasets with `TableSpec` and `ColumnSpec` (names, types, partitions, docs)
- Get typed `DataFrame` helpers (`TypedDataFrame`) with safe joins and schema verification
- Define jobs as `FlowStep`s, compose them into simple workflows
- Read/write/merge Delta tables through a compact API (`JobOps`)
- Work locally or in a metastore/catalog environment

The examples below are distilled from the tests and public API in this repo.

### Installation

```bash
pip install uplite
```

Requirements (pulled as dependencies): `pyspark>=3.5.0,<=3.5.5`, `delta-spark>=3.3.0`, `boto3`.

Python 3.12+ is recommended (see `pyproject.toml`).

### Quickstart (local Delta catalog)

1) Start a Spark session configured for Delta:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName("uplite-quickstart")
    .master("local[2]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.defaultTableFormat", "delta")
    .config("spark.sql.sources.default", "delta")
    # optional: set a local warehouse folder
    .config("spark.sql.warehouse.dir", "/tmp/local-delta-warehouse")
    .getOrCreate()
)

spark.sql("CREATE SCHEMA IF NOT EXISTS uplite;")
spark.sql("USE uplite;")
```

2) Tell uplite you are in local mode and provide catalog/schema parameters used to resolve table names:

```python
import uplite.flow as flow

flow.LOCAL_MODE = True  # local mode uses `<schema>.<table>` instead of `<catalog>.<schema>.<table>`
flow.override_params = {
    "catalog": "local",   # can be any string in local mode
    "schema": "uplite",   # matches the schema you `USE`d above
}
```

3) (Optional) Auto-register existing Delta tables from a warehouse folder (local or S3). For local, layout is `<WAREHOUSE>/uplite.db/<table>`:

```python
from uplite.lake import auto_register_tables

auto_register_tables(spark, "/tmp/local-delta-warehouse")
```

For S3, point to an S3A prefix that contains `uplite.db`: `auto_register_tables(spark, "s3a://my-bucket/path/to/warehouse")`.

### Define a schema with TableSpec

Use `TableSpec` and `ColumnSpec` to describe a Delta table. You can use Spark data types or simple strings.

```python
from pyspark.sql.types import IntegerType, StringType, DoubleType
from uplite.datalang import TableSpec, ColumnSpec

class Promotion(TableSpec):
    promotion_id = ColumnSpec(IntegerType(), description="promotion id")
    target_type = ColumnSpec(StringType(), description="target type")
    target_value = ColumnSpec(StringType(), description="target value")
    promotion_type = ColumnSpec(StringType(), description="promotion type")
    discount_percentage = ColumnSpec(DoubleType(), description="discount percentage")

# Useful introspection helpers
Promotion.table_name()   # "promotion"
Promotion.table_zone()   # derived from package name (e.g. "raw" / "processed")
Promotion.table_id()     # "<zone>.<name>", e.g. "raw.promotion"
Promotion.alias()        # used in SQL as a stable table alias
```

### Convert raw DataFrames to typed DataFrames

`conform_to_spec(df, TableSpec)` casts/aligns columns and returns a `TypedDataFrame` bound to your spec.

```python
from uplite.datalang import conform_to_spec

raw_promos = spark.read.csv("sample_data", header=True)
t_promos = conform_to_spec(raw_promos, Promotion)

# Validate schema before writes/joins
t_promos.verify_schema()
```

### Write, read, merge — job building blocks

Use `FlowStep` + `JobFlowMixin` to implement a job. Interact with the catalog via `self.data` (a `JobOps`).

```python
from uplite.flow import FlowStep, JobFlowMixin, WorkflowMixin
from pyspark.sql import SparkSession

class ImportPromotions(JobFlowMixin, FlowStep[None]):
    def define(self, spark: SparkSession) -> None:
        # Read from a raw source
        raw_promos = spark.read.csv("sample_data", header=True)

        # Enforce expected schema and get a TypedDataFrame
        t_promos = conform_to_spec(raw_promos, Promotion)

        # Create/overwrite the Delta table based on the spec
        self.data.write(t_promos, mode="overwrite")

        # Read back as a typed DataFrame
        self.data.read(spark, Promotion).show()

class PromotionWorkflow(WorkflowMixin, FlowStep[None]):
    def __init__(self):
        self.register_sub_flow(ImportPromotions())

# Run it
job = PromotionWorkflow()
job.define(spark)
```

Merging with deduplication (SCD4 helper available):

```python
# Upsert with deduplication based on matching columns
self.data.merge(
    t_promos,
    matching_columns=[Promotion.promotion_id],
    # order_by defaults to matching_columns, but you can specify custom ordering columns
)

# Or perform SCD4-like merge and automatically append change history
self.data.merge_with_scd4(
    t_promos,
    matching_columns=[Promotion.promotion_id],
)
```

### Change Data Feed checkpoints

Consume only new changes from a Delta table using CDF and automatic checkpoints:

```python
with self.data.read_since_latest_checkpoint(spark, Promotion) as changes:
    # process incremental changes ("insert", "update_postimage")
    changes.show()
    # when the context manager exits successfully, the checkpoint is advanced
```

### Typed joins

`TypedDataFrame.eq_join` verifies join keys exist on both specs and returns a typed result:

```python
left = self.data.read(spark, Promotion)
right = self.data.read(spark, Promotion)  # example only

joined = left.eq_join(right, left_on=Promotion.promotion_id, right_on=Promotion.promotion_id)
joined.show()
```

### Registering existing tables into Spark catalog

`uplite.lake.auto_register_tables(spark, warehouse_dir)` discovers Delta tables and creates catalog entries:

- Local directory: expects `<warehouse_dir>/uplite.db/<table>` layout
- S3: pass an `s3a://bucket/prefix` and it will look under `<prefix>/uplite.db/`

```python
from uplite.lake import auto_register_tables

auto_register_tables(spark, "/tmp/local-delta-warehouse")
# or
auto_register_tables(spark, "s3a://my-bucket/path/to/warehouse")
```

### Parameter resolution and table names

`JobOps` builds full table names from module-level parameters in `uplite.flow`:

- `override_params["catalog"]` and `override_params["schema"]`
- `LOCAL_MODE = True` → resolves to ``<schema>`.`<table>``
- `LOCAL_MODE = False` → resolves to ``<catalog>`.`<schema>`.`<table>``

Set them once at startup:

```python
import uplite.flow as flow

flow.LOCAL_MODE = True
flow.override_params = {"catalog": "prod", "schema": "uplite"}
```

### Tips and gotchas

- Always call `conform_to_spec` before writing/merging to enforce schema.
- `TypedDataFrame.verify_schema()` is used internally by writers/mergers but can be called explicitly.
- For local development, create and `USE` the schema in Spark (e.g., `uplite`) and set `LOCAL_MODE = True`.
- If using S3, configure Hadoop AWS/S3A and credentials; `boto3` is used for discovery in `auto_register_tables`.

### Minimal end-to-end example

```python
from pyspark.sql import SparkSession
import uplite.flow as flow
from uplite.datalang import TableSpec, ColumnSpec, conform_to_spec
from uplite.flow import FlowStep, JobFlowMixin, WorkflowMixin
from pyspark.sql.types import IntegerType, StringType

packages = [
    "io.delta:delta-spark_2.12:3.1.0",
    "org.apache.hadoop:hadoop-aws:3.3.1",
]

spark = (
    SparkSession.builder.appName("uplite-example")
    .master("local[2]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .config("spark.sql.defaultTableFormat", "delta")
    .config("spark.sql.sources.default", "delta")
    .config("spark.jars.packages", ",".join(packages))
    .config("spark.sql.warehouse.dir", "data")
    .getOrCreate()
)

spark.sql("CREATE SCHEMA IF NOT EXISTS uplite;")
spark.sql("USE uplite;")

flow.LOCAL_MODE = True
flow.override_params = {"catalog": "local", "schema": "uplite"}

class Promotion(TableSpec):
    promotion_id = ColumnSpec(IntegerType())
    promotion_type = ColumnSpec(StringType())

class Import(JobFlowMixin, FlowStep[None]):
    def define(self, spark: SparkSession) -> None:
        raw_df = spark.createDataFrame([
            {"promotion_id": 1, "promotion_type": "discount"},
            {"promotion_id": 2, "promotion_type": "bundle"},
        ])
        t_df = conform_to_spec(raw_df, Promotion)
        self.data.write(t_df, mode="overwrite")
        self.data.read(spark, Promotion).show()

class Workflow(WorkflowMixin, FlowStep[None]):
    def __init__(self):
        self.register_sub_flow(Import())

Workflow().define(spark)
```

---

If you run into anything that feels rough or is missing, please open an issue with a short snippet — most features here are driven by real-world tests and use-cases.
