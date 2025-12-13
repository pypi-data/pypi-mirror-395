# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from enum import Enum

import pytest

from ipsdk.http import HTTPMethod
from ipsdk.http import HTTPStatus


class TestHTTPStatus:
    """Test cases for the HTTPStatus enumeration.

    Note: HTTPStatus is Python's standard library enum (http.HTTPStatus).
    These tests verify that the standard library enum is available and working.
    """

    def test_http_status_is_enum(self):
        """Test that HTTPStatus is an Enum class."""
        assert issubclass(HTTPStatus, Enum)

    def test_http_status_from_stdlib(self):
        """Test that HTTPStatus is from the standard library."""
        assert HTTPStatus.__module__ == "http"

    def test_informational_status_codes(self):
        """Test 1xx informational status codes."""
        assert HTTPStatus.CONTINUE.value == 100
        assert HTTPStatus.SWITCHING_PROTOCOLS.value == 101
        assert HTTPStatus.PROCESSING.value == 102
        assert HTTPStatus.EARLY_HINTS.value == 103

    def test_success_status_codes(self):
        """Test 2xx success status codes."""
        assert HTTPStatus.OK.value == 200
        assert HTTPStatus.CREATED.value == 201
        assert HTTPStatus.ACCEPTED.value == 202
        assert HTTPStatus.NON_AUTHORITATIVE_INFORMATION.value == 203
        assert HTTPStatus.NO_CONTENT.value == 204
        assert HTTPStatus.RESET_CONTENT.value == 205
        assert HTTPStatus.PARTIAL_CONTENT.value == 206
        assert HTTPStatus.MULTI_STATUS.value == 207
        assert HTTPStatus.ALREADY_REPORTED.value == 208
        assert HTTPStatus.IM_USED.value == 226

    def test_redirection_status_codes(self):
        """Test 3xx redirection status codes."""
        assert HTTPStatus.MULTIPLE_CHOICES.value == 300
        assert HTTPStatus.MOVED_PERMANENTLY.value == 301
        assert HTTPStatus.FOUND.value == 302
        assert HTTPStatus.SEE_OTHER.value == 303
        assert HTTPStatus.NOT_MODIFIED.value == 304
        assert HTTPStatus.USE_PROXY.value == 305
        assert HTTPStatus.TEMPORARY_REDIRECT.value == 307
        assert HTTPStatus.PERMANENT_REDIRECT.value == 308

    def test_client_error_status_codes(self):
        """Test 4xx client error status codes."""
        assert HTTPStatus.BAD_REQUEST.value == 400
        assert HTTPStatus.UNAUTHORIZED.value == 401
        assert HTTPStatus.PAYMENT_REQUIRED.value == 402
        assert HTTPStatus.FORBIDDEN.value == 403
        assert HTTPStatus.NOT_FOUND.value == 404
        assert HTTPStatus.METHOD_NOT_ALLOWED.value == 405
        assert HTTPStatus.NOT_ACCEPTABLE.value == 406
        assert HTTPStatus.PROXY_AUTHENTICATION_REQUIRED.value == 407
        assert HTTPStatus.REQUEST_TIMEOUT.value == 408
        assert HTTPStatus.CONFLICT.value == 409
        assert HTTPStatus.GONE.value == 410
        assert HTTPStatus.LENGTH_REQUIRED.value == 411
        assert HTTPStatus.PRECONDITION_FAILED.value == 412
        # Standard library uses different names for some status codes
        assert HTTPStatus.REQUEST_ENTITY_TOO_LARGE.value == 413
        assert HTTPStatus.REQUEST_URI_TOO_LONG.value == 414
        assert HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value == 415
        assert HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE.value == 416
        assert HTTPStatus.EXPECTATION_FAILED.value == 417
        assert HTTPStatus.IM_A_TEAPOT.value == 418
        assert HTTPStatus.MISDIRECTED_REQUEST.value == 421
        assert HTTPStatus.UNPROCESSABLE_ENTITY.value == 422
        assert HTTPStatus.LOCKED.value == 423
        assert HTTPStatus.FAILED_DEPENDENCY.value == 424
        assert HTTPStatus.TOO_EARLY.value == 425
        assert HTTPStatus.UPGRADE_REQUIRED.value == 426
        assert HTTPStatus.PRECONDITION_REQUIRED.value == 428
        assert HTTPStatus.TOO_MANY_REQUESTS.value == 429
        assert HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE.value == 431
        assert HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS.value == 451

    def test_server_error_status_codes(self):
        """Test 5xx server error status codes."""
        assert HTTPStatus.INTERNAL_SERVER_ERROR.value == 500
        assert HTTPStatus.NOT_IMPLEMENTED.value == 501
        assert HTTPStatus.BAD_GATEWAY.value == 502
        assert HTTPStatus.SERVICE_UNAVAILABLE.value == 503
        assert HTTPStatus.GATEWAY_TIMEOUT.value == 504
        assert HTTPStatus.HTTP_VERSION_NOT_SUPPORTED.value == 505
        assert HTTPStatus.VARIANT_ALSO_NEGOTIATES.value == 506
        assert HTTPStatus.INSUFFICIENT_STORAGE.value == 507
        assert HTTPStatus.LOOP_DETECTED.value == 508
        assert HTTPStatus.NOT_EXTENDED.value == 510
        assert HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED.value == 511

    def test_status_code_by_name(self):
        """Test accessing status codes by name."""
        assert HTTPStatus["OK"].value == 200
        assert HTTPStatus["NOT_FOUND"].value == 404
        assert HTTPStatus["INTERNAL_SERVER_ERROR"].value == 500

    def test_status_code_by_value(self):
        """Test accessing status codes by value."""
        assert HTTPStatus(200) == HTTPStatus.OK
        assert HTTPStatus(404) == HTTPStatus.NOT_FOUND
        assert HTTPStatus(500) == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_status_code_comparison(self):
        """Test comparing status codes."""
        assert HTTPStatus.OK.value < HTTPStatus.NOT_FOUND.value
        assert HTTPStatus.NOT_FOUND.value < HTTPStatus.INTERNAL_SERVER_ERROR.value
        assert HTTPStatus.OK == HTTPStatus.OK
        assert HTTPStatus.OK != HTTPStatus.CREATED

    def test_status_code_iteration(self):
        """Test iterating over all status codes."""
        all_statuses = list(HTTPStatus)
        assert len(all_statuses) > 0
        assert HTTPStatus.OK in all_statuses
        assert HTTPStatus.NOT_FOUND in all_statuses
        assert HTTPStatus.INTERNAL_SERVER_ERROR in all_statuses

    def test_status_code_membership(self):
        """Test membership testing for status codes."""
        assert HTTPStatus.OK in HTTPStatus
        assert HTTPStatus.NOT_FOUND in HTTPStatus
        assert HTTPStatus.INTERNAL_SERVER_ERROR in HTTPStatus

    def test_status_code_names(self):
        """Test that status code names match expected values."""
        assert HTTPStatus.OK.name == "OK"
        assert HTTPStatus.NOT_FOUND.name == "NOT_FOUND"
        assert HTTPStatus.INTERNAL_SERVER_ERROR.name == "INTERNAL_SERVER_ERROR"

    def test_status_code_uniqueness(self):
        """Test that all status code values are unique."""
        values = [status.value for status in HTTPStatus]
        assert len(values) == len(set(values))

    def test_commonly_used_status_codes(self):
        """Test commonly used status codes are present."""
        # Most common success codes
        assert HTTPStatus.OK.value == 200
        assert HTTPStatus.CREATED.value == 201
        assert HTTPStatus.NO_CONTENT.value == 204

        # Most common client error codes
        assert HTTPStatus.BAD_REQUEST.value == 400
        assert HTTPStatus.UNAUTHORIZED.value == 401
        assert HTTPStatus.FORBIDDEN.value == 403
        assert HTTPStatus.NOT_FOUND.value == 404

        # Most common server error codes
        assert HTTPStatus.INTERNAL_SERVER_ERROR.value == 500
        assert HTTPStatus.BAD_GATEWAY.value == 502
        assert HTTPStatus.SERVICE_UNAVAILABLE.value == 503

    def test_status_code_ranges(self):
        """Test that status codes are in correct ranges."""
        for status in HTTPStatus:
            if status.name.startswith(("CONTINUE", "SWITCHING", "PROCESSING", "EARLY")):
                assert 100 <= status.value < 200
            elif status.name in (
                "OK",
                "CREATED",
                "ACCEPTED",
                "NON_AUTHORITATIVE_INFORMATION",
                "NO_CONTENT",
                "RESET_CONTENT",
                "PARTIAL_CONTENT",
                "MULTI_STATUS",
                "ALREADY_REPORTED",
                "IM_USED",
            ):
                assert 200 <= status.value < 300
            elif status.name in (
                "MULTIPLE_CHOICES",
                "MOVED_PERMANENTLY",
                "FOUND",
                "SEE_OTHER",
                "NOT_MODIFIED",
                "USE_PROXY",
                "TEMPORARY_REDIRECT",
                "PERMANENT_REDIRECT",
            ):
                assert 300 <= status.value < 400

    def test_invalid_status_code_raises_error(self):
        """Test that accessing non-existent status code raises ValueError."""
        with pytest.raises(ValueError):
            HTTPStatus(999)

    def test_status_code_string_representation(self):
        """Test string representation of status codes."""
        assert "HTTPStatus.OK" in repr(HTTPStatus.OK)
        assert "HTTPStatus.NOT_FOUND" in repr(HTTPStatus.NOT_FOUND)


class TestHTTPMethod:
    """Test cases for the HTTPMethod enumeration.

    Note: HTTPMethod uses http.HTTPMethod from standard library on Python 3.11+,
    and a custom implementation for backward compatibility on Python < 3.11.
    """

    def test_http_method_is_enum(self):
        """Test that HTTPMethod is an Enum class."""
        assert issubclass(HTTPMethod, Enum)

    def test_http_method_availability(self):
        """Test that HTTPMethod is available regardless of Python version."""
        # HTTPMethod should be available on all supported Python versions
        assert HTTPMethod is not None

        # Verify it has the expected behavior
        assert hasattr(HTTPMethod, "GET")
        assert hasattr(HTTPMethod, "POST")
        assert HTTPMethod.GET.value == "GET"

    def test_standard_http_methods(self):
        """Test standard HTTP methods are defined."""
        assert HTTPMethod.GET.value == "GET"
        assert HTTPMethod.POST.value == "POST"
        assert HTTPMethod.PUT.value == "PUT"
        assert HTTPMethod.DELETE.value == "DELETE"
        assert HTTPMethod.PATCH.value == "PATCH"
        assert HTTPMethod.HEAD.value == "HEAD"
        assert HTTPMethod.OPTIONS.value == "OPTIONS"
        assert HTTPMethod.TRACE.value == "TRACE"
        assert HTTPMethod.CONNECT.value == "CONNECT"

    def test_method_by_name(self):
        """Test accessing methods by name."""
        assert HTTPMethod["GET"].value == "GET"
        assert HTTPMethod["POST"].value == "POST"
        assert HTTPMethod["DELETE"].value == "DELETE"

    def test_method_by_value(self):
        """Test accessing methods by value."""
        assert HTTPMethod("GET") == HTTPMethod.GET
        assert HTTPMethod("POST") == HTTPMethod.POST
        assert HTTPMethod("DELETE") == HTTPMethod.DELETE

    def test_method_comparison(self):
        """Test comparing HTTP methods."""
        assert HTTPMethod.GET == HTTPMethod.GET
        assert HTTPMethod.GET != HTTPMethod.POST
        assert HTTPMethod.PUT != HTTPMethod.PATCH

    def test_method_iteration(self):
        """Test iterating over all HTTP methods."""
        all_methods = list(HTTPMethod)
        assert len(all_methods) == 9
        assert HTTPMethod.GET in all_methods
        assert HTTPMethod.POST in all_methods
        assert HTTPMethod.DELETE in all_methods

    def test_method_membership(self):
        """Test membership testing for HTTP methods."""
        assert HTTPMethod.GET in HTTPMethod
        assert HTTPMethod.POST in HTTPMethod
        assert HTTPMethod.DELETE in HTTPMethod

    def test_method_names(self):
        """Test that method names match expected values."""
        assert HTTPMethod.GET.name == "GET"
        assert HTTPMethod.POST.name == "POST"
        assert HTTPMethod.DELETE.name == "DELETE"

    def test_method_values_are_strings(self):
        """Test that all method values are strings."""
        for method in HTTPMethod:
            assert isinstance(method.value, str)
            assert method.value.isupper()

    def test_method_uniqueness(self):
        """Test that all method values are unique."""
        values = [method.value for method in HTTPMethod]
        assert len(values) == len(set(values))

    def test_commonly_used_methods(self):
        """Test commonly used HTTP methods are present."""
        # CRUD operations
        assert HTTPMethod.GET.value == "GET"  # Read
        assert HTTPMethod.POST.value == "POST"  # Create
        assert HTTPMethod.PUT.value == "PUT"  # Update/Replace
        assert HTTPMethod.PATCH.value == "PATCH"  # Partial Update
        assert HTTPMethod.DELETE.value == "DELETE"  # Delete

        # Other common methods
        assert HTTPMethod.HEAD.value == "HEAD"
        assert HTTPMethod.OPTIONS.value == "OPTIONS"

    def test_invalid_method_raises_error(self):
        """Test that accessing non-existent method raises ValueError."""
        with pytest.raises(ValueError):
            HTTPMethod("INVALID")

    def test_method_string_representation(self):
        """Test string representation of HTTP methods."""
        assert "HTTPMethod.GET" in repr(HTTPMethod.GET)
        assert "HTTPMethod.POST" in repr(HTTPMethod.POST)

    def test_method_value_matches_name(self):
        """Test that method values match their names."""
        for method in HTTPMethod:
            assert method.value == method.name

    def test_safe_vs_unsafe_methods(self):
        """Test categorization of safe vs unsafe HTTP methods."""
        # Safe methods (should not modify resources)
        safe_methods = {
            HTTPMethod.GET,
            HTTPMethod.HEAD,
            HTTPMethod.OPTIONS,
        }

        # Unsafe methods (may modify resources)
        unsafe_methods = {
            HTTPMethod.POST,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
            HTTPMethod.PATCH,
        }

        # Note: TRACE and CONNECT are special cases not categorized here

        for method in safe_methods:
            assert method.value in ["GET", "HEAD", "OPTIONS"]

        for method in unsafe_methods:
            assert method.value in ["POST", "PUT", "DELETE", "PATCH"]

    def test_idempotent_methods(self):
        """Test identification of idempotent HTTP methods."""
        # Idempotent methods (multiple identical requests same as single request)
        idempotent = {
            HTTPMethod.GET,
            HTTPMethod.HEAD,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
            HTTPMethod.OPTIONS,
        }

        # Non-idempotent methods
        non_idempotent = {HTTPMethod.POST, HTTPMethod.PATCH}

        for method in idempotent:
            assert method.value in ["GET", "HEAD", "PUT", "DELETE", "OPTIONS"]

        for method in non_idempotent:
            assert method.value in ["POST", "PATCH"]

        """Test that enum members cannot be deleted."""
        # Enums don't allow deleting members
        with pytest.raises(AttributeError):
            del HTTPStatus.OK


class TestHTTPStatusEdgeCases:
    """Test edge cases and special scenarios for HTTPStatus."""

    def test_teapot_status_code(self):
        """Test the humorous 418 I'm a teapot status code."""
        assert HTTPStatus.IM_A_TEAPOT.value == 418

    def test_status_code_with_underscores(self):
        """Test status codes with long names containing underscores."""
        assert HTTPStatus.NON_AUTHORITATIVE_INFORMATION.value == 203
        assert HTTPStatus.PROXY_AUTHENTICATION_REQUIRED.value == 407
        assert HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE.value == 431

    def test_multiple_ways_to_access_same_status(self):
        """Test accessing the same status code in different ways."""
        # By name
        status1 = HTTPStatus.OK

        # By value
        status2 = HTTPStatus(200)

        # By string name
        status3 = HTTPStatus["OK"]

        assert status1 == status2 == status3
        assert status1 is status2 is status3

    def test_status_code_hash_consistency(self):
        """Test that enum members have consistent hashes."""
        status1 = HTTPStatus.OK
        status2 = HTTPStatus.OK

        assert hash(status1) == hash(status2)
        assert status1 is status2

    def test_status_code_in_dict_keys(self):
        """Test using status codes as dictionary keys."""
        status_dict = {
            HTTPStatus.OK: "Success",
            HTTPStatus.NOT_FOUND: "Not Found",
            HTTPStatus.INTERNAL_SERVER_ERROR: "Server Error",
        }

        assert status_dict[HTTPStatus.OK] == "Success"
        assert status_dict[HTTPStatus(404)] == "Not Found"
        assert status_dict[HTTPStatus["INTERNAL_SERVER_ERROR"]] == "Server Error"

    def test_status_code_in_set(self):
        """Test using status codes in sets."""
        success_codes = {
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.NO_CONTENT,
        }

        assert HTTPStatus.OK in success_codes
        assert HTTPStatus.NOT_FOUND not in success_codes
        assert len(success_codes) == 3


class TestHTTPMethodEdgeCases:
    """Test edge cases and special scenarios for HTTPMethod."""

    def test_multiple_ways_to_access_same_method(self):
        """Test accessing the same method in different ways."""
        # By name
        method1 = HTTPMethod.GET

        # By value
        method2 = HTTPMethod("GET")

        # By string name
        method3 = HTTPMethod["GET"]

        assert method1 == method2 == method3
        assert method1 is method2 is method3

    def test_method_hash_consistency(self):
        """Test that enum members have consistent hashes."""
        method1 = HTTPMethod.GET
        method2 = HTTPMethod.GET

        assert hash(method1) == hash(method2)
        assert method1 is method2

    def test_method_in_dict_keys(self):
        """Test using methods as dictionary keys."""
        method_dict = {
            HTTPMethod.GET: "Retrieve",
            HTTPMethod.POST: "Create",
            HTTPMethod.DELETE: "Remove",
        }

        assert method_dict[HTTPMethod.GET] == "Retrieve"
        assert method_dict[HTTPMethod("POST")] == "Create"
        assert method_dict[HTTPMethod["DELETE"]] == "Remove"

    def test_method_in_set(self):
        """Test using methods in sets."""
        crud_methods = {
            HTTPMethod.GET,
            HTTPMethod.POST,
            HTTPMethod.PUT,
            HTTPMethod.DELETE,
        }

        assert HTTPMethod.GET in crud_methods
        assert HTTPMethod.OPTIONS not in crud_methods
        assert len(crud_methods) == 4

    def test_method_case_sensitivity(self):
        """Test that method values are case-sensitive."""
        assert HTTPMethod.GET.value == "GET"

        # Lowercase version should raise ValueError
        with pytest.raises(ValueError):
            HTTPMethod("get")


class TestEnumsIntegration:
    """Integration tests for enums with realistic use cases."""

    def test_status_code_and_method_combination(self):
        """Test combining status codes and methods in realistic scenarios."""
        # Successful GET request
        method = HTTPMethod.GET
        status = HTTPStatus.OK
        assert method.value == "GET"
        assert status.value == 200

        # Resource creation with POST
        method = HTTPMethod.POST
        status = HTTPStatus.CREATED
        assert method.value == "POST"
        assert status.value == 201

        # Resource not found with GET
        method = HTTPMethod.GET
        status = HTTPStatus.NOT_FOUND
        assert method.value == "GET"
        assert status.value == 404

    def test_building_http_response_mapping(self):
        """Test building a response mapping with enums."""
        response_map = {
            (HTTPMethod.GET, HTTPStatus.OK): ("Resource retrieved successfully"),
            (HTTPMethod.POST, HTTPStatus.CREATED): ("Resource created successfully"),
            (HTTPMethod.DELETE, HTTPStatus.NO_CONTENT): (
                "Resource deleted successfully"
            ),
            (HTTPMethod.GET, HTTPStatus.NOT_FOUND): "Resource not found",
        }

        # Test accessing the map
        key1 = (HTTPMethod.GET, HTTPStatus.OK)
        assert response_map[key1] == "Resource retrieved successfully"

        key2 = (HTTPMethod.POST, HTTPStatus.CREATED)
        assert response_map[key2] == "Resource created successfully"

    def test_http_method_routing(self):
        """Test using HTTP methods for routing logic."""
        allowed_methods = {
            HTTPMethod.GET,
            HTTPMethod.POST,
            HTTPMethod.PUT,
        }

        assert HTTPMethod.GET in allowed_methods
        assert HTTPMethod.DELETE not in allowed_methods

    def test_status_code_categorization(self):
        """Test categorizing status codes by type."""

        def is_success(status: HTTPStatus) -> bool:
            return 200 <= status.value < 300

        def is_client_error(status: HTTPStatus) -> bool:
            return 400 <= status.value < 500

        def is_server_error(status: HTTPStatus) -> bool:
            return 500 <= status.value < 600

        assert is_success(HTTPStatus.OK)
        assert is_success(HTTPStatus.CREATED)
        assert not is_success(HTTPStatus.NOT_FOUND)

        assert is_client_error(HTTPStatus.BAD_REQUEST)
        assert is_client_error(HTTPStatus.UNAUTHORIZED)
        assert not is_client_error(HTTPStatus.OK)

        assert is_server_error(HTTPStatus.INTERNAL_SERVER_ERROR)
        assert is_server_error(HTTPStatus.BAD_GATEWAY)
        assert not is_server_error(HTTPStatus.NOT_FOUND)
