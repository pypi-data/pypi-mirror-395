"""
Fauthy SDK Management Mixin

This module provides a mixin for Fauthy management API endpoints.
"""

from typing import Any, Dict, List, Optional

import requests


class ManagementMixin:
    """Mixin class for Fauthy management API endpoints."""

    def get_management_info(self) -> requests.Response:
        """
        Get management info, use as ping endpoint.

        Returns:
            requests.Response: The API response containing management information
        """
        return self._make_request("GET", "")

    def list_users(
        self,
        page: int = 1,
        query: str = "",
        per_page: int = 10,
        custom_claims_filter: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """
        List users for the tenant with pagination and search.

        Args:
            page (int): Page number (default: 1)
            query (str): Search query (default: "")
            per_page (int): Items per page, between 1 and 100 (default: 10)
            custom_claims_filter (Optional[Dict[str, str]]): Filter by custom claims.
                Keys should be claim names, values should be claim values.
                Example: {"company": "Test Corp", "department": "Engineering"}

        Returns:
            requests.Response: The API response containing paginated user list
        """
        params = {
            "page": page,
            "query": query,
            "per_page": per_page,
        }

        # Add custom claims filters if provided
        if custom_claims_filter:
            for claim_name, claim_value in custom_claims_filter.items():
                params[f"claim_{claim_name}"] = claim_value

        return self._make_request("GET", "users", params=params)

    def create_user(
        self,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        roles: Optional[List[str]] = None,
        custom_claims: Optional[Dict[str, Any]] = None,
        mark_as_verified: bool = False,
    ) -> requests.Response:
        """
        Create a new user for the tenant.

        Args:
            email (str): User's email address
            first_name (Optional[str]): User's first name
            last_name (Optional[str]): User's last name
            roles (Optional[List[str]]): List of role UUIDs
            custom_claims (Optional[Dict[str, Any]]): Custom JWT claims
            mark_as_verified (bool): Mark user as verified using MANUAL verification method (default: False)

        Returns:
            requests.Response: The API response containing the created user
        """
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "roles": roles or [],
            "custom_claims": custom_claims or {},
            "mark_as_verified": mark_as_verified,
        }
        return self._make_request("POST", "users", data=data)

    def get_user(self, user_id: str) -> requests.Response:
        """
        Get a specific user by ID.

        Args:
            user_id (str): The UUID of the user to retrieve

        Returns:
            requests.Response: The API response containing the user data
        """
        return self._make_request("GET", f"users/{user_id}")

    def update_user(
        self,
        user_id: str,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        roles: Optional[List[str]] = None,
        custom_claims: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Update a user.

        Args:
            user_id (str): The UUID of the user to update
            email (Optional[str]): User's email address
            first_name (Optional[str]): User's first name
            last_name (Optional[str]): User's last name
            roles (Optional[List[str]]): List of role UUIDs
            custom_claims (Optional[Dict[str, Any]]): Custom JWT claims

        Returns:
            requests.Response: The API response containing the updated user
        """
        data = {}
        if email is not None:
            data["email"] = email
        if first_name is not None:
            data["first_name"] = first_name
        if last_name is not None:
            data["last_name"] = last_name
        if roles is not None:
            data["roles"] = roles
        if custom_claims is not None:
            data["custom_claims"] = custom_claims

        return self._make_request("PUT", f"users/{user_id}", data=data)

    def delete_user(self, user_id: str) -> requests.Response:
        """
        Delete a user.

        Args:
            user_id (str): The UUID of the user to delete

        Returns:
            requests.Response: The API response (204 No Content on success)
        """
        return self._make_request("DELETE", f"users/{user_id}")

    def set_user_password(self, user_id: str, password: str) -> requests.Response:
        """
        Set a user's password.

        Args:
            user_id (str): The UUID of the user
            password (str): The new password

        Returns:
            requests.Response: The API response containing the updated user
        """
        data = {"password": password}
        return self._make_request("POST", f"users/{user_id}/password", data=data)

    def list_roles(
        self,
        page: int = 1,
        n_per_page: Optional[int] = None,
    ) -> requests.Response:
        """
        List roles for the tenant with pagination.

        Args:
            page (int): Page number (1-based, default: 1)
            n_per_page (Optional[int]): Number of items per page, between 1 and 250

        Returns:
            requests.Response: The API response containing paginated role list
        """
        params = {"page": page}
        if n_per_page is not None:
            params["n_per_page"] = n_per_page
        return self._make_request("GET", "roles", params=params)
