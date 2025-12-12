from __future__ import annotations

import datetime
import json
import os

import pandas as pd
import pytest
from dotenv import load_dotenv

from datafarmclient import DatafarmClient
from datafarmclient.base import json_to_pandas
from datafarmclient.exceptions import EntityExistsError
from datafarmclient.utils import format_datetime

load_dotenv()


def requires_DATAFARM_API_KEY():
    api_key = os.environ.get("DATAFARM_API_KEY")
    reason = "Environment variable DATAFARM_API_KEY not present"
    return pytest.mark.skipif(api_key is None, reason=reason)


@pytest.fixture
def api_key() -> str:
    return os.getenv("DATAFARM_API_KEY")


@pytest.fixture
def repo(api_key: str) -> DatafarmClient:
    api_url = os.environ.get("DATAFARM_API_URL")
    assert api_key is not None
    dfr = DatafarmClient(api_url)
    dfr.login(api_key=api_key)
    return dfr


@pytest.fixture
def json_input() -> str:
    data = {
        "schema": {
            "fields": [
                {"name": "GUID", "type": "string"},
                {"name": "ID", "type": "integer"},
                {"name": "EntityID", "type": "string"},
                {"name": "Touched", "type": "datetime"},
            ],
            "primaryKey": ["GUID"],
            "pandas_version": "0.20.0",
        },
        "data": [
            [
                "{62F60AF2-C34A-11ED-B2F7-1831BF2DC749}",
                2,
                "AKZ_waves_CMEMS_unfiltered_Hm0",
                1679332722000,
            ]
        ],
    }

    return json.dumps(data)


@pytest.fixture
def json_input_empty() -> str:
    data = {
        "schema": {
            "fields": [
                {"name": "GUID", "type": "string"},
                {"name": "ID", "type": "integer"},
                {"name": "EntityID", "type": "string"},
                {"name": "Touched", "type": "datetime"},
            ],
            "primaryKey": ["GUID"],
            "pandas_version": "0.20.0",
        }
    }

    return json.dumps(data)


@requires_DATAFARM_API_KEY()
def test_connection(repo: DatafarmClient, api_key: str):
    assert repo.connected
    repo.logoff()
    assert not repo.connected
    repo.login(api_key=api_key)
    assert repo.connected


@requires_DATAFARM_API_KEY()
def test_list_time_series(repo: DatafarmClient):
    assert len(repo.timeseries.list()) > 1


@requires_DATAFARM_API_KEY()
def test_not_exists(repo: DatafarmClient):
    entity_name = "test_ts_4"
    response_exists = repo.entities("enTimeSeries").exists(entity_name)

    assert response_exists is False


@requires_DATAFARM_API_KEY()
def test_exists(repo: DatafarmClient):
    entity_name = "test_ts_3"
    response_exists = repo.entities("enTimeSeries").exists(entity_name)

    assert response_exists is True


@requires_DATAFARM_API_KEY()
def test_get_data(repo: DatafarmClient):
    time_series = "testapi.insert"
    data = repo.timeseries.get_data(
        time_series_id=[time_series],
        start="2015-03-24T10:16:45.034Z",
        end="2023-03-24T10:16:45.034Z",
        limit=10,
    )
    assert data is not None
    assert isinstance(data, list)
    data = data[0]
    assert data.shape == (10, 2)
    assert data.columns.tolist() == ["Data", "QualityTxt"]
    assert data.index.name == "RefDateTimeRef"


@requires_DATAFARM_API_KEY()
def test_get_data_5_rows(repo: DatafarmClient):
    time_series = "Sleipner-A_waves_CMEMS_unfiltered_Hm0"
    data = repo.timeseries.get_data(
        time_series_id=[time_series],
        start="2015-03-24T10:16:45.034Z",
        end="2023-03-24T10:16:45.034Z",
        limit=5,
    )
    assert isinstance(data, list)
    data = data[0]
    assert data.shape == (5, 2)


@requires_DATAFARM_API_KEY()
def test_get_data_with_resampling(repo: DatafarmClient):
    resampling = repo.timeseries.create_resample(
        method="interpolation", repetition_type="stairs", period="apHour"
    )
    time_series = "Ekofisk_waves_CMEMS_filtered_Tp"
    data = repo.timeseries.get_data(
        time_series_id=[time_series],
        start="2015-03-24T10:16:45.034Z",
        end="2023-03-24T10:16:45.034Z",
        limit=1000,
        aggregation=resampling,
    )
    assert data is not None
    assert isinstance(data, list)
    data = data[0]
    assert data.columns.tolist() == ["Data", "QualityId"]
    assert data.index.name == "RefDateTimeRef"


@requires_DATAFARM_API_KEY()
def test_get_data_with_aggregation(repo: DatafarmClient):
    agg = repo.timeseries.create_aggregation(method="amMedian", period="apDay")
    time_series = "Ekofisk_waves_CMEMS_filtered_Tp"
    data = repo.timeseries.get_data(
        time_series_id=[time_series],
        start="2015-03-24T10:16:45.034Z",
        end="2023-03-24T10:16:45.034Z",
        limit=1000,
        aggregation=agg,
    )
    assert data is not None
    assert isinstance(data, list)
    data = data[0]
    assert data.columns.tolist() == ["Data", "QualityId"]
    assert data.index.name == "RefDateTimeRef"


def test_to_dataframe(json_input):
    df = json_to_pandas(json_input)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 3)
    assert df.columns.tolist() == ["ID", "EntityID", "Touched"]
    assert df.index.name == "GUID"
    assert df["Touched"].dtype == "datetime64[ns]"


def test_to_dataframe_empty(json_input_empty):
    df = json_to_pandas(json_input_empty)
    assert isinstance(df, pd.DataFrame)
    assert df.empty
    assert df.shape == (0, 4)
    assert df.columns.tolist() == ["GUID", "ID", "EntityID", "Touched"]


def test_to_dataframe_error():
    with pytest.raises(ValueError):
        json_to_pandas("{}")


def test_parse_datetime_valid():
    dt = "2023-05-15T14:30:00"
    result = format_datetime(dt)
    expected = "2023-05-15T14:30:00.000Z"
    assert result == expected


def test_parse_datetime_invalid():
    dt = "2023-50-50"
    with pytest.raises(ValueError):
        format_datetime(dt)


def test_parse_datetime_other_formate():
    dt = "05/15/2023 14:30:00"
    result = format_datetime(dt)
    expected = "2023-05-15T14:30:00.000Z"
    assert result == expected


def test_parse_datetime_object():
    dt = datetime.datetime(2023, 5, 15, 14, 30, 0)
    result = format_datetime(dt)
    expected = "2023-05-15T14:30:00.000Z"
    assert result == expected


@requires_DATAFARM_API_KEY()
def test_units(repo: DatafarmClient):
    units = repo.units
    assert units is not None
    assert isinstance(units, pd.DataFrame)
    assert "IDName" in units.columns.tolist()
    assert "l/min" in units["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_time_series_source_descriptions(repo: DatafarmClient):
    time_series_source_descriptions = repo.time_series_source_descriptions
    assert time_series_source_descriptions is not None
    assert isinstance(time_series_source_descriptions, pd.DataFrame)
    assert "IDName" in time_series_source_descriptions.columns.tolist()


@requires_DATAFARM_API_KEY()
def test_time_series_types(repo: DatafarmClient):
    time_series_types = repo.time_series_types
    assert time_series_types is not None
    assert isinstance(time_series_types, pd.DataFrame)
    assert "IDName" in time_series_types.columns.tolist()
    assert "CMEMS" in time_series_types["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_time_series_status(repo: DatafarmClient):
    time_series_status = repo.time_series_status
    assert time_series_status is not None
    assert isinstance(time_series_status, pd.DataFrame)
    assert "IDName" in time_series_status.columns.tolist()
    assert "filtered" in time_series_status["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_qualities(repo: DatafarmClient):
    qualities = repo.qualities
    assert qualities is not None
    assert isinstance(qualities, pd.DataFrame)
    assert "IDName" in qualities.columns.tolist()
    assert "ok" in qualities["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_parameters(repo: DatafarmClient):
    parameters = repo.parameters
    assert parameters is not None
    assert isinstance(parameters, pd.DataFrame)
    assert "IDName" in parameters.columns.tolist()
    assert "Hm0" in parameters["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_medias(repo: DatafarmClient):
    medias = repo.medias
    assert medias is not None
    assert isinstance(medias, pd.DataFrame)
    assert "IDName" in medias.columns.tolist()
    assert "waves" in medias["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_locations(repo: DatafarmClient):
    assert hasattr(repo, "locations")
    locations = repo.locations
    assert locations is not None
    assert isinstance(locations, pd.DataFrame)
    assert "IDName" in locations.columns.tolist()
    assert "Sleipner-A" in locations["IDName"].tolist()


@requires_DATAFARM_API_KEY()
def test_entity_crud(repo: DatafarmClient):
    entity_name = "test_ts_4"
    # Create
    entity_id = repo.entities("enTimeSeries").create(
        id_name=entity_name, fields={"IDDescription": "test4"}
    )
    assert entity_id is not None

    # Create if exists - raises an exception
    with pytest.raises(EntityExistsError):
        repo.entities("enTimeSeries").create(
            id_name=entity_name, fields={"IDDescription": "test4"}
        )

    # Get entity ID of newly created entity
    response_get = repo.entities("enTimeSeries").get(entity_name)
    assert response_get is not None
    assert response_get == entity_id

    # Delete entity again
    response_delete = repo.entities("enTimeSeries").delete(entity_id)
    assert response_delete.status_code == 200
    assert response_delete.json()["result"] == f"Entity: {entity_id} deleted"


@requires_DATAFARM_API_KEY()
def test_entity_list(repo: DatafarmClient):
    res = repo.entities("enTimeSeries").list(fields=["Id", "EntityId"])
    assert "Id" in res.columns.tolist()
    assert "EntityId" in res.columns.tolist()


@requires_DATAFARM_API_KEY()
def test_time_series_insert_data(repo: DatafarmClient):
    import pandas as pd

    data = pd.DataFrame(
        {
            "QualityTxt": ["ok", "critical"],
            "Data": [None, 3],
        },
        index=[
            pd.to_datetime("2020-01-01T00:00:00Z"),
            pd.to_datetime("2020-01-01T12:00:00Z"),
        ],
    )

    response = repo.timeseries.insert_data(time_series_id="test_ts_3", data=data)
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json, dict)


@requires_DATAFARM_API_KEY()
def test_time_series_insert_data_file(repo: DatafarmClient):
    data = pd.DataFrame(
        {
            "QualityTxt": ["ok", "ok", "critical"],
            "Data": [1.23, None, 3],
            "FilePath": [
                "tests/data/test_upload.txt",
                "tests/data/test_upload.txt",
                "tests/data/test_upload.txt",
            ],
        },
        index=[
            pd.to_datetime("2020-01-01T00:00:00Z"),
            pd.to_datetime("2020-01-01T12:00:00Z"),
            pd.to_datetime("2020-01-01T18:00:00Z"),
        ],
    )
    response = repo.timeseries.insert_data(time_series_id="test_ts_3", data=data)
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json, dict)


@requires_DATAFARM_API_KEY()
def test_time_series_delete_data(repo: DatafarmClient):
    timestamp = pd.Timestamp("2020-01-02T11:00:00Z")
    delta = pd.Timedelta(microseconds=1)

    data = pd.DataFrame(
        {
            "Data": [1],
            "QualityTxt": ["ok"],
        },
        index=[timestamp],
    )
    repo.timeseries.insert_data("test_ts_3", data, bulk_insert=True)
    res = repo.timeseries.get_data("test_ts_3", start=timestamp, end=timestamp + delta)
    assert len(res) > 0
    assert len(res[0]) == 1

    repo.timeseries.delete_data("test_ts_3", timestamps=[timestamp])
    res = repo.timeseries.get_data("test_ts_3", start=timestamp, end=timestamp + delta)
    assert len(res[0]) == 0


@requires_DATAFARM_API_KEY()
def test_time_series_update_data_quality(repo: DatafarmClient):
    timestamp = pd.Timestamp("2020-01-02T11:00:00Z")
    delta = pd.Timedelta(microseconds=1)

    data = pd.DataFrame(
        {
            "Data": [1],
            "QualityTxt": ["ok"],
        },
        index=[timestamp],
    )
    repo.timeseries.insert_data("test_ts_3", data, bulk_insert=True)
    res = repo.timeseries.get_data("test_ts_3", start=timestamp, end=timestamp + delta)
    assert len(res) == 1
    assert len(res[0]) > 0
    qualities = res[0].QualityTxt.copy()
    qualities.iloc[0] = "critical"
    repo.timeseries.update_data_quality("test_ts_3", qualities)
    res = repo.timeseries.get_data("test_ts_3", start=timestamp, end=timestamp + delta)
    assert len(res) == 1
    assert len(res[0]) > 0
    assert res[0].iloc[0]["QualityTxt"] == "critical"


@requires_DATAFARM_API_KEY()
def test_time_series_latest_values(repo: DatafarmClient):
    res = repo.timeseries.latest_values(["testapi.insert", "test_ts_3"])
    assert len(res) == 2
    assert "testapi.insert" in res.index.values
    assert "test_ts_3" in res.index.values
