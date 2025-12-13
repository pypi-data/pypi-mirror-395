# Recursor SDK (Python)

[![PyPI version](https://badge.fury.io/py/recursor-sdk.svg)](https://badge.fury.io/py/recursor-sdk)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Complete Python SDK for interacting with the Recursor API. Provides authentication, project management, real-time updates via WebSocket, and full access to all platform features.

## Installation

```bash
pip install recursor-sdk
```

Or build from source:

```bash
cd sdk/python
python -m pip install build
python -m build
pip install dist/recursor_sdk-*.whl
```

## Quick Start

### Basic Usage

```python
from recursor_sdk import RecursorSDK

sdk = RecursorSDK(base_url="https://api.recursor.dev/api/v1")

# Check health
healthy = sdk.check_health()
print(f"API is healthy: {healthy}")
```

### Authentication

```python
# Register a new user
user = sdk.register(
    email="user@example.com",
    password="SecurePass123",
    username="johndoe",
    full_name="John Doe"
)

# Login
response = sdk.login("user@example.com", "SecurePass123")
# Access token is automatically set for future requests

# Get user profile
profile = sdk.get_profile()
print(f"User: {profile['email']}")

# Update profile
updated = sdk.update_profile(full_name="John Smith")

# Change password
sdk.change_password("SecurePass123", "NewSecurePass456")
```

### Project Management

```python
# Create a project
project = sdk.create_project(
    name="My Project",
    organization_id="org-123",
    description="Project description"
)

# Get project
project_details = sdk.get_project(project["id"])

# List projects
projects = sdk.list_projects("org-123")

# Get MCP configuration
mcp_config = sdk.get_mcp_config(project["id"])
print(f"MCP Config: {mcp_config}")

# Regenerate API key
api_key_response = sdk.regenerate_project_api_key(project["id"])

# Update project
updated = sdk.update_project(
    project["id"],
    name="Updated Project Name",
    description="New description"
)

# Delete project
sdk.delete_project(project["id"])
```

### Organizations & Teams

```python
# Create organization
org = sdk.create_organization(
    name="My Organization",
    description="Organization description"
)

# List organizations
orgs = sdk.list_organizations()

# Add member
sdk.add_member_to_organization(org["id"], "user-123")

# Remove member
sdk.remove_member_from_organization(org["id"], "user-123")
```

### Corrections

```python
# Create correction
correction = sdk.create_correction(
    input_text="incorrect code",
    output_text="correct code",
    expected_output="correct code",
    context={"explanation": "Fix bug"},
    correction_type="bug"
)

# List corrections
result = sdk.list_corrections(page=1, page_size=50)
corrections = result.get("corrections", [])

# Search corrections
results = sdk.search_corrections("authentication", limit=10)

# Get correction
correction_details = sdk.get_correction(correction["id"])

# Update correction
updated = sdk.update_correction(
    correction["id"],
    {"context": {"explanation": "Updated explanation"}}
)

# Get statistics
stats = sdk.get_correction_stats()
```

### Code Intelligence

```python
# Detect intent
intent = sdk.detect_intent(
    user_request="Add error handling to login",
    current_file="auth.py",
    tags=["error-handling"]
)

# Get intent history
history = sdk.get_intent_history(limit=50)

# Correct code
result = sdk.correct_code("def func(): pass", "python")

# Get analytics
dashboard = sdk.get_analytics_dashboard("user-123", period="30d")
time_saved = sdk.get_time_saved("user-123", period="30d")
quality = sdk.get_quality_metrics("user-123", period="30d")
```

### Billing & Usage

```python
# Get current usage
usage = sdk.get_usage()
print(f"API Calls: {usage['api_calls']['used']} / {usage['api_calls']['limit']}")

# Get usage history
history = sdk.get_usage_history(days=30, resource_type="api_call")

# List billing plans
plans = sdk.list_billing_plans()

# Get subscription
subscription = sdk.get_subscription()
```

### Notifications

```python
# List notifications
notifications = sdk.list_notifications()

# Mark as read
sdk.mark_notification_as_read("notification-123")

# Mark all as read
sdk.mark_all_notifications_as_read()

# Delete notification
sdk.delete_notification("notification-123")
```

### Settings

```python
# Get settings
settings = sdk.get_settings()

# Update account
sdk.update_account(full_name="John Smith", email="newemail@example.com")

# Update preferences
sdk.update_preferences({"theme": "dark", "notifications": True})

# Get guidelines
guidelines = sdk.get_guidelines()
```

### WebSocket (Real-time Updates)

```python
import asyncio
from recursor_sdk import RecursorSDK

async def main():
    sdk = RecursorSDK(base_url="https://api.recursor.dev/api/v1")
    
    # Login first to get access token
    sdk.login("user@example.com", "password")
    
    # Create and connect WebSocket
    ws = await sdk.connect_websocket()
    
    # Subscribe to events
    def on_notification(data):
        print(f"New notification: {data}")
    
    def on_usage(data):
        print(f"Usage updated: {data}")
    
    ws.on("notification.new", on_notification)
    ws.on("usage.updated", on_usage)
    
    # Keep connection alive
    await asyncio.sleep(60)
    
    # Disconnect when done
    await sdk.disconnect_websocket()

asyncio.run(main())
```

### Gateway Endpoints

```python
# LLM Gateway
policy = sdk.get_llm_gateway_policy()
chat_response = sdk.gateway_chat(
    messages=[{"role": "user", "content": "Hello!"}],
    provider="openai",
    model="gpt-4",
    call_provider=True
)

# Robotics Gateway
robotics_policy = sdk.get_robotics_gateway_policy()
robotics_result = sdk.robotics_gateway_observe(
    state={"position": [0, 0, 0]},
    command={"action": "move"}
)

# AV Gateway
av_policy = sdk.get_av_gateway_policy()
av_result = sdk.av_gateway_observe(
    sensors={"camera": "data"},
    state={"speed": 60},
    action={"brake": False},
    timestamp=int(time.time()),
    vehicle_id="vehicle-123"
)
```

## Environment Variables

- `RECURSOR_API_URL` - API base URL (default: `http://localhost:8000/api/v1`)
- `RECURSOR_API_KEY` - API key for authentication
- `RECURSOR_ACCESS_TOKEN` - Access token for authentication

## API Reference

### Authentication Methods
- `register(email, password, username, full_name=None)` - Register new user
- `login(email, password)` - Login and get access token
- `logout()` - Logout current user
- `refresh_token(refresh_token)` - Refresh access token
- `get_profile()` - Get user profile
- `update_profile(full_name=None, username=None)` - Update user profile
- `change_password(current_password, new_password)` - Change password
- `generate_api_key()` - Generate API key
- `revoke_api_key()` - Revoke API key
- `get_password_requirements()` - Get password requirements

### Project Methods
- `create_project(name, organization_id, description=None, settings=None)` - Create project
- `get_project(project_id)` - Get project
- `list_projects(organization_id=None)` - List projects
- `update_project(project_id, name=None, description=None, settings=None, is_active=None)` - Update project
- `delete_project(project_id)` - Delete project
- `regenerate_project_api_key(project_id)` - Regenerate API key
- `get_mcp_config(project_id)` - Get MCP configuration
- `get_mcp_stats(project_id)` - Get MCP statistics

### Organization Methods
- `create_organization(name, description=None)` - Create organization
- `list_organizations()` - List organizations
- `get_organization(org_id)` - Get organization
- `update_organization(org_id, name=None, description=None)` - Update organization
- `add_member_to_organization(org_id, user_id)` - Add member
- `remove_member_from_organization(org_id, user_id)` - Remove member

### Correction Methods
- `create_correction(input_text, output_text, expected_output=None, context=None, correction_type=None, organization_id=None)` - Create correction
- `list_corrections(page=1, page_size=50, include_inactive=False, organization_id=None)` - List corrections
- `search_corrections(query, limit=10, organization_id=None)` - Search corrections
- `get_correction(correction_id)` - Get correction
- `update_correction(correction_id, updates)` - Update correction
- `get_correction_stats()` - Get statistics

### Code Intelligence Methods
- `detect_intent(user_request, current_file=None, user_id=None, project_id=None, tags=None, similar_limit=5, organization_id=None)` - Detect intent
- `get_intent_history(limit=50, project_id=None)` - Get intent history
- `correct_code(code, language, project_profile=None)` - Correct code
- `correct_config(config, config_type)` - Correct config
- `correct_documentation(markdown, doc_type="README")` - Correct documentation
- `apply_auto_corrections(user_id, model_name, corrections)` - Apply auto corrections
- `get_trust_score(user_id, model_name)` - Get trust score
- `submit_feedback(prediction_id, accepted)` - Submit feedback
- `get_auto_correct_stats(user_id)` - Get auto correction stats
- `get_patterns(user_id=None)` - Get patterns
- `get_analytics_dashboard(user_id, period="30d", project_id=None)` - Get analytics dashboard
- `get_time_saved(user_id, period="30d", project_id=None)` - Get time saved metrics
- `get_quality_metrics(user_id, period="30d", project_id=None)` - Get quality metrics
- `get_ai_agent_metrics(user_id, project_id=None)` - Get AI agent metrics

### Billing Methods
- `get_usage()` - Get current usage
- `get_usage_history(days=30, resource_type=None)` - Get usage history
- `list_billing_plans()` - List billing plans
- `get_subscription()` - Get subscription

### Notification Methods
- `list_notifications()` - List notifications
- `mark_notification_as_read(notification_id)` - Mark as read
- `mark_all_notifications_as_read()` - Mark all as read
- `delete_notification(notification_id)` - Delete notification

### Settings Methods
- `get_settings()` - Get settings
- `update_account(full_name=None, email=None)` - Update account
- `update_preferences(preferences)` - Update preferences
- `get_guidelines()` - Get guidelines
- `change_password_via_settings(current_password, new_password)` - Change password
- `delete_account()` - Delete account

### Activity Methods
- `list_activity_logs(page=1, page_size=50)` - List activity logs
- `export_activity_logs()` - Export activity logs (returns bytes)

### WebSocket Methods
- `create_websocket()` - Create WebSocket client
- `connect_websocket()` - Connect WebSocket (async)
- `disconnect_websocket()` - Disconnect WebSocket (async)

### Gateway Methods
- `get_llm_gateway_policy()` - Get LLM gateway policy
- `gateway_chat(messages, provider="openai", model=None, call_provider=False, user_id=None, organization_id=None)` - LLM gateway chat
- `get_robotics_gateway_policy()` - Get robotics gateway policy
- `robotics_gateway_observe(state, command=None, environment=None, user_id=None, organization_id=None)` - Robotics gateway observe
- `get_av_gateway_policy()` - Get AV gateway policy
- `av_gateway_observe(sensors, state, action, timestamp, vehicle_id, user_id=None, organization_id=None)` - AV gateway observe

## Error Handling

The SDK raises exceptions for failed requests:

```python
try:
    sdk.login("wrong", "wrong")
except Exception as e:
    print(f"Login failed: {e}")
    # HTTPStatusError: 401 Unauthorized
```

## Type Hints

Full type hints included for better IDE support and type checking.

## License

MIT License. See `LICENSE` file.
