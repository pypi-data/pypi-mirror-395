"""
Test the SDK endpoints.
"""

from unittest.mock import Mock


def test_get_management_info(mock_session, client):
    """Test get_management_info functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"status": "ok"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.get_management_info()

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/",
        json=None,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_users(mock_session, client):
    """Test list_users functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.list_users(page=2, query="test", per_page=20)

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/users",
        json=None,
        params={"page": 2, "query": "test", "per_page": 20},
        timeout=(5, 30),
    )
    assert response == mock_response


def test_create_user(mock_session, client):
    """Test create_user functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"uuid": "test-uuid", "email": "test@example.com"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.create_user(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        roles=["role1", "role2"],
        custom_claims={"company": "Test Corp"},
        mark_as_verified=True,
    )

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://api.fauthy.com/v1/management/users",
        json={
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "roles": ["role1", "role2"],
            "custom_claims": {"company": "Test Corp"},
            "mark_as_verified": True,
        },
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_get_user(mock_session, client):
    """Test get_user functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"uuid": "test-uuid", "email": "test@example.com"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.get_user("test-uuid")

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/users/test-uuid",
        json=None,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_update_user(mock_session, client):
    """Test update_user functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        "uuid": "test-uuid",
        "email": "updated@example.com",
    }
    mock_session.request.return_value = mock_response

    # Make request
    response = client.update_user(
        user_id="test-uuid",
        email="updated@example.com",
        first_name="Jane",
        last_name="Smith",
    )

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://api.fauthy.com/v1/management/users/test-uuid",
        json={
            "email": "updated@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
        },
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_update_user_partial(mock_session, client):
    """Test update_user with only some fields."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"uuid": "test-uuid", "first_name": "Jane"}
    mock_session.request.return_value = mock_response

    # Make request with only first_name
    response = client.update_user(user_id="test-uuid", first_name="Jane")

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="PUT",
        url="https://api.fauthy.com/v1/management/users/test-uuid",
        json={"first_name": "Jane"},
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_delete_user(mock_session, client):
    """Test delete_user functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.status_code = 204
    mock_session.request.return_value = mock_response

    # Make request
    response = client.delete_user("test-uuid")

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="DELETE",
        url="https://api.fauthy.com/v1/management/users/test-uuid",
        json=None,
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_set_user_password(mock_session, client):
    """Test set_user_password functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"uuid": "test-uuid", "email": "test@example.com"}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.set_user_password("test-uuid", "newpassword123")

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="POST",
        url="https://api.fauthy.com/v1/management/users/test-uuid/password",
        json={"password": "newpassword123"},
        params=None,
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_roles(mock_session, client):
    """Test list_roles functionality."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request
    response = client.list_roles(page=2, n_per_page=50)

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/roles",
        json=None,
        params={"page": 2, "n_per_page": 50},
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_roles_default_params(mock_session, client):
    """Test list_roles with default parameters."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request with defaults
    response = client.list_roles()

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/roles",
        json=None,
        params={"page": 1},
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_users_with_custom_claims_filter(mock_session, client):
    """Test list_users with custom claims filtering."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request with custom claims filter
    custom_claims = {"company": "Test Corp", "department": "Engineering"}
    response = client.list_users(
        page=1, query="test", per_page=20, custom_claims_filter=custom_claims
    )

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/users",
        json=None,
        params={
            "page": 1,
            "query": "test",
            "per_page": 20,
            "claim_company": "Test Corp",
            "claim_department": "Engineering",
        },
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_users_with_single_custom_claim_filter(mock_session, client):
    """Test list_users with a single custom claim filter."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request with single custom claim filter
    custom_claims = {"role": "admin"}
    response = client.list_users(custom_claims_filter=custom_claims)

    # Verify request was made correctly
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/users",
        json=None,
        params={"page": 1, "query": "", "per_page": 10, "claim_role": "admin"},
        timeout=(5, 30),
    )
    assert response == mock_response


def test_list_users_without_custom_claims_filter(mock_session, client):
    """Test list_users without custom claims filter (should not add claim_ params)."""
    # Setup mock response
    mock_response = Mock()
    mock_response.json.return_value = {"items": [], "total": 0, "page": 1}
    mock_session.request.return_value = mock_response

    # Make request without custom claims filter
    response = client.list_users(page=2, query="test", per_page=20)

    # Verify request was made correctly (no claim_ parameters)
    mock_session.request.assert_called_once_with(
        method="GET",
        url="https://api.fauthy.com/v1/management/users",
        json=None,
        params={"page": 2, "query": "test", "per_page": 20},
        timeout=(5, 30),
    )
    assert response == mock_response
