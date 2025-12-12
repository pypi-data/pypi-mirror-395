# Fauthy Python SDK

A Python SDK for interacting with the Fauthy API.

## Installation

```bash
pip install fauthy-python-sdk
```

## Usage

### Basic Setup

```python
from fauthy_sdk import FauthyClient

# Initialize the client
client = FauthyClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
```

### Management API

The SDK provides access to the Fauthy Management API v1 endpoints.

#### Get Management Info

```python
response = client.get_management_info()
print(response.json())
```

#### List Users

```python
# Basic listing
response = client.list_users()

# With pagination and search
response = client.list_users(
    page=1,
    query="john",
    per_page=20
)

# With custom claims filtering
custom_claims = {
    "company": "Test Corp",
    "department": "Engineering"
}
response = client.list_users(
    page=1,
    query="",
    per_page=10,
    custom_claims_filter=custom_claims
)
```

#### Create User

```python
response = client.create_user(
    email="user@example.com",
    first_name="John",
    last_name="Doe",
    roles=["role_uuid_1", "role_uuid_2"],
    custom_claims={
        "company": "Test Corp",
        "department": "Engineering"
    },
    mark_as_verified=True
)
```

#### Get User

```python
response = client.get_user("user_uuid")
```

#### Update User

```python
response = client.update_user(
    user_id="user_uuid",
    first_name="Jane",
    last_name="Smith",
    email="jane@example.com"
)
```

#### Delete User

```python
response = client.delete_user("user_uuid")
```

#### Set User Password

```python
response = client.set_user_password(
    user_id="user_uuid",
    password="new_secure_password"
)
```

#### List Roles

```python
# Basic listing
response = client.list_roles()

# With pagination
response = client.list_roles(
    page=1,
    n_per_page=50
)
```

## Custom Claims Filtering

The SDK supports filtering users by custom claims using the `custom_claims_filter` parameter in the `list_users` method. This allows you to filter users based on their custom JWT claims.

### Example

```python
# Filter users by company and department
custom_claims = {
    "company": "Test Corp",
    "department": "Engineering"
}

response = client.list_users(
    page=1,
    per_page=20,
    custom_claims_filter=custom_claims
)
```

This will send a request with query parameters like:
- `claim_company=Test Corp`
- `claim_department=Engineering`

The API will return only users whose custom claims match these values.

## Error Handling

The SDK raises `requests.exceptions.RequestException` for HTTP errors. You can handle these exceptions to manage API errors:

```python
import requests

try:
    response = client.get_user("user_uuid")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
```

## Response Format

All methods return a `requests.Response` object. You can access the JSON data using:

```python
response = client.list_users()
data = response.json()
print(f"Total users: {data['total']}")
print(f"Users: {data['items']}")
```