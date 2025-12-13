# /user_profiler/agenticmem/agenticmem_client
Description: Python SDK for remote async access to AgenticMem API

## Main Entry Points

- **Client**: `agenticmem/client.py` - `AgenticMemClient`
- **Utils**: `agenticmem/client_utils.py` - Helper utilities

## Purpose

1. **Remote API access** - Async SDK for applications to call AgenticMem backend
2. **Authentication** - Handle login and Bearer token management
3. **Type-safe interface** - Auto-parsing responses into Pydantic models

## API Methods

**Authentication:**
- `login(email, password)` - Get auth token

**Publishing:**
- `publish_interaction(request_id, user_id, interactions, source, agent_version)` - Publish interactions (triggers profile/feedback/evaluation)

**Profiles:**
- `search_profiles(request)` - Semantic search
- `get_profiles(request)` - Get all for user
- `delete_profile(user_id, profile_id, search_query)` - Delete profiles
- `get_profile_change_log()` - Get history

**Interactions:**
- `search_interactions(request)` - Semantic search
- `get_interactions(request)` - Get all for user
- `delete_interaction(user_id, interaction_id)` - Delete interaction

**Feedback:**
- `get_raw_feedbacks(request)` - Raw feedback from interactions
- `get_feedbacks(request)` - Aggregated feedback with status

**Configuration:**
- `set_config(config)` - Update org config (extractors, evaluators, storage)
- `get_config()` - Get current config

## Architecture Pattern

- **All async** - Uses `aiohttp` for HTTP requests
- **Type-safe** - Pydantic models from `agenticmem_commons`
- **Auto-parsing** - Responses → Pydantic models
- **Flexible input** - Accepts Pydantic models or dicts
- **Bearer auth** - Automatic token handling
