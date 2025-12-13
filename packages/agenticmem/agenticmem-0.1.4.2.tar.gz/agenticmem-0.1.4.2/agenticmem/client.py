import os
import aiohttp
import asyncio
from urllib.parse import urljoin
import requests
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Union
from agenticmem_commons.api_schema.retriever_schema import (
    SearchInteractionRequest,
    SearchInteractionResponse,
    SearchUserProfileRequest,
    SearchUserProfileResponse,
    GetInteractionsRequest,
    GetInteractionsResponse,
    GetUserProfilesRequest,
    GetUserProfilesResponse,
    GetRawFeedbacksRequest,
    GetRawFeedbacksResponse,
    GetFeedbacksRequest,
    GetFeedbacksResponse,
    GetRequestsRequest,
    GetRequestsResponse,
    GetAgentSuccessEvaluationResultsRequest,
    GetAgentSuccessEvaluationResultsResponse,
)

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

IS_TEST_ENV = os.environ.get("IS_TEST_ENV", "false").strip() == "true"

if IS_TEST_ENV:
    BACKEND_URL = "http://127.0.0.1:8000"  # Local server for testing
else:
    BACKEND_URL = "http://agenticmem-test.us-west-2.elasticbeanstalk.com:8081"  # Elastic Beanstalk server url

from agenticmem_commons.api_schema.service_schemas import (
    InteractionData,
    ProfileChangeLogResponse,
    PublishUserInteractionRequest,
    PublishUserInteractionResponse,
    DeleteUserProfileRequest,
    DeleteUserProfileResponse,
    DeleteUserInteractionRequest,
    DeleteUserInteractionResponse,
    DeleteRequestRequest,
    DeleteRequestResponse,
    DeleteRequestGroupRequest,
    DeleteRequestGroupResponse,
)
from agenticmem_commons.api_schema.login_schema import Token
from agenticmem_commons.config_schema import Config
from .cache import InMemoryCache


class AgenticMemClient:
    """Client for interacting with the AgenticMem API."""

    # Shared thread pool for all instances to maximize efficiency
    _thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="agenticmem")

    def __init__(self, api_key: str = "", url_endpoint: str = ""):
        """Initialize the AgenticMem client.

        Args:
            api_key (str): Your API key for authentication
        """
        self.api_key = api_key
        self.base_url = url_endpoint if url_endpoint else BACKEND_URL
        self.session = requests.Session()
        self._cache = InMemoryCache()

    def _get_auth_headers(self) -> dict:
        """Get authentication headers for API requests.

        Returns:
            dict: Headers with authorization and content-type
        """
        if self.api_key:
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
        return {}

    def _convert_to_model(self, data: Union[dict, object], model_class):
        """Convert dict to model instance if needed.

        Args:
            data: Either a dict or already an instance of model_class
            model_class: The target class to convert to

        Returns:
            An instance of model_class
        """
        if isinstance(data, dict):
            return model_class(**data)
        return data

    def _fire_and_forget(self, sync_func, async_func, *args, **kwargs):
        """Execute a request in fire-and-forget mode.

        This method optimizes execution based on context:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            sync_func: Synchronous function to call
            async_func: Asynchronous function to call
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
        """
        try:
            loop = asyncio.get_running_loop()

            # We're in an async context - use the event loop
            async def fire_and_forget():
                try:
                    await async_func(*args, **kwargs)
                except Exception:
                    # Silently ignore errors in fire-and-forget mode
                    pass

            loop.create_task(fire_and_forget())
        except RuntimeError:
            # No running loop - we're in sync context, use thread pool
            def send_request():
                try:
                    sync_func(*args, **kwargs)
                except Exception:
                    # Silently ignore errors in fire-and-forget mode
                    pass

            self._thread_pool.submit(send_request)

    async def _make_async_request(
        self, method: str, endpoint: str, headers: Optional[dict] = None, **kwargs
    ):
        """Make an async HTTP request to the API."""
        url = urljoin(self.base_url, endpoint)

        # Merge auth headers with any provided headers
        request_headers = self._get_auth_headers()
        if headers:
            request_headers.update(headers)

        async with aiohttp.ClientSession() as async_session:
            response = await async_session.request(
                method, url, headers=request_headers, **kwargs
            )
            response.raise_for_status()
            return await response.json()

    def _make_request(
        self, method: str, endpoint: str, headers: Optional[dict] = None, **kwargs
    ):
        """Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, DELETE)
            endpoint (str): API endpoint
            headers (dict, optional): Additional headers to include in the request
            **kwargs: Additional arguments to pass to requests

        Returns:
            dict: API response
        """
        url = urljoin(self.base_url, endpoint)

        # Merge auth headers with any provided headers
        request_headers = self._get_auth_headers()
        if headers:
            request_headers.update(headers)

        self.session.headers.update(request_headers)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def login(self, email: str, password: str) -> Token:
        """Login to the AgenticMem API."""
        response = self._make_request(
            "POST",
            "/token",
            data={"username": email, "password": password},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "accept": "application/json",
            },
        )
        return Token(**response)

    def _publish_interaction_sync(
        self, request: PublishUserInteractionRequest
    ) -> PublishUserInteractionResponse:
        """Internal sync method to publish interaction."""
        response = self._make_request(
            "POST",
            "/api/publish_interaction",
            json=request.model_dump(),
        )
        return PublishUserInteractionResponse(**response)

    async def _publish_interaction_async(
        self, request: PublishUserInteractionRequest
    ) -> PublishUserInteractionResponse:
        """Internal async method to publish interaction."""
        response = await self._make_async_request(
            "POST",
            "/api/publish_interaction",
            json=request.model_dump(),
        )
        return PublishUserInteractionResponse(**response)

    def publish_interaction(
        self,
        user_id: str,
        interactions: list[Union[InteractionData, dict]],
        source: str = "",
        agent_version: str = "",
        request_group: Optional[str] = None,
        wait_for_response: bool = False,
    ) -> Optional[PublishUserInteractionResponse]:
        """Publish user interactions.

        This method is optimized for resource efficiency:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            user_id (str): The user ID
            interactions (List[InteractionData]): List of interaction data
            source (str, optional): The source of the interaction
            agent_version (str, optional): The agent version
            request_group (Optional[str], optional): The request group. Defaults to None.
            wait_for_response (bool, optional): If True, wait for response. If False, send request without waiting. Defaults to False.
        Returns:
            Optional[PublishUserInteractionResponse]: Response containing success status and message if wait_for_response=True, None otherwise
        """
        interaction_data_list = [
            (
                InteractionData(**interaction_request)
                if isinstance(interaction_request, dict)
                else interaction_request
            )
            for interaction_request in interactions
        ]
        request = PublishUserInteractionRequest(
            request_group=request_group,
            user_id=user_id,
            interaction_data_list=interaction_data_list,
            source=source,
            agent_version=agent_version,
        )

        if wait_for_response:
            # Synchronous blocking call
            return self._publish_interaction_sync(request)
        else:
            # Non-blocking fire-and-forget
            self._fire_and_forget(
                self._publish_interaction_sync, self._publish_interaction_async, request
            )
            return None

    def search_interactions(
        self,
        request: Union[SearchInteractionRequest, dict],
    ) -> SearchInteractionResponse:
        """Search for user interactions.

        Args:
            request (SearchInteractionRequest): The search request

        Returns:
            SearchInteractionResponse: Response containing matching interactions
        """
        request = self._convert_to_model(request, SearchInteractionRequest)
        response = self._make_request(
            "POST",
            "/api/search_interactions",
            json=request.model_dump(),
        )
        return SearchInteractionResponse(**response)

    def search_profiles(
        self,
        request: Union[SearchUserProfileRequest, dict],
    ) -> SearchUserProfileResponse:
        """Search for user profiles.

        Args:
            request (SearchUserProfileRequest): The search request

        Returns:
            SearchUserProfileResponse: Response containing matching profiles
        """
        request = self._convert_to_model(request, SearchUserProfileRequest)
        response = self._make_request(
            "POST", "/api/search_profiles", json=request.model_dump()
        )
        return SearchUserProfileResponse(**response)

    def _delete_profile_sync(
        self, request: DeleteUserProfileRequest
    ) -> DeleteUserProfileResponse:
        """Internal sync method to delete profile."""
        response = self._make_request(
            "DELETE",
            "/api/delete_profile",
            json=request.model_dump(),
        )
        return DeleteUserProfileResponse(**response)

    async def _delete_profile_async(
        self, request: DeleteUserProfileRequest
    ) -> DeleteUserProfileResponse:
        """Internal async method to delete profile."""
        response = await self._make_async_request(
            "DELETE",
            "/api/delete_profile",
            json=request.model_dump(),
        )
        return DeleteUserProfileResponse(**response)

    def delete_profile(
        self,
        user_id: str,
        profile_id: str = "",
        search_query: str = "",
        wait_for_response: bool = False,
    ) -> Optional[DeleteUserProfileResponse]:
        """Delete user profiles.

        This method is optimized for resource efficiency:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            user_id (str): The user ID
            profile_id (str, optional): Specific profile ID to delete
            search_query (str, optional): Query to match profiles for deletion
            wait_for_response (bool, optional): If True, wait for response. If False, send request without waiting. Defaults to False.

        Returns:
            Optional[DeleteUserProfileResponse]: Response containing success status and message if wait_for_response=True, None otherwise
        """
        request = DeleteUserProfileRequest(
            user_id=user_id,
            profile_id=profile_id,
            search_query=search_query,
        )

        if wait_for_response:
            # Synchronous blocking call
            return self._delete_profile_sync(request)
        else:
            # Non-blocking fire-and-forget
            self._fire_and_forget(
                self._delete_profile_sync, self._delete_profile_async, request
            )
            return None

    def _delete_interaction_sync(
        self, request: DeleteUserInteractionRequest
    ) -> DeleteUserInteractionResponse:
        """Internal sync method to delete interaction."""
        response = self._make_request(
            "DELETE",
            "/api/delete_interaction",
            json=request.model_dump(),
        )
        return DeleteUserInteractionResponse(**response)

    async def _delete_interaction_async(
        self, request: DeleteUserInteractionRequest
    ) -> DeleteUserInteractionResponse:
        """Internal async method to delete interaction."""
        response = await self._make_async_request(
            "DELETE",
            "/api/delete_interaction",
            json=request.model_dump(),
        )
        return DeleteUserInteractionResponse(**response)

    def delete_interaction(
        self, user_id: str, interaction_id: str, wait_for_response: bool = False
    ) -> Optional[DeleteUserInteractionResponse]:
        """Delete a user interaction.

        This method is optimized for resource efficiency:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            user_id (str): The user ID
            interaction_id (str): The interaction ID to delete
            wait_for_response (bool, optional): If True, wait for response. If False, send request without waiting. Defaults to False.

        Returns:
            Optional[DeleteUserInteractionResponse]: Response containing success status and message if wait_for_response=True, None otherwise
        """
        request = DeleteUserInteractionRequest(
            user_id=user_id, interaction_id=interaction_id
        )

        if wait_for_response:
            # Synchronous blocking call
            return self._delete_interaction_sync(request)
        else:
            # Non-blocking fire-and-forget
            self._fire_and_forget(
                self._delete_interaction_sync, self._delete_interaction_async, request
            )
            return None

    def _delete_request_sync(
        self, request: DeleteRequestRequest
    ) -> DeleteRequestResponse:
        """Internal sync method to delete request."""
        response = self._make_request(
            "DELETE",
            "/api/delete_request",
            json=request.model_dump(),
        )
        return DeleteRequestResponse(**response)

    async def _delete_request_async(
        self, request: DeleteRequestRequest
    ) -> DeleteRequestResponse:
        """Internal async method to delete request."""
        response = await self._make_async_request(
            "DELETE",
            "/api/delete_request",
            json=request.model_dump(),
        )
        return DeleteRequestResponse(**response)

    def delete_request(
        self, request_id: str, wait_for_response: bool = False
    ) -> Optional[DeleteRequestResponse]:
        """Delete a request and all its associated interactions.

        This method is optimized for resource efficiency:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            request_id (str): The request ID to delete
            wait_for_response (bool, optional): If True, wait for response. If False, send request without waiting. Defaults to False.

        Returns:
            Optional[DeleteRequestResponse]: Response containing success status and message if wait_for_response=True, None otherwise
        """
        request = DeleteRequestRequest(request_id=request_id)

        if wait_for_response:
            # Synchronous blocking call
            return self._delete_request_sync(request)
        else:
            # Non-blocking fire-and-forget
            self._fire_and_forget(
                self._delete_request_sync, self._delete_request_async, request
            )
            return None

    def _delete_request_group_sync(
        self, request: DeleteRequestGroupRequest
    ) -> DeleteRequestGroupResponse:
        """Internal sync method to delete request group."""
        response = self._make_request(
            "DELETE",
            "/api/delete_request_group",
            json=request.model_dump(),
        )
        return DeleteRequestGroupResponse(**response)

    async def _delete_request_group_async(
        self, request: DeleteRequestGroupRequest
    ) -> DeleteRequestGroupResponse:
        """Internal async method to delete request group."""
        response = await self._make_async_request(
            "DELETE",
            "/api/delete_request_group",
            json=request.model_dump(),
        )
        return DeleteRequestGroupResponse(**response)

    def delete_request_group(
        self, request_group: str, wait_for_response: bool = False
    ) -> Optional[DeleteRequestGroupResponse]:
        """Delete all requests and interactions in a request group.

        This method is optimized for resource efficiency:
        - In async contexts (e.g., FastAPI): Uses existing event loop (most efficient)
        - In sync contexts: Uses shared thread pool (avoids thread creation overhead)

        Args:
            request_group (str): The request group to delete
            wait_for_response (bool, optional): If True, wait for response. If False, send request without waiting. Defaults to False.

        Returns:
            Optional[DeleteRequestGroupResponse]: Response containing success status, message, and deleted count if wait_for_response=True, None otherwise
        """
        request = DeleteRequestGroupRequest(request_group=request_group)

        if wait_for_response:
            # Synchronous blocking call
            return self._delete_request_group_sync(request)
        else:
            # Non-blocking fire-and-forget
            self._fire_and_forget(
                self._delete_request_group_sync,
                self._delete_request_group_async,
                request,
            )
            return None

    def get_profile_change_log(self) -> ProfileChangeLogResponse:
        """Get profile change log.

        Returns:
            ProfileChangeLogResponse: Response containing profile change log
        """
        response = self._make_request("GET", "/api/profile_change_log")
        return ProfileChangeLogResponse(**response)

    def get_interactions(
        self,
        request: Union[GetInteractionsRequest, dict],
    ) -> GetInteractionsResponse:
        """Get user interactions.

        Args:
            request (GetInteractionsRequest): The list request

        Returns:
            GetInteractionsResponse: Response containing list of interactions
        """
        request = self._convert_to_model(request, GetInteractionsRequest)
        response = self._make_request(
            "POST",
            "/api/get_interactions",
            json=request.model_dump(),
        )
        return GetInteractionsResponse(**response)

    def get_profiles(
        self,
        request: Union[GetUserProfilesRequest, dict],
        force_refresh: bool = False,
    ) -> GetUserProfilesResponse:
        """Get user profiles.

        Args:
            request (GetUserProfilesRequest): The list request
            force_refresh (bool, optional): If True, bypass cache and fetch fresh data. Defaults to False.

        Returns:
            GetUserProfilesResponse: Response containing list of profiles
        """
        request = self._convert_to_model(request, GetUserProfilesRequest)

        # Check cache if not forcing refresh
        if not force_refresh:
            cached_result = self._cache.get(
                "get_profiles",
                user_id=request.user_id,
                start_time=request.start_time,
                end_time=request.end_time,
                top_k=request.top_k,
            )
            if cached_result is not None:
                return cached_result

        # Make API call
        response = self._make_request(
            "POST",
            "/api/get_profiles",
            json=request.model_dump(),
        )
        result = GetUserProfilesResponse(**response)

        # Store in cache
        self._cache.set(
            "get_profiles",
            result,
            user_id=request.user_id,
            start_time=request.start_time,
            end_time=request.end_time,
            top_k=request.top_k,
        )

        return result

    def get_all_profiles(
        self,
        limit: int = 100,
    ) -> GetUserProfilesResponse:
        """Get all user profiles across all users.

        Args:
            limit (int, optional): Maximum number of profiles to return. Defaults to 100.

        Returns:
            GetUserProfilesResponse: Response containing all user profiles
        """
        response = self._make_request(
            "GET",
            f"/api/get_all_profiles?limit={limit}",
        )
        return GetUserProfilesResponse(**response)

    def set_config(self, config: Union[Config, dict]) -> dict:
        """Set configuration for the organization.

        Args:
            config (Union[Config, dict]): The configuration to set

        Returns:
            dict: Response containing success status and message
        """
        config = self._convert_to_model(config, Config)
        response = self._make_request(
            "POST",
            "/api/set_config",
            json=config.model_dump(),
        )
        return response

    def get_config(self) -> Config:
        """Get configuration for the organization.

        Returns:
            Config: The current configuration
        """
        response = self._make_request(
            "GET",
            "/api/get_config",
        )
        return Config(**response)

    def get_raw_feedbacks(
        self,
        request: Optional[Union[GetRawFeedbacksRequest, dict]] = None,
    ) -> GetRawFeedbacksResponse:
        """Get raw feedbacks.

        Args:
            request (Optional[Union[GetRawFeedbacksRequest, dict]]): The get request, defaults to empty request if None

        Returns:
            GetRawFeedbacksResponse: Response containing raw feedbacks
        """
        if request is None:
            request = GetRawFeedbacksRequest()
        else:
            request = self._convert_to_model(request, GetRawFeedbacksRequest)
        response = self._make_request(
            "POST",
            "/api/get_raw_feedbacks",
            json=request.model_dump(),
        )
        return GetRawFeedbacksResponse(**response)

    def get_feedbacks(
        self,
        request: Optional[Union[GetFeedbacksRequest, dict]] = None,
        force_refresh: bool = False,
    ) -> GetFeedbacksResponse:
        """Get feedbacks.

        Args:
            request (Optional[Union[GetFeedbacksRequest, dict]]): The get request, defaults to empty request if None
            force_refresh (bool, optional): If True, bypass cache and fetch fresh data. Defaults to False.

        Returns:
            GetFeedbacksResponse: Response containing feedbacks
        """
        if request is None:
            request = GetFeedbacksRequest()
        else:
            request = self._convert_to_model(request, GetFeedbacksRequest)

        # Check cache if not forcing refresh
        if not force_refresh:
            cached_result = self._cache.get(
                "get_feedbacks",
                limit=request.limit,
                feedback_name=request.feedback_name,
            )
            if cached_result is not None:
                return cached_result

        # Make API call
        response = self._make_request(
            "POST",
            "/api/get_feedbacks",
            json=request.model_dump(),
        )
        result = GetFeedbacksResponse(**response)

        # Store in cache
        self._cache.set(
            "get_feedbacks",
            result,
            limit=request.limit,
            feedback_name=request.feedback_name,
        )

        return result

    def get_requests(
        self,
        request: Union[GetRequestsRequest, dict],
    ) -> GetRequestsResponse:
        """Get requests with their associated interactions, grouped by request_group.

        Args:
            request (Union[GetRequestsRequest, dict]): The get request

        Returns:
            GetRequestsResponse: Response containing requests grouped by request_group with their interactions
        """
        request = self._convert_to_model(request, GetRequestsRequest)
        response = self._make_request(
            "POST",
            "/api/get_requests",
            json=request.model_dump(),
        )
        return GetRequestsResponse(**response)

    def get_agent_success_evaluation_results(
        self,
        request: Union[GetAgentSuccessEvaluationResultsRequest, dict],
    ) -> GetAgentSuccessEvaluationResultsResponse:
        """Get agent success evaluation results.

        Args:
            request (Union[GetAgentSuccessEvaluationResultsRequest, dict]): The get request

        Returns:
            GetAgentSuccessEvaluationResultsResponse: Response containing agent success evaluation results
        """
        request = self._convert_to_model(
            request, GetAgentSuccessEvaluationResultsRequest
        )
        response = self._make_request(
            "POST",
            "/api/get_agent_success_evaluation_results",
            json=request.model_dump(),
        )
        return GetAgentSuccessEvaluationResultsResponse(**response)
