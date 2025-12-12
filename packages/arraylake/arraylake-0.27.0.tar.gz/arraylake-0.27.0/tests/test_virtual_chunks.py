from uuid import uuid4

import icechunk
import pytest

from arraylake import Client


class TestAuthorization:
    @staticmethod
    def assert_vcc_set(repo: icechunk.Repository, expected_vcc_url_prefix: str) -> None:
        # check the virtual chunk containers have been set
        # TODO annoying that IC doesn't just return an empty dict instead of None if there are no containers
        virtual_chunk_containers = repo.config.virtual_chunk_containers if repo.config.virtual_chunk_containers is not None else {}
        assert set(virtual_chunk_containers) == {expected_vcc_url_prefix}

        # TODO can't easily compare generated icechunk.ObjectStoreConfig objects as that class doesn't implement `__eq__` or even expose access to its attributes :/
        # TODO once we allow virtual chunks to refere to to non-anonymous buckets it will become important to check this!
        # assert virtual_chunk_containers[expected_vcc_prefix].store == expected_storeconfig

    @staticmethod
    def assert_prefixes_authorized(repo: icechunk.Repository, expected_vcc_url_prefix: str) -> None:
        # check virtual chunk containers are correctly authorized
        # TODO apparently the IC config doesn't round-trip the url_prefix string exactly - it removes any trailing slash.
        authorized_prefixes = {prefix if prefix.endswith("/") else prefix + "/" for prefix in repo.authorized_virtual_container_prefixes}
        assert authorized_prefixes == {expected_vcc_url_prefix}

    @staticmethod
    def assert_authorized(repo: icechunk.Repository, expected_vcc_url_prefix: str) -> None:
        TestAuthorization.assert_vcc_set(repo, expected_vcc_url_prefix)
        TestAuthorization.assert_prefixes_authorized(repo, expected_vcc_url_prefix)

    @pytest.mark.parametrize(
        "authorization",
        [
            pytest.param("explicit", id="explicit-authorization"),
            pytest.param("fetch", id="fetch-containers"),
            pytest.param("automatic", id="automatic-discovery", marks=pytest.mark.xfail(reason="Not yet implemented", strict=True)),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_repo(self, isolated_org, default_bucket, minio_anon_bucket, token, authorization):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            name = f"{org_name}/foo"
            repo = client.create_repo(
                name,
                bucket_config_nickname=repo_bucket.nickname,
                config=initial_config,
            )

            # Manually set a virtual chunk container on the icechunk repo directly
            modified_config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            modified_config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=modified_config)
            repo.save_config()

            if authorization == "explicit":
                authorize_virtual_chunk_access = {vcc_url_prefix: virtual_bucket.nickname}
            elif authorization == "fetch":
                authorize_virtual_chunk_access = client.get_virtual_chunk_containers(name)
            elif authorization == "automatic":
                authorize_virtual_chunk_access = None

            # Get the repo
            repo = client.get_repo(name, authorize_virtual_chunk_access=authorize_virtual_chunk_access)

            self.assert_authorized(repo, vcc_url_prefix)

            # check that the original repo config has not been altered
            assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("user_specified_url", "bucket_config_prefix", "expected_vcc_prefix"),
        [
            ("s3://anonbucket/", "", "s3://anonbucket/"),
            ("s3://anonbucket", "", "s3://anonbucket/"),
            ("s3://anonbucket/prefix/", "prefix", "s3://anonbucket/prefix/"),
            ("s3://anonbucket/prefix", "prefix", "s3://anonbucket/prefix/"),
            # passing a more specific prefix than that in the bucket config is allowed
            ("s3://anonbucket/prefix/", "", "s3://anonbucket/prefix/"),
            ("s3://anonbucket/prefix", "", "s3://anonbucket/prefix/"),
            ("s3://anonbucket/prefix/subprefix/", "prefix", "s3://anonbucket/prefix/subprefix/"),
            ("s3://anonbucket/prefix/subprefix", "prefix", "s3://anonbucket/prefix/subprefix/"),
        ],
    )
    async def test_create_repo_with_auto_containers(
        self, isolated_org, default_bucket, minio_anon_bucket, token, user_specified_url, bucket_config_prefix, expected_vcc_prefix
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket(prefix=bucket_config_prefix)

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo, automatically creating virtual chunk containers
            repo_name = "foo"
            name = f"{org_name}/{repo_name}"
            repo = client.create_repo(
                name, authorize_virtual_chunk_access={user_specified_url: virtual_bucket.nickname}, config=initial_config
            )

            self.assert_authorized(repo, expected_vcc_prefix)

            # Get the repo
            # Note: it's assumed that the user passes the exact same prefix at get-time. If they don't then IC will raise because it doesn't do the path standardization that AL does.
            repo = client.get_repo(name, authorize_virtual_chunk_access={user_specified_url: virtual_bucket.nickname})

            self.assert_authorized(repo, expected_vcc_prefix)

            # check that the original repo config has not been altered
            assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_import_existing_repo_with_existing_vccs(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage, config=initial_config)

            # Manually set a virtual chunk container on the icechunk repo directly
            modified_config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=vcc_url_prefix,
                store=icechunk.s3_store(),
            )
            modified_config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=modified_config)
            ic_repo.save_config()

            # Use arraylake client to import the repo
            repo = client.create_repo(
                repo_name,
                prefix=repo_prefix,
                import_existing=True,
                authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname},
            )
            self.assert_authorized(repo, vcc_url_prefix)

            repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})
            self.assert_authorized(repo, vcc_url_prefix)

            # check that the original repo config has not been altered
            assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_import_existing_repo_without_existing_vccs(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            icechunk.Repository.create(storage=ic_storage, config=initial_config)

            # Use arraylake client to import the repo
            with pytest.warns(UserWarning, match="New virtual chunk containers will not be persisted"):
                repo = client.create_repo(
                    repo_name,
                    prefix=repo_prefix,
                    import_existing=True,
                    authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname},
                )
            self.assert_authorized(repo, vcc_url_prefix)

            repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})
            # VCCs won't be present as they were not persisted
            self.assert_prefixes_authorized(repo, vcc_url_prefix)

            # check that the original repo config has not been altered
            assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    async def test_modify_via_authorize_access_method(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        initial_config = icechunk.RepositoryConfig.default()
        initial_config.inline_chunk_threshold_bytes = 1024

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, config=initial_config)

            # explicitly set the virtual chunk containers using AL API
            client.authorize_virtual_chunk_access(name=repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            # Get the repo
            # Note: it's assumed that the user passes the exact same prefix at get-time. If they don't then IC will raise.
            repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            self.assert_authorized(repo, vcc_url_prefix)

            # check that the original repo config has not been altered
            assert repo.config.inline_chunk_threshold_bytes == 1024

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("invalid_user_specified_url", "bucket_config_prefix", "expected_err_msg"),
        [
            # we're not currently auto-inferring anything, including which bucket the user is referring to
            (None, "prefix", "must provide a bucket url"),
            ("prefix/", "prefix", "must be a complete url"),
            ("prefix", "prefix", "must be a complete url"),
            # various ways in which it could be inconsistent
            ("malformed", "prefix", "must be a complete url"),
            (2, "prefix", "must be a valid string url, but got type <class 'int'>"),
            ("gs://anonbucket/", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("gs://anonbucket", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://differentbucket/", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://differentbucket", "prefix", "Provided bucket url must be consistent with bucket config"),
            ("s3://anonbucket/differentprefix/", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
            ("s3://anonbucket/differentprefix", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
            ("s3://anonbucket/prefixwhichisdifferent", "prefix", "Provided prefix must be consistent with prefix in bucket config"),
        ],
    )
    async def test_raise_on_create_repo_with_inconsistent_virtual_chunk_container(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        invalid_user_specified_url,
        bucket_config_prefix,
        expected_err_msg,
    ) -> None:
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket(prefix=bucket_config_prefix)

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"
            with pytest.raises(ValueError, match=expected_err_msg):
                client.create_repo(repo_name, authorize_virtual_chunk_access={invalid_user_specified_url: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_requires_writer_authorization(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name)

            # the repo writer never sets the VCCs

            # Get the repo
            repo = client.get_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            # the reader will not be able to access the virtual chunks
            assert repo.config.virtual_chunk_containers == None


# These tests check that creating potentially malicious IC repos via AL is forbidden,
# and that any potentially malicious IC repos that are created directly via IC are detected at import-time or open-time by AL.


@pytest.mark.parametrize(
    "unsafe_url_prefix, ic_store_type",
    [
        pytest.param(
            "file:///home/",
            "local_filesystem",
        ),
        pytest.param(
            "memory://some-location/",
            "in_memory",
            marks=pytest.mark.xfail(reason="Not implemented in Icechunk"),
        ),
        pytest.param(
            "http://server/",
            "http",
        ),
    ],
)
@pytest.mark.asyncio
class TestForbidUnsafeVirtualChunkContainers:
    """Check that any method of creating an AL repo with virtual chunks detects any potentially malicious virtual chunk containers."""

    # TODO also check upon modify_repo?

    @pytest.fixture
    def ic_store(self, ic_store_type, tmp_path):
        """Create the appropriate ic_store based on the parameterized type."""
        if ic_store_type == "local_filesystem":
            return icechunk.local_filesystem_store(str(tmp_path))
        elif ic_store_type == "in_memory":
            return icechunk.ObjectStoreConfig.InMemory()
        elif ic_store_type == "http":
            return icechunk.http_store()
        else:
            raise ValueError(f"Unknown ic_store_type: {ic_store_type}")

    async def test_create_repo(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        unsafe_url_prefix,
        ic_store_type,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # attempt to create the repo, forbidding automatically creating unsafe virtual chunk containers
            with pytest.raises(ValueError, match="Forbidden virtual chunk container url_prefix"):
                client.create_repo(repo_name, authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_get_repo(self, isolated_org, default_bucket, minio_anon_bucket, token, unsafe_url_prefix, ic_store):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a virtual chunk container on the icechunk repo directly
            # We will also separately forbid doing this with the Arraylake client, but we can't stop a canny bad guy doing it using IC manually
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=unsafe_url_prefix,
                store=ic_store,
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # attempt to get unsafe repo
            with pytest.raises(ValueError, match="Forbidden virtual chunk container url_prefix"):
                client.get_repo(repo_name, authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname})

    async def test_import_existing_repo(
        self,
        isolated_org,
        default_bucket,
        minio_anon_bucket,
        token,
        unsafe_url_prefix,
        ic_store,
    ):
        repo_bucket = default_bucket()
        virtual_bucket = minio_anon_bucket()

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=unsafe_url_prefix,
                store=ic_store,
            )
            config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=config)
            ic_repo.save_config()

            # attempt to import existing unsafe repo
            with pytest.raises(ValueError, match="Forbidden virtual chunk container url_prefix"):
                # TODO also detect the unsafe containers when auto-discovery is implemented?
                client.create_repo(
                    repo_name,
                    prefix=repo_prefix,
                    import_existing=True,
                    authorize_virtual_chunk_access={unsafe_url_prefix: virtual_bucket.nickname},
                )

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))


@pytest.mark.parametrize(
    "unsafe_virtual_bucket_config, expected_err_msg",
    [
        ("default_bucket", "uses HMAC credentials"),  # default bucket is a HMAC bucket
        (
            "delegated_creds_bucket",
            "does not support anonymous public access",
        ),
    ],
)
@pytest.mark.asyncio
class TestForbidUnsafeBucketConfigs:
    """Check that any method of creating an AL repo with virtual chunks detects any potentially insecure bucket configs."""

    async def test_create_repo(
        self,
        isolated_org,
        default_bucket,
        unsafe_virtual_bucket_config,
        expected_err_msg,
        request,
        token,
    ):
        unsafe_virtual_bucket_config = request.getfixturevalue(unsafe_virtual_bucket_config)

        repo_bucket = default_bucket()
        virtual_bucket = unsafe_virtual_bucket_config(name="unsafebucket", nickname="myunsafebucket")
        vcc_url_prefix = "s3://" + virtual_bucket.name + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            with pytest.raises(ValueError, match=f"Cannot use virtual chunk references that refer to a bucket which {expected_err_msg}"):
                client.create_repo(repo_name, authorize_virtual_chunk_access={vcc_url_prefix: virtual_bucket.nickname})

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))

    async def test_get_repo(self, isolated_org, default_bucket, unsafe_virtual_bucket_config, expected_err_msg, request, token):
        unsafe_virtual_bucket_config = request.getfixturevalue(unsafe_virtual_bucket_config)

        repo_bucket = default_bucket()
        virtual_bucket = unsafe_virtual_bucket_config(name="unsafebucket", nickname="unsafebucket")
        url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            # Create the repo without virtual chunk containers
            repo_name = f"{org_name}/foo"
            repo = client.create_repo(repo_name, bucket_config_nickname=repo_bucket.nickname)

            # Manually set a virtual chunk container on the icechunk repo directly
            # We will also separately forbid doing this with the Arraylake client, but we can't stop a canny bad guy doing it using IC manually
            config = repo.config
            container = icechunk.VirtualChunkContainer(
                url_prefix=url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            repo = repo.reopen(config=config)
            repo.save_config()

            # attempt to get unsafe repo
            with pytest.raises(ValueError, match=f"Cannot use virtual chunk references that refer to a bucket which {expected_err_msg}"):
                client.get_repo(repo_name, authorize_virtual_chunk_access={url_prefix: virtual_bucket.nickname})

    async def test_import_existing_repo(self, isolated_org, default_bucket, unsafe_virtual_bucket_config, expected_err_msg, request, token):
        unsafe_virtual_bucket_config = request.getfixturevalue(unsafe_virtual_bucket_config)

        repo_bucket = default_bucket()
        virtual_bucket = unsafe_virtual_bucket_config(name="unsafebucket", nickname="unsafebucket")
        url_prefix = "s3://" + virtual_bucket.name + virtual_bucket.prefix + "/"

        client = Client(token=token)
        async with isolated_org(repo_bucket, virtual_bucket) as (org_name, buckets):
            repo_name = f"{org_name}/foo"

            # Use icechunk to create the repo outside of the arraylake client
            # IDK a better way to set up the storage for this, hardcoding for now
            repo_prefix = str(uuid4())[:8]
            ic_storage = icechunk.s3_storage(
                bucket=repo_bucket.name,
                prefix=repo_prefix,
                region="us-east-1",
                endpoint_url="http://localhost:9000",
                allow_http=True,
                access_key_id="minio123",
                secret_access_key="minio123",
                force_path_style=True,
            )
            ic_repo = icechunk.Repository.create(storage=ic_storage)

            # Manually set a virtual chunk container on the icechunk repo directly
            config = icechunk.RepositoryConfig.default()
            container = icechunk.VirtualChunkContainer(
                url_prefix=url_prefix,
                store=icechunk.s3_store(),
            )
            config.set_virtual_chunk_container(container)
            ic_repo = ic_repo.reopen(config=config)
            ic_repo.save_config()

            # attempt to import existing unsafe repo
            with pytest.raises(ValueError, match=f"Cannot use virtual chunk references that refer to a bucket which {expected_err_msg}"):
                # TODO also detect the unsafe containers when auto-discovery is implemented?
                client.create_repo(
                    repo_name,
                    prefix=repo_prefix,
                    import_existing=True,
                    authorize_virtual_chunk_access={url_prefix: virtual_bucket.nickname},
                )

            assert not any(repo.name == "foo" for repo in client.list_repos(org_name))
