import asyncio
import os
from typing import Any, ClassVar

import httpx
from loguru import logger

from elluminate.resources import (
    CriteriaResource,
    CriterionSetsResource,
    ExperimentsResource,
    LLMConfigsResource,
    ProjectsResource,
    PromptTemplatesResource,
    RatingsResource,
    ResponsesResource,
    TemplateVariablesCollectionsResource,
    TemplateVariablesResource,
)
from elluminate.utils import raise_for_status_with_detail


class Client:
    _semaphore: ClassVar[asyncio.Semaphore] = asyncio.Semaphore(10)

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        token: str | None = None,
        project_id: int | None = None,
        api_key_env: str = "ELLUMINATE_API_KEY",
        token_env: str = "ELLUMINATE_OAUTH_TOKEN",
        base_url_env: str = "ELLUMINATE_BASE_URL",
        timeout: float = 120.0,
        proxy: str | None = None,
    ) -> None:
        """Initialize the Elluminate SDK client.

        Args:
            base_url (str): Base URL of the Elluminate API. Defaults to "https://app.elluminate.de".
            api_key (str | None): API key for authentication. If not provided, will look for key in environment variable given by `api_key_env`.
            token (str | None): OAuth access token for authentication. If not provided, will look for token in environment variable given by `token_env`.
            project_id (int | None): Project ID to select.
            api_key_env (str): Name of environment variable containing API key. Defaults to "ELLUMINATE_API_KEY".
            token_env (str): Name of environment variable containing OAuth token. Defaults to "ELLUMINATE_OAUTH_TOKEN".
            base_url_env (str): Name of environment variable containing base URL. Defaults to "ELLUMINATE_BASE_URL". If set, overrides base_url.
            timeout (float): Timeout in seconds for API requests. Defaults to 120.0.
            proxy (str | None): Proxy URL for HTTP/HTTPS requests (e.g., "http://proxy.example.com:8080" or "http://user:pass@proxy.example.com:8080").
                If not provided, will check HTTP_PROXY, HTTPS_PROXY, and ALL_PROXY environment variables.

        Raises:
            ValueError: If neither API key nor token is provided or found in environment.

        """
        self.api_key, self.token = self._resolve_credentials(api_key, token, api_key_env, token_env)
        self.base_url = self._resolve_base_url(base_url, base_url_env)
        self.timeout = timeout
        self.proxy = self._resolve_proxy(proxy)

        # Local import to avoid circular imports when referencing the version
        from elluminate import __version__

        headers = self._build_default_headers(__version__)

        timeout_config = httpx.Timeout(self.timeout)
        self.async_session = httpx.AsyncClient(
            headers=headers, timeout=timeout_config, follow_redirects=True, proxy=self.proxy
        )
        self.sync_session = httpx.Client(
            headers=headers, timeout=timeout_config, follow_redirects=True, proxy=self.proxy
        )

        # Check the SDK version compatibility and print warning if needed
        self.check_version()

        # Load the project and set the route prefix
        self.projects = ProjectsResource(self)
        # The projects resource sets `current_project` and `project_route_prefix`
        self.current_project = self.projects.load_project(project_id=project_id)
        logger.info(f"Active project set to ID {self.current_project.id}")

        # Initialize the resources
        self.prompt_templates = PromptTemplatesResource(self)
        self.collections = TemplateVariablesCollectionsResource(self)
        self.template_variables = TemplateVariablesResource(self)
        self.responses = ResponsesResource(self)
        self.criteria = CriteriaResource(self)
        self.criterion_sets = CriterionSetsResource(self)
        self.llm_configs = LLMConfigsResource(self)
        self.experiments = ExperimentsResource(self)
        self.ratings = RatingsResource(self)

    def check_version(self) -> None:
        """Check if the SDK version is compatible with the required version."""
        # Import locally to avoid circular imports
        from elluminate import __version__

        response = self.sync_session.post(
            f"{self.base_url}/api/v0/version/compatible",
            json={"current_sdk_version": __version__},
        )
        raise_for_status_with_detail(response)
        compatibility = response.json()
        if not compatibility["is_compatible"]:
            response = httpx.get("https://pypi.org/pypi/elluminate/json")
            current_pypi_version = response.json()["info"]["version"]
            logger.warning(
                f"Current SDK version ({__version__}) is not compatible with the required version ({compatibility['required_sdk_version']}). "
                "Some features may not work as expected. "
                f"Please upgrade the SDK to the latest version ({current_pypi_version}) by running `pip install -U elluminate`."
            )

    async def _aget(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.async_session.get(f"{self.project_route_prefix}/{path}", **kwargs)
        raise_for_status_with_detail(response)
        return response

    async def _apost(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.async_session.post(f"{self.project_route_prefix}/{path}", **kwargs)
        raise_for_status_with_detail(response)
        return response

    async def _aput(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.async_session.put(f"{self.project_route_prefix}/{path}", **kwargs)
        raise_for_status_with_detail(response)
        return response

    async def _adelete(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.async_session.delete(f"{self.project_route_prefix}/{path}", **kwargs)
        raise_for_status_with_detail(response)
        return response

    async def _apatch(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self.async_session.patch(f"{self.project_route_prefix}/{path}", **kwargs)
        raise_for_status_with_detail(response)
        return response

    def _resolve_credentials(
        self,
        api_key: str | None,
        token: str | None,
        api_key_env: str,
        token_env: str,
    ) -> tuple[str | None, str | None]:
        if api_key is not None or token is not None:
            # Important: any token that is directly provided takes precedence over the environment variables
            resolved_api_key = api_key
            resolved_token = token
        else:
            resolved_api_key = os.getenv(api_key_env)
            resolved_token = os.getenv(token_env)
        if not resolved_api_key and not resolved_token:
            raise ValueError(f"Neither {api_key_env} nor {token_env} set.")
        return resolved_api_key, resolved_token

    def _resolve_base_url(self, base_url: str | None, base_url_env: str) -> str:
        resolved = base_url or os.getenv(base_url_env) or "https://app.elluminate.de"
        return resolved.rstrip("/")

    def _resolve_proxy(self, proxy: str | None) -> str | None:
        """Resolve proxy configuration from parameter or environment variables.

        Args:
            proxy: Explicitly provided proxy URL.

        Returns:
            Proxy URL if configured, None otherwise.

        Note:
            httpx automatically respects HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, and NO_PROXY
            environment variables when proxy=None. By explicitly checking these, we allow
            users to see which proxy is being used via the proxy attribute.

        """
        if proxy is not None:
            return proxy

        # Check standard proxy environment variables
        # httpx will use these automatically, but we expose them for visibility
        return os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY") or os.getenv("ALL_PROXY")

    def _build_default_headers(self, sdk_version: str) -> dict[str, str]:
        if self.api_key:
            logger.info(f"Using API key: {self.api_key[:5]}...")
            return {"X-API-Key": self.api_key, "SDK-Version": sdk_version}

        if not self.token:
            raise ValueError("OAuth token not provided.")

        logger.info(f"Using OAuth token: {self.token[:5]}...")
        return {"Authorization": f"Bearer {self.token}", "SDK-Version": sdk_version}
