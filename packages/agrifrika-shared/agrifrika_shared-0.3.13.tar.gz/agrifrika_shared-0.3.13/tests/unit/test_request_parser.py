"""Tests for request parser utility functions."""

import pytest
import json
from pydantic import BaseModel, ValidationError as PydanticValidationError
from agrifrika_shared.utils.request_parser import (
    parse_lambda_event,
    parse_lambda_body,
    get_auth_context,
    get_user_id,
    get_path_parameter,
    get_query_parameter,
    get_header,
    extract_pagination,
)


class SampleRequest(BaseModel):
    """Sample Pydantic model for testing."""
    name: str
    email: str
    age: int = 25


@pytest.mark.unit
class TestParseLambdaEvent:
    """Tests for parse_lambda_event function."""

    def test_parses_json_body(self):
        """Test parsing JSON string body into Pydantic model."""
        event = {
            'body': json.dumps({'name': 'John', 'email': 'john@example.com'})
        }

        result = parse_lambda_event(event, SampleRequest)

        assert result.name == 'John'
        assert result.email == 'john@example.com'
        assert result.age == 25  # Default value

    def test_parses_dict_body(self):
        """Test parsing dict body into Pydantic model."""
        event = {
            'body': {'name': 'Jane', 'email': 'jane@example.com', 'age': 30}
        }

        result = parse_lambda_event(event, SampleRequest)

        assert result.name == 'Jane'
        assert result.email == 'jane@example.com'
        assert result.age == 30

    def test_merges_path_parameters(self):
        """Test that path parameters are merged into body."""
        event = {
            'body': {'name': 'John', 'email': 'john@example.com'},
            'pathParameters': {'userId': '123'}
        }

        class RequestWithId(BaseModel):
            name: str
            email: str
            userId: str

        result = parse_lambda_event(event, RequestWithId)

        assert result.userId == '123'

    def test_merges_query_parameters(self):
        """Test that query parameters are merged into body."""
        event = {
            'body': {'name': 'John'},
            'queryStringParameters': {'email': 'john@example.com'}
        }

        result = parse_lambda_event(event, SampleRequest)

        assert result.name == 'John'
        assert result.email == 'john@example.com'

    def test_handles_empty_body(self):
        """Test handling of empty or missing body."""
        event = {}

        class OptionalRequest(BaseModel):
            name: str = 'default'
            email: str = 'default@example.com'

        result = parse_lambda_event(event, OptionalRequest)

        assert result.name == 'default'
        assert result.email == 'default@example.com'

    def test_handles_none_body(self):
        """Test handling of None body."""
        event = {'body': None}

        class OptionalRequest(BaseModel):
            name: str = 'default'

        result = parse_lambda_event(event, OptionalRequest)
        assert result.name == 'default'

    def test_validates_against_schema(self):
        """Test that validation errors are raised for invalid data."""
        event = {
            'body': json.dumps({'name': 'John'})  # Missing required email
        }

        with pytest.raises(PydanticValidationError):
            parse_lambda_event(event, SampleRequest)

    def test_handles_empty_string_body(self):
        """Test handling of empty string body."""
        event = {'body': ''}

        class OptionalRequest(BaseModel):
            name: str = 'default'

        result = parse_lambda_event(event, OptionalRequest)
        assert result.name == 'default'


@pytest.mark.unit
class TestParseLambdaBody:
    """Tests for parse_lambda_body function."""

    def test_parses_json_string_body(self):
        """Test parsing JSON string body."""
        event = {'body': json.dumps({'key': 'value'})}

        result = parse_lambda_body(event)

        assert result == {'key': 'value'}

    def test_parses_dict_body(self):
        """Test parsing dict body."""
        event = {'body': {'key': 'value'}}

        result = parse_lambda_body(event)

        assert result == {'key': 'value'}

    def test_handles_empty_body(self):
        """Test handling empty body."""
        event = {}

        result = parse_lambda_body(event)

        assert result == {}

    def test_handles_none_body(self):
        """Test handling None body."""
        event = {'body': None}

        result = parse_lambda_body(event)

        assert result == {}

    def test_handles_empty_string_body(self):
        """Test handling empty string body."""
        event = {'body': ''}

        result = parse_lambda_body(event)

        assert result == {}


@pytest.mark.unit
class TestGetAuthContext:
    """Tests for get_auth_context function."""

    def test_extracts_cognito_claims(self):
        """Test extracting Cognito claims from event."""
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user-123',
                        'email': 'user@example.com',
                        'custom:user_type': 'client'
                    }
                }
            }
        }

        result = get_auth_context(event)

        assert result['sub'] == 'user-123'
        assert result['email'] == 'user@example.com'
        assert result['custom:user_type'] == 'client'

    def test_returns_empty_dict_when_no_claims(self):
        """Test that empty dict is returned when no claims present."""
        event = {}

        result = get_auth_context(event)

        assert result == {}

    def test_handles_missing_authorizer(self):
        """Test handling missing authorizer context."""
        event = {'requestContext': {}}

        result = get_auth_context(event)

        assert result == {}


@pytest.mark.unit
class TestGetUserId:
    """Tests for get_user_id function."""

    def test_extracts_user_id(self):
        """Test extracting user ID from Cognito claims."""
        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user-123'
                    }
                }
            }
        }

        result = get_user_id(event)

        assert result == 'user-123'

    def test_returns_none_when_no_user_id(self):
        """Test that None is returned when no user ID present."""
        event = {}

        result = get_user_id(event)

        assert result is None


@pytest.mark.unit
class TestGetPathParameter:
    """Tests for get_path_parameter function."""

    def test_extracts_path_parameter(self):
        """Test extracting specific path parameter."""
        event = {
            'pathParameters': {
                'userId': '123',
                'orderId': '456'
            }
        }

        result = get_path_parameter(event, 'userId')

        assert result == '123'

    def test_returns_none_for_missing_parameter(self):
        """Test that None is returned for missing parameter."""
        event = {'pathParameters': {'userId': '123'}}

        result = get_path_parameter(event, 'orderId')

        assert result is None

    def test_handles_missing_path_parameters(self):
        """Test handling event with no path parameters."""
        event = {}

        result = get_path_parameter(event, 'userId')

        assert result is None

    def test_handles_none_path_parameters(self):
        """Test handling None path parameters."""
        event = {'pathParameters': None}

        result = get_path_parameter(event, 'userId')

        assert result is None


@pytest.mark.unit
class TestGetQueryParameter:
    """Tests for get_query_parameter function."""

    def test_extracts_query_parameter(self):
        """Test extracting specific query parameter."""
        event = {
            'queryStringParameters': {
                'page': '1',
                'limit': '20'
            }
        }

        result = get_query_parameter(event, 'page')

        assert result == '1'

    def test_returns_default_for_missing_parameter(self):
        """Test that default is returned for missing parameter."""
        event = {'queryStringParameters': {'page': '1'}}

        result = get_query_parameter(event, 'limit', '10')

        assert result == '10'

    def test_returns_none_when_no_default(self):
        """Test that None is returned when no default provided."""
        event = {'queryStringParameters': {}}

        result = get_query_parameter(event, 'missing')

        assert result is None

    def test_handles_missing_query_parameters(self):
        """Test handling event with no query parameters."""
        event = {}

        result = get_query_parameter(event, 'page', '1')

        assert result == '1'

    def test_handles_none_query_parameters(self):
        """Test handling None query parameters."""
        event = {'queryStringParameters': None}

        result = get_query_parameter(event, 'page', '1')

        assert result == '1'


@pytest.mark.unit
class TestGetHeader:
    """Tests for get_header function."""

    def test_extracts_header_case_sensitive(self):
        """Test extracting header with case-sensitive match."""
        event = {
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer token'
            }
        }

        result = get_header(event, 'Content-Type', case_sensitive=True)

        assert result == 'application/json'

    def test_extracts_header_case_insensitive(self):
        """Test extracting header with case-insensitive match."""
        event = {
            'headers': {
                'Content-Type': 'application/json'
            }
        }

        # Different case
        result = get_header(event, 'content-type')

        assert result == 'application/json'

    def test_returns_none_for_missing_header(self):
        """Test that None is returned for missing header."""
        event = {'headers': {'Content-Type': 'application/json'}}

        result = get_header(event, 'Authorization')

        assert result is None

    def test_handles_missing_headers(self):
        """Test handling event with no headers."""
        event = {}

        result = get_header(event, 'Content-Type')

        assert result is None

    def test_handles_none_headers(self):
        """Test handling None headers."""
        event = {'headers': None}

        result = get_header(event, 'Content-Type')

        assert result is None

    def test_case_sensitive_no_match(self):
        """Test that case-sensitive mode doesn't match wrong case."""
        event = {
            'headers': {
                'content-type': 'application/json'
            }
        }

        result = get_header(event, 'Content-Type', case_sensitive=True)

        assert result is None


@pytest.mark.unit
class TestExtractPagination:
    """Tests for extract_pagination function."""

    def test_extracts_pagination_parameters(self):
        """Test extracting pagination parameters from query string."""
        event = {
            'queryStringParameters': {
                'page': '2',
                'limit': '50'
            }
        }

        result = extract_pagination(event)

        assert result['page'] == 2
        assert result['limit'] == 50

    def test_uses_default_values(self):
        """Test that default values are used when parameters missing."""
        event = {}

        result = extract_pagination(event)

        assert result['page'] == 1
        assert result['limit'] == 20

    def test_enforces_minimum_page(self):
        """Test that page is enforced to be at least 1."""
        event = {
            'queryStringParameters': {
                'page': '0'
            }
        }

        result = extract_pagination(event)

        assert result['page'] == 1

    def test_enforces_maximum_limit(self):
        """Test that limit is capped at 100."""
        event = {
            'queryStringParameters': {
                'limit': '200'
            }
        }

        result = extract_pagination(event)

        assert result['limit'] == 100

    def test_enforces_minimum_limit(self):
        """Test that limit is enforced to be at least 1."""
        event = {
            'queryStringParameters': {
                'limit': '0'
            }
        }

        result = extract_pagination(event)

        assert result['limit'] == 1

    def test_handles_negative_values(self):
        """Test handling negative values."""
        event = {
            'queryStringParameters': {
                'page': '-5',
                'limit': '-10'
            }
        }

        result = extract_pagination(event)

        assert result['page'] == 1
        assert result['limit'] == 1
