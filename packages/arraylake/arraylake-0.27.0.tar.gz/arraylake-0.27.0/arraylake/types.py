from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import UTC, datetime, time, timedelta
from enum import Enum, StrEnum
from typing import Annotated, Any, Generic, Literal, TypeAlias, TypeVar
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    PlainValidator,
    SecretStr,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic.functional_validators import BeforeValidator

HTML = str

VALID_NAME = r"(\w[\w\.\-_]+)"

ScalarType = str | int | float | bool | None

RepoMetadataT = dict[str, ScalarType | list[ScalarType]]

OrgName: TypeAlias = str
RepoName: TypeAlias = str
OrgAndRepoName: TypeAlias = str  # of the form {org_name}/{repo_name}
BucketPrefix: TypeAlias = str
BucketNickname: TypeAlias = str
URI: TypeAlias = str  # of the form "platform://bucket_name[/prefix]"


def validate_name(name: str, *, entity: str) -> str:
    """
    All names must start with a word character (i.e. letter, digit, or underscore),
    then have at least one more character, which is either another word character, a dot, or a hyphen.
    """
    if not re.fullmatch(VALID_NAME, name):
        raise ValueError(f"Invalid {entity} name: `{name}`")

    return name


class NameValidator:
    def __init__(self, *, entity: str) -> None:
        self.entity = entity

    def __call__(self, name: str) -> str:
        return validate_name(name, entity=self.entity)


# TODO in python 3.12+ we should add `type ` to the start of these lines
# That should stop IDE linters complaining that "Variable is not allowed in type expression" by making it a proper type alias
OrgName: TypeAlias = Annotated[str, BeforeValidator(NameValidator(entity="org"))]
RepoName: TypeAlias = Annotated[str, BeforeValidator(NameValidator(entity="repo"))]


def validate_org_and_repo_name(org_and_repo_name: str) -> str:
    expr = f"{VALID_NAME}/{VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo_name)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo_name}`. Should have the form `[ORG]/[REPO]`.")

    return org_and_repo_name


OrgAndRepoName: TypeAlias = Annotated[str, BeforeValidator(validate_org_and_repo_name)]  # of the form {org_name}/{repo_name}


def validate_bucket_name(name: str) -> str:
    """
    S3 and GCS have fairly strict naming rules so we can mostly rely on them here.
    Our checks are meant to make sure the data we receive is valid.
    """

    if " " in name:
        raise ValueError(f"Bucket name must not contain spaces. Received {name}")
    if "://" in name:
        raise ValueError(f"Bucket name must not contain schemes. Received {name}")
    if "/" in name:
        raise ValueError(f"Bucket name must not contain slashes. Received {name}")
    if len(name) < 3:
        raise ValueError(f"Bucket name must be at least 3 characters long. Received {name}")

    validate_name(name, entity="bucket")

    return name


BucketName: TypeAlias = Annotated[str, BeforeValidator(validate_bucket_name)]


def validate_nickname(nickname: str) -> str:
    # Remove leading and trailing whitespace.
    nickname = nickname.strip()

    validate_name(name=nickname, entity="bucket nickname")

    # NOTE: We only impose a limit on string size. This is intended to be a
    # human-friendly identifier, so we're looser than e.g. S3 regarding
    # naming conventions and restrictions.
    if len(nickname) < 3:
        raise ValueError("Bucket nickname must be at least 3 characters long.")
    if len(nickname) > 64:
        raise ValueError("Bucket nickname must be at most 64 characters long.")

    return nickname


BucketNickname: TypeAlias = Annotated[str, BeforeValidator(validate_nickname)]


def validate_bucket_prefix(prefix: str) -> str:
    if prefix == "":
        return prefix
    # Remove leading and trailing whitespace.
    prefix = prefix.strip()
    if " " in prefix:
        raise ValueError("Bucket prefix must not contain spaces.")
    if prefix.startswith("/") or prefix.endswith("/"):
        raise ValueError("Bucket prefix must not start or end with a slash.")

    return prefix


BucketPrefix: TypeAlias = Annotated[str, BeforeValidator(validate_bucket_prefix)]
URI: TypeAlias = str  # of the form "platform://bucket_name[/prefix]"


def utc_now():
    # drop microseconds because bson does not support them
    return datetime.now(UTC).replace(microsecond=0)


def datetime_to_isoformat(v: datetime) -> str:
    return v.isoformat()


def to_dbid_bytes(v: Any) -> DBIDBytes:
    if isinstance(v, str):
        return DBIDBytes.fromhex(v)
    if isinstance(v, bytes):
        return DBIDBytes(v)
    if hasattr(v, "binary"):
        return DBIDBytes(v.binary)
    raise ValueError("Invalid DBID object")


class DBIDBytes(bytes):
    def __str__(self) -> str:
        """Format as hex digits"""
        return self.hex()

    def __repr__(self):
        return str(self)


def dbid_validator(v: Any) -> DBIDBytes:
    return to_dbid_bytes(v)


DBID = Annotated[DBIDBytes, PlainValidator(dbid_validator)]


class RepoKind(StrEnum):
    V1 = "v1"
    Icechunk = "icechunk"


class RepoCreateBody(BaseModel):
    name: RepoName
    description: str | None = None
    bucket_nickname: BucketNickname | None = None
    kind: RepoKind = RepoKind.Icechunk
    prefix: BucketPrefix | None = None
    create_mode: Literal["create", "register", "import", "subscribe"] = "register"
    marketplace_listing_id: str | None = None  # Required when create_mode = "subscribe"
    metadata: RepoMetadataT | None = None

    @model_validator(mode="after")
    def validate_subscription_info(self) -> RepoCreateBody:
        if self.create_mode == "subscribe" and self.marketplace_listing_id is None:
            raise ValueError("marketplace_listing_id is required when create_mode is 'subscribe'")
        return self


class RepoModifyRequest(BaseModel):
    description: str | None = None
    add_metadata: RepoMetadataT | None = None
    remove_metadata: list[str] | None = None
    update_metadata: RepoMetadataT | None = None
    optimization_config: OptimizationConfig | None = None


class RepoModifyBody(BaseModel):
    description: str | None = None
    metadata: RepoMetadataT | None = None
    optimization_config: OptimizationConfig | None = None


# Used for `/orgs/{org}/{repo}/visibility` endpoint
class RepoVisibilityModel(BaseModel):
    """The visibility of a repo"""

    visibility: RepoVisibility


class RepoVisibility(str, Enum):
    # PRIVATE: Visible only to repo members.
    # NOTE: Currently, this means any member of an org.
    PRIVATE = "PRIVATE"

    # AUTHENTICATED_PUBLIC: Visible to any authenticated user of Arraylake.
    AUTHENTICATED_PUBLIC = "AUTHENTICATED_PUBLIC"

    # PUBLIC: Visible to anybody on the public internet.
    # PUBLIC = "PUBLIC"


Platform = Literal["s3", "s3-compatible", "minio", "gs", "azure"]


class AWSCustomerManagedRoleAuth(BaseModel):
    # TODO: Run a Mongo migration to convert all existing customer_managed_role
    # auth to aws_customer_managed_role.
    method: Literal["aws_customer_managed_role", "customer_managed_role"]
    external_customer_id: str
    external_role_name: str
    shared_secret: SecretStr | None = None

    @field_serializer("shared_secret", when_used="unless-none")
    def serialize_shared_secret(self, v, _info):
        """
        Serialize shared_secret based on context:
        - context={'reveal_secrets': True}: Reveal secret (for client → server API calls)
        - Otherwise: Keep obfuscated (for server → client responses and display)
        """
        if _info.context and _info.context.get("reveal_secrets"):
            return v.get_secret_value() if isinstance(v, SecretStr) else v
        # Default: keep obfuscated
        return str(v) if isinstance(v, SecretStr) else v


class GCPCustomerManagedRoleAuth(BaseModel):
    method: Literal["gcp_customer_managed_role"]
    target_service_account: str


class R2CustomerManagedRoleAuth(BaseModel):
    method: Literal["r2_customer_managed_role"]
    external_account_id: str
    account_api_token: SecretStr
    parent_access_key_id: SecretStr
    duration_seconds: int = 3600  # Default to 1 hour TODO: figure out how we want to handle expiration

    @field_serializer("account_api_token", "parent_access_key_id", when_used="unless-none")
    def serialize_secrets(self, v, _info):
        """
        Serialize secrets based on context:
        - context={'reveal_secrets': True}: Reveal secret (for client → server API calls)
        - Otherwise: Keep obfuscated (for server → client responses and display)
        """
        if _info.context and _info.context.get("reveal_secrets"):
            return v.get_secret_value() if isinstance(v, SecretStr) else v
        # Default: keep obfuscated
        return str(v) if isinstance(v, SecretStr) else v


class AzureDelegatedCredentialsAuth(BaseModel):
    method: Literal["azure_credential_delegation"]
    tenant_id: str  # Tenant ID where the storage account resides
    storage_account: str  # Azure storage account name that contains the container/bucket


CustomerManagedRoleAuth: TypeAlias = (
    AWSCustomerManagedRoleAuth | GCPCustomerManagedRoleAuth | R2CustomerManagedRoleAuth | AzureDelegatedCredentialsAuth
)


# NOTE: Deprecating bucket policy method
class BucketPolicyAuth(BaseModel):
    method: Literal["bucket_policy"]


class HmacAuth(BaseModel):
    method: Literal["hmac"]
    # NOTE: these ideally would be secret strings
    access_key_id: str
    secret_access_key: str


# TODO: Rename to Self Managed
class AnonymousAuth(BaseModel):
    method: Literal["anonymous"]


AuthConfig: TypeAlias = CustomerManagedRoleAuth | BucketPolicyAuth | HmacAuth | AnonymousAuth


class BucketModel(BaseModel):
    """
    Common attributes defining a bucket configuration in arraylake.

    Used for NewBucket requests, so should only contain parameters that users should be allowed to set.
    """

    nickname: BucketNickname
    platform: Platform
    name: BucketName
    prefix: BucketPrefix = ""
    extra_config: Mapping[str, str | bool]

    @property
    def protocol(self) -> str:
        """The protocol (or "scheme") used for urls to this bucket, e.g. 's3://'."""
        match self.platform:
            case "s3" | "s3-compatible" | "minio":
                return "s3://"
            case "gs":
                return "gs://"
            case "azure":
                return "az://"
            case _:
                raise NotImplementedError(self.platform)

    @property
    def url(self) -> URI:
        """
        The full url to the bucket, e.g. 's3://bucket/prefix/'.

        Includes platform scheme, bucket name, and possibly prefix.
        """
        url = f"{self.protocol}{self.name}/{self.prefix}"
        return url + "/" if not url.endswith("/") else url

    @property
    def region_name(self) -> str | None:
        """
        Cloud region for this bucket (e.g. `us-east-1`)

        Returns `None` If not applicable (e.g. for R2 or Tigris buckets).
        """
        region = self.extra_config.get("region_name")
        return str(region) if region else None


class Bucket(BucketModel):
    """A bucket configuration which actually exists in arraylake."""

    id: UUID
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    created_by: EmailStr | None = None

    # NOTE: To prevent credential leakage, we don't share the auth_config here.

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=UTC)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)

    @property
    def protocol(self) -> str:
        """The protocol (or "scheme") used for urls to this bucket, e.g. 's3://'."""
        match self.platform:
            case "s3" | "s3-compatible" | "minio":
                # TODO is this right for e.g. r2?
                return "s3://"
            case "gs":
                return "gs://"
            case "azure":
                return "az://"
            case _:
                raise NotImplementedError(self.platform)

    @property
    def url(self) -> URI:
        """
        The full url to the bucket, e.g. 's3://bucket/prefix/'.

        Included platform scheme, bucket name, and possibly prefix.
        """
        url = f"{self.protocol}{self.name}/{self.prefix}"
        return url + "/" if not url.endswith("/") else url


class NewBucket(BucketModel):
    """A request to create a new bucket."""

    auth_config: AuthConfig = Field(discriminator="method")

    @model_validator(mode="after")
    def _validate_bucket_options(self):
        if self.platform in ["s3"]:  # TODO: decide if the same is needed for gs buckets
            if "region_name" not in self.extra_config:
                raise ValueError("S3 buckets require a region_name.")
        if self.platform == "s3-compatible":
            if "endpoint_url" not in self.extra_config:
                raise ValueError("S3-compatible buckets require an endpoint_url.")
        return self

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None, info: ValidationInfo) -> AuthConfig | None:
        valid_methods = [
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
            "anonymous",
            "hmac",
        ]
        if auth_config and auth_config.method not in valid_methods:
            # Deprecating bucket policy method
            raise ValueError(f"Bucket auth config method must be one of {valid_methods}")
        if auth_config:
            if auth_config.method in ("customer_managed_role", "aws_customer_managed_role") and not info.data["platform"] == "s3":
                raise ValueError("Customer managed role is only supported for s3 buckets.")
            if auth_config.method == "gcp_customer_managed_role" and not info.data["platform"] == "gs":
                raise ValueError("GCP customer managed role is only supported for gs buckets.")
            if auth_config.method == "r2_customer_managed_role":
                # Can't use _is_r2_bucket because of circular import issues
                if not (
                    info.data["platform"] == "s3-compatible"
                    and info.data["extra_config"].get("endpoint_url")
                    and "r2.cloudflarestorage.com" in info.data["extra_config"]["endpoint_url"]
                ):
                    raise ValueError("R2 customer managed role is only supported for R2 buckets.")
            if auth_config.method == "azure_credential_delegation" and not info.data["platform"] == "azure":
                raise ValueError("Azure credential delegation is only supported for azure buckets.")
        return auth_config if auth_config else None


class BucketModifyRequest(BaseModel):
    """A request with optional fields to modify a bucket's config on a per-field
    basis."""

    nickname: BucketNickname | None = None
    platform: Platform | None = None
    name: BucketName | None = None
    prefix: BucketPrefix | None = None
    extra_config: dict[str, Any] | None = None
    auth_config: AuthConfig | None = None

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None) -> AuthConfig | None:
        if auth_config and auth_config.method not in [
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
            "anonymous",
            "hmac",
        ]:
            # Deprecating bucket policy method
            raise ValueError("Bucket auth config method must be Anonymous, Customer Managed Role, or HMAC")
        return auth_config if auth_config else None


class BucketResponse(Bucket):
    """A response after successfully creating a bucket configuration."""

    is_default: bool
    auth_config: AuthConfig | None = None


class RepoOperationMode(StrEnum):
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class NewRepoOperationStatus(BaseModel):
    mode: RepoOperationMode
    message: str | None = None


class RepoOperationStatusResponse(NewRepoOperationStatus):
    initiated_by: dict
    estimated_end_time: datetime | None = None


class ModelWithID(BaseModel):
    id: DBID = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, id: Any) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("id")
    def serialize_id(self, id: DBID) -> str:
        return str(id)


def timedelta_from_seconds(v: Any) -> timedelta:
    if isinstance(v, (int, float)):
        return timedelta(seconds=v)
    if isinstance(v, timedelta):
        return v
    raise ValueError("input must be a timedelta or number of seconds")


class GCKeep(BaseModel):
    pass


class GCDeleteOlderThan(BaseModel):
    date: timedelta


GCAction = GCKeep | GCDeleteOlderThan


class GCConfig(BaseModel):
    """Configuration for garbage collection"""

    extra_gc_roots: set[str] = Field(default_factory=set)
    dangling_chunks: GCAction = Field(default_factory=GCKeep)
    dangling_manifests: GCAction = Field(default_factory=GCKeep)
    dangling_attributes: GCAction = Field(default_factory=GCKeep)
    dangling_transaction_logs: GCAction = Field(default_factory=GCKeep)
    dangling_snapshots: GCAction = Field(default_factory=GCKeep)
    gc_every: timedelta | None = None  # None means no gc
    enabled: bool = False

    @field_validator(
        "dangling_chunks", "dangling_manifests", "dangling_attributes", "dangling_transaction_logs", "dangling_snapshots", mode="before"
    )
    @classmethod
    def _parse_dangling(cls, v: Any) -> GCAction:
        if v is None:
            return GCKeep()
        if isinstance(v, (int, float)):
            return GCDeleteOlderThan(date=timedelta_from_seconds(v))
        else:
            # we let pydantic handle other cases
            return v

    @field_serializer("dangling_chunks", "dangling_manifests", "dangling_attributes", "dangling_transaction_logs", "dangling_snapshots")
    @classmethod
    def serialize_dangling(self, value: GCAction) -> float | None:
        if isinstance(value, GCKeep):
            return None
        else:
            assert isinstance(value, GCDeleteOlderThan)
            return value.date.total_seconds()

    @field_validator("gc_every", mode="before")
    @classmethod
    def parse_gc_every(cls, v: Any) -> timedelta | None:
        if v is not None:
            return timedelta_from_seconds(v)
        return None

    @field_serializer("gc_every")
    @classmethod
    def serialize_gc_every(self, value: timedelta | None) -> float | None:
        if value is not None:
            return value.total_seconds()
        return None


class ExpirationConfig(BaseModel):
    """Configuration for expiration"""

    expire_versions_older_than: timedelta
    expire_every: timedelta | None = None  # None means no expiration
    enabled: bool = False

    @field_validator("expire_every", "expire_versions_older_than", mode="before")
    @classmethod
    def parse_expire_every(cls, v: Any) -> timedelta | None:
        if v is not None:
            return timedelta_from_seconds(v)
        return None

    @field_serializer("expire_every", "expire_versions_older_than")
    @classmethod
    def serialize_expire_every(self, value: timedelta | None) -> float | None:
        if value is not None:
            return value.total_seconds()
        return None


class OptimizationWindow(BaseModel):
    """The preferred time to run optimization tasks on a repo"""

    duration: timedelta
    start_time: time  # Time of day in UTC
    day_of_week: int  # 0 = Monday, 6 = Sunday

    @field_validator("duration", mode="before")
    @classmethod
    def parse_duration(cls, v: Any) -> timedelta:
        return timedelta_from_seconds(v)

    @field_serializer("duration")
    @classmethod
    def serialize_duration(self, duration: timedelta) -> float:
        return duration.total_seconds()


class OptimizationConfig(BaseModel):
    """High-level config for repo optimizations"""

    window: OptimizationWindow | None = None  # If None, uses the org default
    gc_config: GCConfig | None = None
    expiration_config: ExpirationConfig | None = None


class SubscriptionStatus(StrEnum):
    """Status of a repo subscription"""

    ACTIVE = "active"
    ORPHANED = "orphaned"


class MarketplaceListing(BaseModel):
    """Marketplace listing information"""

    id: str
    repo_id: str | None
    org: str
    org_description: str | None = None
    org_avatar: str | None = None
    org_email: str | None = None
    status: str
    repo_readme: str
    listing_name: str
    description: str | None = None
    license_text: str | None = None
    created_on: datetime
    last_updated: datetime

    class Config:
        populate_by_name = True


class RepoSubscriptionInfo(BaseModel):
    """Information about a repo's subscription to a parent repo"""

    parent_repo: Repo | None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    marketplace_listing: MarketplaceListing | None


class Repo(ModelWithID):
    org: OrgName
    name: RepoName
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    description: str | None = None
    metadata: RepoMetadataT | None = None
    created_by: UUID | None = None
    visibility: RepoVisibility = RepoVisibility.PRIVATE
    subscription: RepoSubscriptionInfo | None = None
    bucket: BucketResponse | None = None
    status: RepoOperationStatusResponse
    kind: RepoKind = RepoKind.Icechunk
    prefix: str
    optimization_config: OptimizationConfig = Field(
        default_factory=lambda: OptimizationConfig(
            window=None,
            gc_config=None,
            expiration_config=None,
        )
    )
    permissions: list[Permission[RepoActions]] = Field(default_factory=list)

    def _asdict(self):
        """custom dict method ready to be serialized as json"""
        d = self.model_dump()
        d["id"] = str(d["id"])
        if self.created_by is not None:
            d["created_by"] = str(d["created_by"])
        if d["bucket"]:
            d["bucket"]["id"] = str(d["bucket"]["id"])
        if d["status"]["estimated_end_time"]:
            d["status"]["estimated_end_time"] = datetime_to_isoformat(d["status"]["estimated_end_time"])
        return d

    def __repr__(self) -> str:
        from arraylake.display.repo import reporepr

        return reporepr(self)

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=UTC)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class Author(BaseModel):
    name: str | None = None
    email: EmailStr

    def entry(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        else:
            return f"<{self.email}>"


class OrgActions(Enum):
    """Actions a user can take on a specific org"""

    CAN_MANAGE_USERS = "CAN_MANAGE_USERS"
    CAN_WRITE_REPOS = "CAN_WRITE_REPOS"
    CAN_READ_REPOS = "CAN_READ_REPOS"
    CAN_READ_REPOS_WITH_FLUX = "CAN_READ_REPOS_WITH_FLUX"


class RepoActions(Enum):
    """Actions a user can take on a specific repo"""

    CAN_READ_WITH_FLUX = "CAN_READ_WITH_FLUX"
    CAN_READ = "CAN_READ"
    CAN_WRITE = "CAN_WRITE"
    CAN_MANAGE_USERS = "CAN_MANAGE_USERS"


ActionType = TypeVar("ActionType", OrgActions, RepoActions)


class Permission(BaseModel, Generic[ActionType]):
    """Holds a permission"""

    principal_id: UUID
    actions: set[ActionType] = set()


class PermissionBody(BaseModel):
    principal_id: str
    resource: str
    action: str  # OrgActions | RepoActions


class PermissionCheckResponse(BaseModel):
    has_permission: bool


class TokenAuthenticateBody(BaseModel):
    token: str


class TokenAuthenticateResponse(BaseModel):
    client_id: UUID


class OauthTokensResponse(BaseModel):
    access_token: SecretStr
    id_token: SecretStr
    refresh_token: SecretStr | None = None
    expires_in: int
    token_type: str

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict that drops default values"""
        tokens = super().model_dump(**kwargs)
        # special case: drop refresh token if it is None
        if not tokens.get("refresh_token", 1):
            del tokens["refresh_token"]
        return tokens

    @field_serializer("access_token", "id_token", "refresh_token", when_used="unless-none")
    def dump_secret(self, v) -> str:
        if isinstance(v, SecretStr):
            return v.get_secret_value()
        return v


class OauthTokens(OauthTokensResponse):
    refresh_token: SecretStr

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict method that decodes secrets"""
        tokens = super().model_dump(**kwargs)
        for k, v in tokens.items():
            if isinstance(v, SecretStr):
                tokens[k] = v.get_secret_value()
        return tokens

    def __hash__(self):
        return hash((self.access_token, self.id_token, self.refresh_token, self.expires_in, self.token_type))


class AuthProviderConfig(BaseModel):
    """
    Used to communicate Auth0 configuration to Arraylake Client/CLI
    """

    domain: str
    client_id: str


class UserInfo(BaseModel):
    id: UUID
    first_name: str | None = None
    family_name: str | None = None
    email: EmailStr

    def as_author(self) -> Author:
        return Author(name=f"{self.first_name} {self.family_name}", email=self.email)


class ApiTokenInfo(BaseModel):
    id: UUID
    client_id: str
    email: EmailStr
    expiration: int

    def as_author(self) -> Author:
        return Author(email=self.email)


class UserDiagnostics(BaseModel):
    system: dict[str, str] | None = None
    versions: dict[str, str] | None = None
    config: dict[str, str] | None = None
    service: dict[str, str] | None = None


class ApiClientResponse(BaseModel):
    id: UUID = Field(alias="_id")
    email: EmailStr
    created: datetime
    expiration: datetime
    last_used: datetime | None = None

    @field_serializer("created", "expiration", "last_used")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class S3Credentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str | None
    expiration: datetime | None


class GSCredentials(BaseModel):
    access_token: str
    principal: str
    expiration: datetime | None


class AzureCredentials(BaseModel):
    sas_token: str  # User delegation SAS token
    storage_account: str  # Storage account name
    expiration: datetime | None  # Token expiration


TempCredentials: TypeAlias = S3Credentials | GSCredentials | AzureCredentials
