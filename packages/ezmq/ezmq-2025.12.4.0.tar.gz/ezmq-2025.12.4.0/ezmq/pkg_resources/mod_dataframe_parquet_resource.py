import json
from pathlib import Path
import pandas as pd
from .. import Resource

class DataFrameParquetResource(Resource):
    def __init__(self, identifier: str, cwd: Path = Path.cwd()):
        self.identifier = identifier
        self.cwd = cwd
        super().__init__(identifier=identifier)
        try:
            self.file_path = cwd / f"{self.identifier}.parquet"
            if not self.file_path.exists():
                self.df = pd.DataFrame()
                self.df.to_parquet(self.file_path)
        except Exception as e:
            raise e
        try:
            self.df: pd.DataFrame = pd.read_parquet(self.file_path).copy()
        except Exception as e:
            raise e

    def _enter(self):
        return self.df

    def _exit(self):
        self.df.to_parquet(self.file_path)

    def _peek(self):
        return self.df.copy()

from pytest import fixture

@fixture
def df_parquet_resource():
    return DataFrameParquetResource("test_df_parquet_resource")

def test_df_parquet_resource(df_parquet_resource):
    df = df_parquet_resource.df
    assert isinstance(df, pd.DataFrame)


def test_df_parquet_resource_peek(df_parquet_resource):
    df = df_parquet_resource.peek()
    assert isinstance(df, pd.DataFrame)

def test_df_parquet_resource_enter_exit(df_parquet_resource):
    with df_parquet_resource as df:
        assert isinstance(df, pd.DataFrame)
        df.loc[0, "a"] = 100

    with df_parquet_resource as df:
        assert df.loc[0, "a"] == 100


def test_df_parquet_resource_json(df_parquet_resource):
    with df_parquet_resource as df:
        df.loc[0, "b"] = json.dumps({"foobar": {"foobar": {"foobar"}}, "foo": 12})