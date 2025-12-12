import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime

from orion.acrecer.etl_acrecer import (
    load_data_for_table_acrecer,
    to_mysql_dt,
    format_dates,
    split_by_type_transaccion,
)
from orion.definition_ids import ID_BASE_MLS_ACRECER


# --- Unit tests for helper functions ---

def test_split_by_type_transaccion_not_implemented():
    """Test that split_by_type_transaccion raises NotImplementedError."""
    with pytest.raises(NotImplementedError):
        split_by_type_transaccion()


def test_format_dates():
    """Test the format_dates function."""
    iso_date = "2023-10-26T10:00:00Z"
    expected = "2023-10-26 00:00:00"  # Note: .date() truncates time
    assert format_dates(iso_date) == expected


def test_to_mysql_dt():
    """Test the to_mysql_dt function for date conversion."""
    assert to_mysql_dt("2023-10-26T10:00:00Z") == datetime(2023, 10, 26, 10, 0, 0)
    assert to_mysql_dt(None) is None
    assert to_mysql_dt("  ") is None


# --- Fixtures for ETL tests ---

@pytest.fixture
def mock_db_queries(mocker):
    """Mocks all database query methods."""
    mocker.patch("orion.acrecer.etl_acrecer.QuerysMLSAcrecer.upsert_all")
    mocker.patch("orion.acrecer.etl_acrecer.QuerysMLSAcrecer.delete_by_id")
    mocker.patch("orion.acrecer.etl_acrecer.QuerysMLSAcrecer.bulk_insert")
    return mocker.patch("orion.acrecer.etl_acrecer.QuerysMLSAcrecer")


@pytest.fixture
def mock_api_data(mocker):
    """Mocks the main API data fetching function."""
    return mocker.patch("orion.acrecer.etl_acrecer.get_all_properties_acrecer_by_city_sync")


@pytest.fixture
def mock_db_session(mocker):
    """Mocks the database session and the initial data read."""
    mock_session = MagicMock()
    # Patch the context manager
    mock_context = mocker.patch("orion.acrecer.etl_acrecer.get_session_bellatrix")
    mock_context.return_value.__enter__.return_value = mock_session
    return mock_session


# --- ETL Logic Tests for load_data_for_table_acrecer ---

def test_etl_initial_load(mock_api_data, mock_db_session, mock_db_queries):
    """
    Test Case: The database is empty, and the API returns new properties.
    Expected: All new properties are bulk inserted.
    """
    # Arrange: API returns two new properties
    api_df = pd.DataFrame({
        "code": ["MLS-101", "MLS-102"],
        "addedOn": ["2023-01-01T10:00:00Z", "2023-01-02T10:00:00Z"],
        "lastUpdate": ["2023-01-01T10:00:00Z", "2023-01-02T10:00:00Z"],
        "propertyImages": ["img1.jpg", "img2.jpg"],
    })
    mock_api_data.return_value = api_df

    # Arrange: DB is empty
    with patch("orion.acrecer.etl_acrecer.list_obj_to_df", return_value=pd.DataFrame()):
        # Act
        load_data_for_table_acrecer()

    # Assert
    mock_db_queries.bulk_insert.assert_called_once()
    mock_db_queries.upsert_all.assert_not_called()
    mock_db_queries.delete_by_id.assert_not_called()

    # Assert on the content of the call
    inserted_records = mock_db_queries.bulk_insert.call_args[0][0]
    assert len(inserted_records) == 2
    assert inserted_records[0]["id"] == 101 + ID_BASE_MLS_ACRECER


def test_etl_no_changes(mock_api_data, mock_db_session, mock_db_queries):
    """
    Test Case: API data and DB data are identical.
    Expected: No database operations are performed.
    """
    # Arrange: API returns one property
    api_df = pd.DataFrame({
        "code": ["MLS-101"],
        "addedOn": ["2023-01-01T10:00:00Z"],
        "lastUpdate": ["2023-01-01T10:00:00Z"],
        "propertyImages": ["img1.jpg"],
    })
    mock_api_data.return_value = api_df

    # Arrange: DB has the same property
    db_df = pd.DataFrame({
        "id": [101 + ID_BASE_MLS_ACRECER],
        "lastUpdate": [datetime(2023, 1, 1, 10, 0, 0)],
    })
    with patch("orion.acrecer.etl_acrecer.list_obj_to_df", return_value=db_df):
        # Act
        load_data_for_table_acrecer()

    # Assert
    mock_db_queries.bulk_insert.assert_not_called()
    mock_db_queries.upsert_all.assert_not_called()
    mock_db_queries.delete_by_id.assert_not_called()


def test_etl_updates_and_deletes(mock_api_data, mock_db_session, mock_db_queries):
    """
    Test Case: One property is updated, another is removed from the API.
    Expected: One upsert, one delete.
    """
    # Arrange: API returns one updated property
    api_df = pd.DataFrame({
        "code": ["MLS-101"],
        "addedOn": ["2023-01-01T10:00:00Z"],
        "lastUpdate": ["2023-01-01T12:00:00Z"],  # Updated time
        "propertyImages": ["img1_new.jpg"],
    })
    mock_api_data.return_value = api_df

    # Arrange: DB has the old version of prop 101 and another prop 102
    db_df = pd.DataFrame({
        "id": [101 + ID_BASE_MLS_ACRECER, 102 + ID_BASE_MLS_ACRECER],
        "lastUpdate": [datetime(2023, 1, 1, 10, 0, 0), datetime(2023, 1, 2, 10, 0, 0)],
    })
    with patch("orion.acrecer.etl_acrecer.list_obj_to_df", return_value=db_df):
        # Act
        load_data_for_table_acrecer()

    # Assert: Update for 101
    mock_db_queries.upsert_all.assert_called_once()
    updated_records = mock_db_queries.upsert_all.call_args[0][0]
    assert len(updated_records) == 1
    assert updated_records[0]["id"] == 101 + ID_BASE_MLS_ACRECER

    # Assert: Delete for 102
    mock_db_queries.delete_by_id.assert_called_once_with(102 + ID_BASE_MLS_ACRECER)

    # Assert: No inserts
    mock_db_queries.bulk_insert.assert_not_called()
