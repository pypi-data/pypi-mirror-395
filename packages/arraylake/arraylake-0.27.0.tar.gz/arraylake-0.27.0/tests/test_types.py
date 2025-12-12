import uuid

import pytest
from pydantic import SecretStr

from arraylake.types import AWSCustomerManagedRoleAuth, Author, NewBucket, R2CustomerManagedRoleAuth, Repo, utc_now


def test_identities_to_author(test_user, test_api_token):
    user_author: Author = test_user.as_author()
    assert isinstance(user_author, Author)
    assert user_author.email == "abc@earthmover.io"
    assert user_author.name == "TestFirst TestFamily"

    api_author: Author = test_api_token.as_author()
    assert isinstance(api_author, Author)
    assert api_author.email == "svc-email@some-earthmover-org.service.earthmover.io"
    assert not api_author.name


@pytest.mark.parametrize(
    "nickname, platform, prefix, name, extra_config",
    [
        ("foo-bar", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}),
        ("foo_bar", "s3-compatible", "foo", "my_bucket_on_s3", {"endpoint_url": "http://localhost:9000"}),
        ("foo-bar", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}),
        ("foo-bar", "s3", "foo/bar/spam", "my-bucket-on-s3", {"region_name": "us-east-1"}),
    ],
)
def test_bucket_name_validation(nickname, platform, prefix, name, extra_config):
    b = NewBucket(
        nickname=nickname, platform=platform, name=name, prefix=prefix, extra_config=extra_config, auth_config={"method": "anonymous"}
    )
    assert b.nickname == nickname
    assert b.platform == platform
    assert b.name == name
    assert b.prefix == prefix


@pytest.mark.parametrize(
    "nickname, platform, prefix, name, extra_config, err_msg",
    [
        ("fo", "s3", "", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket nickname must be at least 3 characters long."),
        ("foo-bar", "s3", "", "b", {"region_name": "us-east-1"}, "Bucket name must be at least 3 characters long."),
        ("foo-bar", "s3-compatible", "", "my bucket", {"endpoint_url": "http://localhost:9000"}, "Bucket name must not contain spaces."),
        (
            "foo-bar",
            "s3-compatible",
            "",
            "s3://my-arraylake-bucket",
            {"endpoint_url": "http://localhost:9000"},
            "Bucket name must not contain schemes.",
        ),
        ("foo-bar", "s3-compatible", "", "my-arraylake-bucket", {}, "S3-compatible buckets require an endpoint_url"),
        ("foo-bar", "s3", "", "my bucket", {"region_name": "us-east-1"}, "Bucket name must not contain spaces."),
        ("foo-bar", "s3", "/foo/", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket prefix must not start or end with a slash."),
        (
            "foo-bar",
            "s3",
            "/foo/bar/",
            "my-bucket-on-s3",
            {"region_name": "us-east-1"},
            "Bucket prefix must not start or end with a slash.",
        ),
        ("foo-bar", "s3", "foo bar", "my-bucket-on-s3", {"region_name": "us-east-1"}, "Bucket prefix must not contain spaces."),
    ],
)
def test_bucket_name_validation_error(nickname, platform, prefix, name, extra_config, err_msg):
    with pytest.raises(ValueError, match=err_msg):
        b = NewBucket(
            nickname=nickname,
            platform=platform,
            name=name,
            prefix=prefix,
            extra_config=extra_config,
            auth_config={"method": "anonymous"},
        )


def test_aws_auth_secret_serialization():
    """Test that AWS auth secrets are obfuscated by default but revealed with context."""
    auth = AWSCustomerManagedRoleAuth(
        method="aws_customer_managed_role",
        external_customer_id="12345678",
        external_role_name="my-role",
        shared_secret=SecretStr("super-secret-value"),
    )

    # Default serialization should obfuscate
    default_dump = auth.model_dump()
    assert default_dump["shared_secret"] == "**********"

    # JSON mode should also obfuscate by default
    json_dump = auth.model_dump(mode="json")
    assert json_dump["shared_secret"] == "**********"

    # With reveal_secrets context, should reveal the secret
    revealed_dump = auth.model_dump(mode="json", context={"reveal_secrets": True})
    assert revealed_dump["shared_secret"] == "super-secret-value"


def test_r2_auth_secret_serialization():
    """Test that R2 auth secrets are obfuscated by default but revealed with context."""
    auth = R2CustomerManagedRoleAuth(
        method="r2_customer_managed_role",
        external_account_id="account123",
        account_api_token=SecretStr("api-token-secret"),
        parent_access_key_id=SecretStr("access-key-secret"),
    )

    # Default serialization should obfuscate
    default_dump = auth.model_dump()
    assert default_dump["account_api_token"] == "**********"
    assert default_dump["parent_access_key_id"] == "**********"

    # With reveal_secrets context, should reveal the secrets
    revealed_dump = auth.model_dump(mode="json", context={"reveal_secrets": True})
    assert revealed_dump["account_api_token"] == "api-token-secret"
    assert revealed_dump["parent_access_key_id"] == "access-key-secret"
