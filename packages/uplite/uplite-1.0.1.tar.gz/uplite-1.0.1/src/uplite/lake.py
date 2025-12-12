import os
from pathlib import Path

import boto3
from pyspark.sql import SparkSession

ELYSIA_DB_NAME = "elysia.db"


def auto_register_tables(spark: SparkSession, warehouse_dir: str) -> None:
    """
    Automatically register tables from either S3 or local file system into Spark catalog.

    Args:
        spark: Active SparkSession
        warehouse_dir: Path to the warehouse directory (can be S3 or local path)
    """
    if warehouse_dir.startswith("s3a://"):
        _register_s3_tables(spark, warehouse_dir)
    else:
        _register_local_tables(spark, warehouse_dir)


def _parse_s3_location(warehouse_dir: str) -> tuple[str, str]:
    bucket_name = warehouse_dir[6:].split("/")[0]
    prefix = "/".join(warehouse_dir[6:].split("/")[1:]) + f"/{ELYSIA_DB_NAME}/"
    return bucket_name, prefix


def _register_s3_tables(spark: SparkSession, warehouse_dir: str) -> None:
    s3_client = boto3.client("s3")
    bucket_name, prefix = _parse_s3_location(warehouse_dir)

    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix,
        Delimiter="/",
    )

    catalog = spark.catalog
    for content in response.get("CommonPrefixes", []):
        subdir = content.get("Prefix").split("/")[-2]
        if not catalog.tableExists(subdir):
            catalog.createTable(subdir, f"{warehouse_dir}/{ELYSIA_DB_NAME}/{subdir}")


def _register_local_tables(spark: SparkSession, warehouse_dir: str) -> None:
    local_warehouse_path = Path(warehouse_dir) / ELYSIA_DB_NAME

    if not os.path.exists(local_warehouse_path):
        return

    catalog = spark.catalog
    for subdir in os.listdir(local_warehouse_path):
        subdir_path = os.path.join(local_warehouse_path, subdir)
        if os.path.isdir(subdir_path):
            if not catalog.tableExists(subdir):
                catalog.createTable(subdir, subdir_path)
