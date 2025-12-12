"""Unit tests for :class:`zoho_creator_sdk.client.FormContext`."""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import Mock

import pytest
from pydantic import ValidationError as PydanticValidationError

from zoho_creator_sdk.client import FormContext
from zoho_creator_sdk.exceptions import APIError
from zoho_creator_sdk.models import Record


class TestFormContext:
    """Test cases for FormContext class."""

    @pytest.fixture
    def mock_http_client(self) -> Mock:
        """Create a mock HTTP client."""
        client = Mock()
        client.config.base_url = "https://www.zohoapis.com"
        client.config.max_records_per_request = 200
        return client

    @pytest.fixture
    def form_context(self, mock_http_client: Mock) -> FormContext:
        """Create a FormContext instance for testing."""
        return FormContext(
            http_client=mock_http_client,
            app_link_name="test-app",
            form_link_name="test-form",
            owner_name="test-owner",
        )

    def test_initialization(self, mock_http_client: Mock) -> None:
        """FormContext initializes correctly."""
        form_context = FormContext(
            http_client=mock_http_client,
            app_link_name="test-app",
            form_link_name="test-form",
            owner_name="test-owner",
        )

        assert form_context.http_client is mock_http_client
        assert form_context.app_link_name == "test-app"
        assert form_context.form_link_name == "test-form"
        assert form_context.owner_name == "test-owner"

    def test_add_record_success(self, form_context: FormContext) -> None:
        """add_record makes correct API call and returns response."""
        test_data = {"Name": "John Doe", "Email": "john@example.com"}
        expected_response = {"data": {"ID": "12345", "Name": "John Doe"}}

        form_context.http_client.post.return_value = expected_response

        result = form_context.add_record(test_data)

        expected_url = (
            "https://www.zohoapis.com/data/test-owner/test-app/form/test-form"
        )
        expected_payload = {"data": test_data}

        form_context.http_client.post.assert_called_once_with(
            expected_url, json=expected_payload
        )
        assert result == expected_response

    def test_add_record_with_empty_data(self, form_context: FormContext) -> None:
        """add_record handles empty data correctly."""
        test_data = {}
        expected_response = {"data": {"ID": "12345"}}

        form_context.http_client.post.return_value = expected_response

        result = form_context.add_record(test_data)

        expected_payload = {"data": {}}
        form_context.http_client.post.assert_called_once_with(
            "https://www.zohoapis.com/data/test-owner/test-app/form/test-form",
            json=expected_payload,
        )
        assert result == expected_response

    def test_get_records_single_page(self, form_context: FormContext) -> None:
        """get_records handles single page response correctly."""
        response_data = {
            "data": [
                {"ID": "1", "Name": "John"},
                {"ID": "2", "Name": "Jane"},
            ],
            "meta": {"more_records": False},
        }

        form_context.http_client.get.return_value = response_data

        records = list(form_context.get_records(limit=10))

        assert len(records) == 2
        assert all(isinstance(record, Record) for record in records)
        assert records[0].ID == "1"
        assert records[1].ID == "2"

        form_context.http_client.get.assert_called_once_with(
            "https://www.zohoapis.com/data/test-owner/test-app/form/test-form",
            params={"limit": 10},
        )

    def test_get_records_multiple_pages(self, form_context: FormContext) -> None:
        """get_records handles pagination correctly."""
        # First page response
        first_page = {
            "data": [{"ID": "1", "Name": "John"}],
            "meta": {
                "more_records": True,
                "next_page_token": "token123",
            },
        }

        # Second page response
        second_page = {
            "data": [{"ID": "2", "Name": "Jane"}],
            "meta": {"more_records": False},
        }

        form_context.http_client.get.side_effect = [first_page, second_page]

        records = list(form_context.get_records(limit=5))

        assert len(records) == 2
        assert records[0].ID == "1"
        assert records[1].ID == "2"

        # Verify both API calls were made
        assert form_context.http_client.get.call_count == 2

        # First call
        first_call = form_context.http_client.get.call_args_list[0]
        assert (
            first_call[0][0]
            == "https://www.zohoapis.com/data/test-owner/test-app/form/test-form"
        )
        assert first_call[1]["params"] == {"limit": 5}

        # Second call with pagination token
        second_call = form_context.http_client.get.call_args_list[1]
        assert (
            second_call[0][0]
            == "https://www.zohoapis.com/data/test-owner/test-app/form/test-form"
        )
        assert second_call[1]["params"] == {"limit": 5, "next_page_token": "token123"}

    def test_get_records_empty_response(self, form_context: FormContext) -> None:
        """get_records handles empty response correctly."""
        response_data = {"data": [], "meta": {"more_records": False}}

        form_context.http_client.get.return_value = response_data

        records = list(form_context.get_records())

        assert len(records) == 0
        form_context.http_client.get.assert_called_once()

    def test_get_records_no_data_field(self, form_context: FormContext) -> None:
        """get_records handles response without data field correctly."""
        response_data = {"meta": {"more_records": False}}

        form_context.http_client.get.return_value = response_data

        records = list(form_context.get_records())

        assert len(records) == 0
        form_context.http_client.get.assert_called_once()

    def test_get_records_with_invalid_record_data(
        self, form_context: FormContext
    ) -> None:
        """get_records raises APIError when record data is invalid."""
        response_data = {
            "data": [{"invalid": "data"}],  # Missing required fields
            "meta": {"more_records": False},
        }

        form_context.http_client.get.return_value = response_data

        with pytest.raises(APIError) as exc_info:
            list(form_context.get_records())

        assert "Failed to parse record data" in str(exc_info.value)
        assert isinstance(exc_info.value.__cause__, PydanticValidationError)

    def test_get_records_pagination_warning(self, form_context: FormContext) -> None:
        """get_records logs warning when more_records is True but no token."""
        response_data = {
            "data": [{"ID": "1", "Name": "John"}],
            "meta": {"more_records": True},  # No next_page_token
        }

        form_context.http_client.get.return_value = response_data

        records = list(form_context.get_records())

        # Should stop after first page due to missing token
        assert len(records) == 1
        assert form_context.http_client.get.call_count == 1

    def test_get_records_with_parameters(self, form_context: FormContext) -> None:
        """get_records passes through query parameters correctly."""
        response_data = {
            "data": [{"ID": "1", "Name": "John"}],
            "meta": {"more_records": False},
        }

        form_context.http_client.get.return_value = response_data

        records = list(
            form_context.get_records(
                limit=20, sort_by="Name", sort_order="asc", criteria="Name='John'"
            )
        )

        assert len(records) == 1

        form_context.http_client.get.assert_called_once_with(
            "https://www.zohoapis.com/data/test-owner/test-app/form/test-form",
            params={
                "limit": 20,
                "sort_by": "Name",
                "sort_order": "asc",
                "criteria": "Name='John'",
            },
        )

    def test_get_records_generator_behavior(self, form_context: FormContext) -> None:
        """get_records returns a generator that yields records lazily."""
        response_data = {
            "data": [{"ID": "1", "Name": "John"}],
            "meta": {"more_records": False},
        }

        form_context.http_client.get.return_value = response_data

        # Should return a generator
        result = form_context.get_records()
        assert isinstance(result, Generator)

        # API call should not be made yet
        form_context.http_client.get.assert_not_called()

        # API call should be made when we start iterating
        first_record = next(result)
        assert isinstance(first_record, Record)
        assert first_record.ID == "1"

        # API call should have been made now
        form_context.http_client.get.assert_called_once()

    @pytest.mark.parametrize(
        "app_link_name,form_link_name,owner_name,expected_url",
        [
            (
                "app1",
                "form1",
                "owner1",
                "https://www.zohoapis.com/data/owner1/app1/form/form1",
            ),
            (
                "my-app",
                "contact-form",
                "john-doe",
                "https://www.zohoapis.com/data/john-doe/my-app/form/contact-form",
            ),
            (
                "app_with_underscores",
                "form_with_underscores",
                "owner_with_underscores",
                (
                    "https://www.zohoapis.com/data/owner_with_underscores/"
                    "app_with_underscores/form/form_with_underscores"
                ),
            ),
        ],
    )
    def test_url_construction(
        self,
        mock_http_client: Mock,
        app_link_name: str,
        form_link_name: str,
        owner_name: str,
        expected_url: str,
    ) -> None:
        """FormContext constructs URLs correctly from various inputs."""
        form_context = FormContext(
            http_client=mock_http_client,
            app_link_name=app_link_name,
            form_link_name=form_link_name,
            owner_name=owner_name,
        )

        # Test add_record URL
        test_data = {"Name": "Test"}
        form_context.http_client.post.return_value = {"data": {}}
        form_context.add_record(test_data)

        form_context.http_client.post.assert_called_once_with(
            expected_url, json={"data": test_data}
        )

        # Test get_records URL
        form_context.http_client.get.return_value = {
            "data": [],
            "meta": {"more_records": False},
        }
        list(form_context.get_records())

        form_context.http_client.get.assert_called_once_with(
            expected_url, params={"max_records": 200}
        )
