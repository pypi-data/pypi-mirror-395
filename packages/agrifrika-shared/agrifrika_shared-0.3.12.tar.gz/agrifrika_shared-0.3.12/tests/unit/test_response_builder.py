"""Tests for response_builder utility functions."""

import pytest
import json
from agrifrika_shared.utils.response_builder import (
    success_response,
    error_response,
    cors_response
)
from agrifrika_shared.utils.exceptions import NotFoundError, ValidationError


class TestSuccessResponse:
    """Tests for success_response function."""

    def test_success_response_with_dict_data(self):
        """Test success response with dictionary data."""
        data = {"id": "123", "name": "Test"}
        response = success_response(data)

        assert response["statusCode"] == 200
        assert "headers" in response
        assert response["headers"]["Content-Type"] == "application/json"

        body = json.loads(response["body"])
        assert body["message"] == "Success"
        assert body["data"] == data

    def test_success_response_with_list_data(self):
        """Test success response with list data."""
        data = [{"id": "1"}, {"id": "2"}]
        response = success_response(data)

        body = json.loads(response["body"])
        assert body["message"] == "Success"
        assert body["data"] == data
        assert len(body["data"]) == 2

    def test_success_response_with_custom_status_code(self):
        """Test success response with custom status code."""
        data = {"id": "123"}
        response = success_response(data, status_code=201)

        assert response["statusCode"] == 201

    def test_success_response_with_custom_message(self):
        """Test success response with custom message."""
        data = {"id": "123"}
        message = "Resource created successfully"
        response = success_response(data, message=message)

        body = json.loads(response["body"])
        assert body["message"] == message

    def test_success_response_cors_headers(self):
        """Test that CORS headers are included."""
        response = success_response({"test": "data"})

        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"


class TestErrorResponse:
    """Tests for error_response function."""

    def test_error_response_basic(self):
        """Test basic error response."""
        message = "Resource not found"
        response = error_response(message, status_code=404)

        assert response["statusCode"] == 404
        body = json.loads(response["body"])
        assert body["message"] == message

    def test_error_response_with_error_code(self):
        """Test error response with error code."""
        response = error_response(
            "Validation failed",
            status_code=400,
            error_code="VALIDATION_ERROR"
        )

        body = json.loads(response["body"])
        assert body["error_code"] == "VALIDATION_ERROR"

    def test_error_response_with_details(self):
        """Test error response with details."""
        details = {"field": "email", "reason": "Invalid format"}
        response = error_response(
            "Validation failed",
            status_code=400,
            details=details
        )

        body = json.loads(response["body"])
        assert body["details"] == details

    def test_error_response_from_exception(self):
        """Test error response created from exception."""
        exception = NotFoundError("User")
        response = error_response(str(exception), status_code=404)

        body = json.loads(response["body"])
        assert body["message"] == "User not found"
        assert response["statusCode"] == 404

    def test_error_response_cors_headers(self):
        """Test that CORS headers are included in error responses."""
        response = error_response("Error", status_code=500)

        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"


class TestCorsResponse:
    """Tests for cors_response function."""

    def test_cors_response_returns_200(self):
        """Test that CORS response returns 200."""
        response = cors_response()
        assert response["statusCode"] == 200

    def test_cors_response_has_required_headers(self):
        """Test that CORS response has all required headers."""
        response = cors_response()

        headers = response["headers"]
        assert "Access-Control-Allow-Origin" in headers
        assert "Access-Control-Allow-Methods" in headers
        assert "Access-Control-Allow-Headers" in headers
        assert "Access-Control-Max-Age" in headers

    def test_cors_response_allow_origin(self):
        """Test CORS allow origin header."""
        response = cors_response()
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    def test_cors_response_allowed_methods(self):
        """Test CORS allowed methods."""
        response = cors_response()
        methods = response["headers"]["Access-Control-Allow-Methods"]
        assert "GET" in methods
        assert "POST" in methods
        assert "PUT" in methods
        assert "DELETE" in methods
        assert "OPTIONS" in methods

    def test_cors_response_empty_body(self):
        """Test that CORS response has empty body."""
        response = cors_response()
        assert response["body"] == ""
