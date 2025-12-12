from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal, TypeVar
from uuid import UUID

from pydantic import TypeAdapter

from arraylake.api_utils import ArraylakeHttpClient, handle_response
from arraylake.metastore.abc import Metastore
from arraylake.types import (
    ApiClientResponse,
    AzureCredentials,
    BucketModifyRequest,
    BucketResponse,
    GSCredentials,
    NewBucket,
    NewRepoOperationStatus,
    OptimizationConfig,
    OrgActions,
    PermissionBody,
    PermissionCheckResponse,
    Repo,
    RepoActions,
    RepoCreateBody,
    RepoKind,
    RepoMetadataT,
    RepoModifyRequest,
    RepoOperationMode,
    RepoOperationStatusResponse,
    S3Credentials,
    TokenAuthenticateBody,
)

# type adapters
LIST_DATABASES_ADAPTER = TypeAdapter(list[Repo])
LIST_BUCKETS_ADAPTER = TypeAdapter(list[BucketResponse])
LIST_REPOS_FOR_BUCKET_ADAPTER = TypeAdapter(list[Repo])

T = TypeVar("T")


@dataclass
class HttpMetastoreConfig:
    """Encapsulates the configuration for the HttpMetastore"""

    api_service_url: str
    org: str
    token: str | None = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth


class HttpMetastore(ArraylakeHttpClient, Metastore):
    """ArrayLake's HTTP Metastore

    This metastore connects to ArrayLake over HTTP

    args:
        config: config for the metastore

    :::note
    Authenticated calls require an Authorization header. Run ``arraylake auth login`` to login before using this metastore.
    :::
    """

    _config: HttpMetastoreConfig

    def __init__(self, config: HttpMetastoreConfig):
        super().__init__(config.api_service_url, token=config.token)

        self._config = config
        self.api_url = config.api_service_url

    async def ping(self) -> dict[str, Any]:
        response = await self._request("GET", "user")
        handle_response(response)

        return response.json()

    async def get_database(self, name: str) -> Repo:
        response = await self._request("GET", f"/repos/{self._config.org}/{name}")
        handle_response(response)
        return Repo.model_validate_json(response.content)

    async def list_databases(self, filter_metadata: RepoMetadataT | None = None) -> list[Repo]:
        # Serialize filter_metadata to JSON string
        filter_metadata_json = json.dumps(filter_metadata) if filter_metadata else None
        response = await self._request("GET", f"/orgs/{self._config.org}/repos", params={"filter_metadata": filter_metadata_json})
        handle_response(response)
        return LIST_DATABASES_ADAPTER.validate_json(response.content)

    async def create_database(
        self,
        name: str,
        bucket_nickname: str | None = None,
        kind: RepoKind = RepoKind.Icechunk,
        prefix: str | None = None,
        import_existing: bool = False,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
    ):
        """
        Creates a repo database entry in the metastore.

        Args:
            name: Name of the repo to create
            bucket_nickname: Optional nickname of a bucket already existing in the org.
            kind: Kind of repo to create
            prefix: Optional prefix for the icechunk repo
            import_existing: Whether to import an existing icechunk repo
            description: Optional description for the repo
            metadata: Optional metadata for the repo
        """
        create_mode: Literal["create", "register", "import"] = "import" if import_existing else "register"
        body = RepoCreateBody(
            name=name,
            bucket_nickname=bucket_nickname,
            kind=kind,
            prefix=prefix,
            create_mode=create_mode,
            description=description,
            metadata=metadata,
        )
        response = await self._request("POST", f"/orgs/{self._config.org}/repos", content=body.model_dump_json())
        handle_response(response)
        repo = Repo.model_validate_json(response.content)

        if repo.kind == RepoKind.Icechunk:
            # TODO: should I wrap this response in an IcechunkV2Database object?
            return repo

        raise ValueError(f"Unknown repo kind: {repo.kind}")

    async def set_repo_status(self, name: str, mode: RepoOperationMode, message: str | None = None) -> RepoOperationStatusResponse:
        """Set repo status"""
        new_status = NewRepoOperationStatus(mode=mode, message=message)
        response = await self._request("PUT", f"/orgs/{self._config.org}/{name}/status", content=new_status.model_dump_json())
        handle_response(response)
        return RepoOperationStatusResponse.model_validate_json(response.content)

    async def modify_database(
        self,
        name: str,
        description: str | None = None,
        add_metadata: RepoMetadataT | None = None,
        remove_metadata: list[str] | None = None,
        update_metadata: RepoMetadataT | None = None,
        optimization_config: OptimizationConfig | None = None,
    ) -> None:
        repo_modify_request = RepoModifyRequest(
            description=description,
            add_metadata=add_metadata,
            remove_metadata=remove_metadata,
            update_metadata=update_metadata,
            optimization_config=optimization_config,
        )
        response = await self._request("PATCH", f"/orgs/{self._config.org}/{name}", content=repo_modify_request.model_dump_json())
        handle_response(response)

    async def delete_database(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        if not (imsure and imreallysure):
            raise ValueError("Don't do this unless you're really sure. Once the database has been deleted, it's gone forever.")

        response = await self._request("DELETE", f"/orgs/{self._config.org}/{name}")
        handle_response(response)

    async def create_bucket_config(self, bucket_config: NewBucket) -> BucketResponse:
        response = await self._request(
            "POST",
            f"/orgs/{self._config.org}/buckets",
            content=bucket_config.model_dump_json(context={"reveal_secrets": True}),
        )
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def get_bucket_config(self, bucket_id: UUID) -> BucketResponse:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}")
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def modify_bucket_config(self, bucket_id: UUID, bucket_config: BucketModifyRequest) -> BucketResponse:
        response = await self._request(
            "PATCH",
            f"/orgs/{self._config.org}/buckets/{bucket_id}",
            content=bucket_config.model_dump_json(context={"reveal_secrets": True}),
        )
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def delete_bucket_config(self, bucket_id: UUID) -> None:
        response = await self._request("DELETE", f"/orgs/{self._config.org}/buckets/{bucket_id}")
        handle_response(response)

    async def list_bucket_configs(self) -> list[BucketResponse]:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets")
        handle_response(response)
        return LIST_BUCKETS_ADAPTER.validate_json(response.content)

    async def list_repos_for_bucket_config(self, bucket_id: UUID) -> list[Repo]:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/repos")
        handle_response(response)
        return LIST_REPOS_FOR_BUCKET_ADAPTER.validate_json(response.content)

    async def set_default_bucket_config(self, bucket_id: UUID) -> None:
        response = await self._request("POST", f"/orgs/{self._config.org}/buckets/{bucket_id}/default")
        handle_response(response)

    async def get_s3_bucket_credentials_from_repo(self, name: str) -> S3Credentials:
        """Gets the S3 credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return S3Credentials.model_validate_json(response.content)

    async def get_gs_bucket_credentials_from_repo(self, name: str) -> GSCredentials:
        """Gets the GCS credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return GSCredentials.model_validate_json(response.content)

    async def get_azure_container_credentials_from_repo(self, name: str) -> AzureCredentials:
        """Gets the Azure credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return AzureCredentials.model_validate_json(response.content)

    async def get_s3_bucket_credentials_from_bucket(self, bucket_id: UUID) -> S3Credentials:
        """Gets the S3 credentials for a bucket. Credentials will be scoped to read-only."""
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials")
        handle_response(response)
        return S3Credentials.model_validate_json(response.content)

    async def get_gs_bucket_credentials_from_bucket(self, bucket_id: UUID) -> GSCredentials:
        """Gets the GCS credentials for a bucket. Credentials will be scoped to read-only."""
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials")
        handle_response(response)
        return GSCredentials.model_validate_json(response.content)

    async def get_azure_container_credentials_from_bucket(self, bucket_id: UUID) -> AzureCredentials:
        """Gets the Azure credentials for a bucket. Credentials will be scoped to read-only."""
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials")
        handle_response(response)
        return AzureCredentials.model_validate_json(response.content)

    async def get_api_client_from_token(self, token: str) -> ApiClientResponse:
        token_body = TokenAuthenticateBody(token=token)
        data = token_body.model_dump()
        response = await self._request("GET", f"/orgs/{self._config.org}/api-clients/authenticate", params=data)
        handle_response(response)
        auth_resp = ApiClientResponse.model_validate_json(response.content)
        return auth_resp

    async def get_permission_check(self, principal_id: str, resource: str, action: OrgActions | RepoActions) -> bool:
        permission_body = PermissionBody(principal_id=principal_id, resource=resource, action=action.value)
        data = permission_body.model_dump()
        response = await self._request("GET", f"/orgs/{self._config.org}/permissions/check", params=data)
        handle_response(response)
        decision = PermissionCheckResponse.model_validate_json(response.content)
        return decision.has_permission
