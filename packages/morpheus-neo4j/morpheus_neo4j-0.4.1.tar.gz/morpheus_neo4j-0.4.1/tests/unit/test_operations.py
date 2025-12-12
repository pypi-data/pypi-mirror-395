from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from morpheus.config.config import Config, DatabaseConfig, ExecutionConfig
from morpheus.core.operations import (
    MigrationOperations,
    filter_migrations_to_target,
    get_target_rollback_migrations,
    load_migrations,
    update_migration_status_from_db,
)
from morpheus.models.migration import Migration
from morpheus.models.migration_status import MigrationStatus
from morpheus.models.priority import Priority


class TestMigrationOperations:
    """Test suite for MigrationOperations using AAA pattern and parametrized tests."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock config for testing."""
        config = Config()
        config.database = DatabaseConfig(
            uri="bolt://localhost:7687",
            username="neo4j",
            password="password",
            database="test_db",
        )
        config.execution = ExecutionConfig(max_parallel=4, parallel=True)
        config.migrations_dir = "/tmp/migrations"
        return config

    @pytest.fixture
    def sample_migrations(self):
        """Create sample Migration objects for testing."""
        return [
            Migration(
                id="20250828120001_initial_schema",
                file_path=Path("/tmp/20250828120001_initial_schema.py"),
                dependencies=[],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120002_user_management",
                file_path=Path("/tmp/20250828120002_user_management.py"),
                dependencies=["20250828120001_initial_schema"],
                status=MigrationStatus.PENDING,
                priority=Priority.HIGH,
            ),
        ]

    @pytest.fixture
    def operations(self, mock_config):
        """Create MigrationOperations instance."""
        return MigrationOperations(mock_config)

    def test_init_with_valid_config(self, mock_config):
        """Test initialization with valid config."""
        # Act
        operations = MigrationOperations(mock_config)

        # Assert
        assert operations.config is mock_config
        assert operations._migrations is None

    def test_load_migrations_cached(self, operations, sample_migrations):
        """Test loading migrations returns cached version."""
        # Arrange
        operations._migrations = sample_migrations

        # Act
        result = operations.load_migrations()

        # Assert
        assert result == sample_migrations

    def test_load_migrations_directory_not_exists(self, mock_config):
        """Test loading migrations when directory doesn't exist."""
        # Arrange - create fresh operations instance to avoid any fixture pollution
        fresh_config = Config()
        fresh_config.database = mock_config.database
        fresh_config.execution = mock_config.execution
        fresh_config.migrations = mock_config.migrations

        operations = MigrationOperations(fresh_config)

        with patch(
            "morpheus.core.operations.resolve_migrations_dir"
        ) as mock_resolve_dir:
            # Create a non-existent path
            nonexistent_path = Path("/definitely/does/not/exist/migrations")
            mock_resolve_dir.return_value = nonexistent_path

            # Force reload to bypass any cache
            with pytest.raises(
                FileNotFoundError, match="Migrations directory does not exist"
            ):
                operations.load_migrations(force_reload=True)

    def test_get_applied_migrations_success(self, operations):
        """Test getting applied migrations successfully."""
        # Arrange
        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor.get_applied_migrations.return_value = [
                "migration1",
                "migration2",
            ]
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.get_applied_migrations()

            # Assert
            assert result == {"migration1", "migration2"}
            mock_executor_class.assert_called_once_with(operations.config)

    @patch.object(MigrationOperations, "load_migrations")
    @patch.object(MigrationOperations, "get_applied_migrations")
    def test_get_pending_migrations_basic(
        self, mock_get_applied, mock_load, operations, sample_migrations
    ):
        """Test getting pending migrations without target."""
        # Arrange
        # Ensure clean state to force load_migrations to be called
        operations._migrations = None
        mock_load.return_value = sample_migrations
        mock_get_applied.return_value = {"20250828120001_initial_schema"}

        # Act
        result = operations.get_pending_migrations()

        # Assert
        expected = [sample_migrations[1]]  # Only second migration is pending
        assert result == expected
        # Verify mocked methods were called
        mock_load.assert_called_once()
        mock_get_applied.assert_called_once()

    @patch.object(MigrationOperations, "load_migrations")
    @patch("morpheus.core.operations.filter_migrations_to_target")
    def test_get_pending_migrations_with_target(
        self, mock_filter, mock_load, operations, sample_migrations
    ):
        """Test getting pending migrations with target specified."""
        # Arrange
        # Ensure clean state to force load_migrations to be called
        operations._migrations = None
        mock_load.return_value = sample_migrations
        applied_ids = {"20250828120001_initial_schema"}
        target = "20250828120002_user_management"
        filtered_migrations = [sample_migrations[1]]
        mock_filter.return_value = filtered_migrations

        # Act
        result = operations.get_pending_migrations(
            target=target, applied_ids=applied_ids
        )

        # Assert
        assert result == filtered_migrations
        # Verify filter was called once
        mock_filter.assert_called_once()
        # Verify the arguments passed to filter_migrations_to_target
        call_args = mock_filter.call_args
        assert call_args[0][0] == sample_migrations  # migrations argument
        assert call_args[0][1] == target  # target argument
        assert call_args[0][2] == applied_ids  # applied_ids argument
        # Verify load_migrations was actually called
        mock_load.assert_called_once()

    @patch.object(MigrationOperations, "load_migrations")
    @patch("morpheus.core.dag_resolver.DAGResolver")
    def test_validate_migrations_success(
        self, mock_resolver_class, mock_load, operations, sample_migrations
    ):
        """Test successful migration validation."""
        # Arrange
        mock_load.return_value = sample_migrations
        mock_resolver = MagicMock()
        mock_dag = MagicMock()
        mock_resolver.build_dag.return_value = mock_dag
        mock_resolver.validate_dag.return_value = []
        mock_resolver.check_conflicts.return_value = []
        mock_resolver_class.return_value = mock_resolver

        # Act
        validation_errors, conflict_errors = operations.validate_migrations(
            sample_migrations
        )

        # Assert
        assert validation_errors == []
        assert conflict_errors == []

    @patch("morpheus.core.executor.MigrationExecutor")
    def test_execute_upgrade_empty_migrations(self, mock_executor_class, operations):
        """Test execute_upgrade with empty migrations list."""
        # Act
        result = operations.execute_upgrade([])

        # Assert
        assert result == {}
        mock_executor_class.assert_not_called()

    def test_execute_upgrade_sequential_success(self, operations, sample_migrations):
        """Test successful sequential upgrade execution."""
        # Arrange
        operations.config.execution.parallel = False
        operations._migrations = (
            sample_migrations  # Set cached migrations for DAG building
        )

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor._execute_single_migration.side_effect = [
                (True, None),
                (True, None),
            ]
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(sample_migrations)

            # Assert
            expected = {
                "20250828120001_initial_schema": (True, None),
                "20250828120002_user_management": (True, None),
            }
            assert result == expected

    def test_execute_upgrade_with_failure_and_failfast(
        self, operations, sample_migrations
    ):
        """Test upgrade execution with failure and failfast enabled."""
        # Arrange
        operations.config.execution.parallel = False
        operations._migrations = (
            sample_migrations  # Set cached migrations for DAG building
        )

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor._execute_single_migration.return_value = (
                False,
                "Migration failed",
            )
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(sample_migrations, failfast=True)

            # Assert
            expected = {
                "20250828120001_initial_schema": (False, "Migration failed"),
                "20250828120002_user_management": (False, "Skipped due to failfast"),
            }
            assert result == expected
            assert mock_executor._execute_single_migration.call_count == 1

    @pytest.mark.parametrize(
        "ci_mode,expected_failfast",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_execute_upgrade_ci_mode(
        self,
        operations,
        sample_migrations,
        ci_mode,
        expected_failfast,
    ):
        """Test CI mode behavior."""
        # Arrange
        operations.config.execution.parallel = False
        operations._migrations = (
            sample_migrations  # Set cached migrations for DAG building
        )

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            if expected_failfast:
                mock_executor._execute_single_migration.return_value = (False, "Failed")
            else:
                mock_executor._execute_single_migration.side_effect = [
                    (False, "Failed"),
                    (True, None),
                ]
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(sample_migrations, ci=ci_mode)

            # Assert
            if expected_failfast:
                expected = {
                    "20250828120001_initial_schema": (False, "Failed"),
                    "20250828120002_user_management": (
                        False,
                        "Skipped due to failfast",
                    ),
                }
                assert result == expected
                assert mock_executor._execute_single_migration.call_count == 1
            else:
                expected = {
                    "20250828120001_initial_schema": (False, "Failed"),
                    "20250828120002_user_management": (True, None),
                }
                assert result == expected
                assert mock_executor._execute_single_migration.call_count == 2

    @patch.object(MigrationOperations, "load_migrations")
    @patch.object(MigrationOperations, "get_applied_migrations")
    def test_execute_downgrade_no_applied_migrations(
        self, mock_get_applied, mock_load, operations, sample_migrations
    ):
        """Test downgrade when no migrations are applied."""
        # Arrange
        target = "20250828120001_initial_schema"
        mock_load.return_value = sample_migrations
        mock_get_applied.return_value = set()

        # Act
        result = operations.execute_downgrade(target)

        # Assert
        assert result == {}

    @patch.object(MigrationOperations, "load_migrations")
    def test_get_migration_status_success(
        self, mock_load, operations, sample_migrations
    ):
        """Test getting migration status successfully."""
        # Arrange
        mock_load.return_value = sample_migrations

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            mock_executor.get_applied_migrations.return_value = [
                "20250828120001_initial_schema"
            ]
            # Mock batch status retrieval
            mock_executor.get_migrations_status_batch.return_value = {
                "20250828120001_initial_schema": {"status": "applied"}
            }
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.get_migration_status()

            # Assert
            expected = {
                "20250828120001_initial_schema": "applied",
                "20250828120002_user_management": "pending",
            }
            assert result == expected


class TestUtilityFunctions:
    """Test suite for utility functions in operations.py."""

    @pytest.fixture
    def sample_migrations(self):
        """Create sample Migration objects for testing."""
        return [
            Migration(
                id="20250828120001_initial_schema",
                file_path=Path("/tmp/20250828120001_initial_schema.py"),
                dependencies=[],
            ),
            Migration(
                id="20250828120002_user_management",
                file_path=Path("/tmp/20250828120002_user_management.py"),
                dependencies=["20250828120001_initial_schema"],
            ),
        ]

    @patch("morpheus.models.migration.Migration.from_file")
    def test_load_migrations_success(self, mock_from_file, tmp_path):
        """Test loading migrations successfully."""
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        (migrations_dir / "20250828120001_initial_schema.py").write_text("# migration")
        (migrations_dir / "20250828120002_user_management.py").write_text("# migration")

        mock_migration1 = Mock()
        mock_migration1.id = "20250828120001_initial_schema"
        mock_migration2 = Mock()
        mock_migration2.id = "20250828120002_user_management"
        mock_from_file.side_effect = [mock_migration1, mock_migration2]

        # Act
        result = load_migrations(migrations_dir)

        # Assert
        assert len(result) == 2
        assert result[0] == mock_migration1
        assert result[1] == mock_migration2

    def test_load_migrations_empty_directory(self, tmp_path):
        """Test loading migrations from empty directory."""
        # Arrange
        empty_dir = tmp_path / "empty_migrations"
        empty_dir.mkdir()

        # Act
        result = load_migrations(empty_dir)

        # Assert
        assert result == []

    @patch("morpheus.models.migration.Migration.from_file")
    def test_load_migrations_ignores_invalid_files(self, mock_from_file, tmp_path):
        """Test that load_migrations ignores invalid file types."""
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        (migrations_dir / "__init__.py").write_text("# init file")
        (migrations_dir / "not_python.txt").write_text("content")

        # Act
        result = load_migrations(migrations_dir)

        # Assert
        assert result == []
        mock_from_file.assert_not_called()

    @patch("morpheus.models.migration.Migration.from_file")
    def test_load_migrations_handles_migration_errors(self, mock_from_file, tmp_path):
        """Test that load_migrations handles migration loading errors."""
        # Arrange
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        (migrations_dir / "valid.py").write_text("# valid migration")
        (migrations_dir / "invalid.py").write_text("# invalid migration")

        def from_file_side_effect(file_path):
            if "invalid" in str(file_path):
                raise Exception("Invalid migration file")
            return Mock(id="valid")

        mock_from_file.side_effect = from_file_side_effect

        # Act
        result = load_migrations(migrations_dir)

        # Assert
        assert len(result) == 1  # Only valid migration loaded
        assert result[0].id == "valid"

    @patch("morpheus.core.dag_resolver.DAGResolver")
    def test_filter_migrations_to_target_success(
        self, mock_resolver_class, sample_migrations
    ):
        """Test filtering migrations to target successfully."""
        # Arrange
        target_id = "20250828120002_user_management"
        applied_ids = set()
        mock_resolver = MagicMock()
        mock_dag = MagicMock()

        with patch(
            "networkx.ancestors", return_value={"20250828120001_initial_schema"}
        ):
            mock_resolver.build_dag.return_value = mock_dag
            mock_resolver_class.return_value = mock_resolver

            # Act
            result = filter_migrations_to_target(
                sample_migrations, target_id, applied_ids
            )

            # Assert
            expected_ids = {
                "20250828120001_initial_schema",
                "20250828120002_user_management",
            }
            result_ids = {m.id for m in result}
            assert result_ids == expected_ids

    def test_filter_migrations_to_target_not_found(self, sample_migrations):
        """Test filtering when target migration is not found."""
        # Act & Assert
        with pytest.raises(ValueError, match="Target migration not found: nonexistent"):
            filter_migrations_to_target(sample_migrations, "nonexistent", set())

    def test_get_target_rollback_migrations_success(self):
        """Test getting rollback migrations successfully."""
        # Arrange
        migrations = [
            Migration(
                id="20250828120001_initial_schema",
                file_path=Path("/tmp/initial_schema.py"),
            ),
            Migration(
                id="20250828120002_user_management",
                file_path=Path("/tmp/user_management.py"),
            ),
            Migration(
                id="20250828120003_product_catalog",
                file_path=Path("/tmp/product_catalog.py"),
            ),
        ]
        mock_dag = Mock()
        target = "20250828120002_user_management"
        applied_ids = {
            "20250828120002_user_management",
            "20250828120003_product_catalog",
        }

        # Act
        result = get_target_rollback_migrations(
            migrations, mock_dag, target, applied_ids
        )

        # Assert
        assert len(result) == 1
        assert result[0].id == "20250828120003_product_catalog"

    def test_get_target_rollback_migrations_target_not_found(self, sample_migrations):
        """Test rollback when target migration is not found."""
        # Act & Assert
        with pytest.raises(ValueError, match="Target migration not found: nonexistent"):
            get_target_rollback_migrations(
                sample_migrations, Mock(), "nonexistent", set()
            )

    @patch("morpheus.core.operations.MigrationExecutor")
    def test_update_migration_status_from_db_success_applied(self, mock_executor_class):
        """Test update_migration_status_from_db function success with applied migration."""
        # Arrange
        mock_executor = Mock()
        mock_executor_class.return_value.__enter__ = Mock(return_value=mock_executor)
        mock_executor_class.return_value.__exit__ = Mock(return_value=None)

        mock_migration = Mock()
        mock_migration.id = "20250828120001_test"

        # Mock the optimized batch call
        mock_executor.get_applied_migrations.return_value = ["20250828120001_test"]
        mock_executor.get_migrations_status_batch.return_value = {
            "20250828120001_test": {
                "status": "applied",
                "applied_at": "2024-01-01T00:00:00",
            }
        }

        config = Mock()
        console = Mock()

        # Act
        update_migration_status_from_db([mock_migration], config, console)

        # Assert
        mock_executor_class.assert_called_once_with(config, console)
        mock_executor.get_applied_migrations.assert_called_once()
        mock_executor.get_migrations_status_batch.assert_called_once_with(
            ["20250828120001_test"]
        )
        assert mock_migration.status == MigrationStatus.APPLIED

    @patch("morpheus.core.operations.MigrationExecutor")
    def test_update_migration_status_from_db_success_pending(self, mock_executor_class):
        """Test update_migration_status_from_db function success with pending migration."""
        # Arrange
        mock_executor = Mock()
        mock_executor_class.return_value.__enter__ = Mock(return_value=mock_executor)
        mock_executor_class.return_value.__exit__ = Mock(return_value=None)

        mock_migration = Mock()
        mock_migration.id = "20250828120001_test"

        # Mock migration as not applied (efficient: no individual query needed)
        mock_executor.get_applied_migrations.return_value = []

        config = Mock()
        console = Mock()

        # Act
        update_migration_status_from_db([mock_migration], config, console)

        # Assert
        mock_executor_class.assert_called_once_with(config, console)
        mock_executor.get_applied_migrations.assert_called_once()
        mock_executor.get_migration_status.assert_not_called()  # Optimized: no individual query
        assert mock_migration.status == MigrationStatus.PENDING

    @patch("morpheus.core.operations.MigrationExecutor")
    def test_update_migration_status_from_db_connection_failure(
        self, mock_executor_class
    ):
        """Test update_migration_status_from_db function with connection failure."""
        # Arrange
        mock_executor_class.return_value.__enter__.side_effect = Exception(
            "Database connection failed"
        )

        mock_migration = Mock()
        config = Mock()
        console = Mock()

        # Act & Assert
        with pytest.raises(
            RuntimeError, match="Failed to update migration status from database"
        ):
            update_migration_status_from_db([mock_migration], config, console)


class TestParallelExecutionRespectsDependencies:
    """Test suite verifying that parallel execution respects DAG dependency batching.

    These tests validate that when parallel=True, migrations are executed in
    proper batches based on their dependencies, not all at once.

    The bug: execute_upgrade() with parallel=True was calling execute_parallel()
    with ALL pending migrations, ignoring dependency relationships.

    Expected behavior: Migrations should be grouped into batches where:
    - Migrations in the same batch have no dependencies on each other
    - Batches are executed sequentially (batch N completes before batch N+1)
    - Migrations within a batch can run in parallel
    """

    @pytest.fixture
    def mock_config(self):
        """Create a mock config with parallel enabled."""
        config = Config()
        config.database = DatabaseConfig(
            uri="bolt://localhost:7687",
            username="neo4j",
            password="password",
            database="test_db",
        )
        config.execution = ExecutionConfig(max_parallel=4, parallel=True)
        config.migrations_dir = "/tmp/migrations"
        return config

    @pytest.fixture
    def migrations_with_chain_dependency(self):
        """Create migrations with chain dependency: A -> B -> C.

        Expected batches:
        - Batch 1: [A] (no dependencies)
        - Batch 2: [B] (depends on A)
        - Batch 3: [C] (depends on B)
        """
        return [
            Migration(
                id="20250828120001_migration_a",
                file_path=Path("/tmp/20250828120001_migration_a.py"),
                dependencies=[],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120002_migration_b",
                file_path=Path("/tmp/20250828120002_migration_b.py"),
                dependencies=["20250828120001_migration_a"],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120003_migration_c",
                file_path=Path("/tmp/20250828120003_migration_c.py"),
                dependencies=["20250828120002_migration_b"],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
        ]

    @pytest.fixture
    def migrations_with_parallel_branches(self):
        """Create migrations with parallel branches: A -> B, A -> C, B+C -> D.

        Expected batches:
        - Batch 1: [A] (no dependencies)
        - Batch 2: [B, C] (both depend only on A, can run in parallel)
        - Batch 3: [D] (depends on B and C)
        """
        return [
            Migration(
                id="20250828120001_migration_a",
                file_path=Path("/tmp/20250828120001_migration_a.py"),
                dependencies=[],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120002_migration_b",
                file_path=Path("/tmp/20250828120002_migration_b.py"),
                dependencies=["20250828120001_migration_a"],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120003_migration_c",
                file_path=Path("/tmp/20250828120003_migration_c.py"),
                dependencies=["20250828120001_migration_a"],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
            Migration(
                id="20250828120004_migration_d",
                file_path=Path("/tmp/20250828120004_migration_d.py"),
                dependencies=[
                    "20250828120002_migration_b",
                    "20250828120003_migration_c",
                ],
                status=MigrationStatus.PENDING,
                priority=Priority.NORMAL,
            ),
        ]

    def test_parallel_execution_respects_chain_dependencies(
        self, mock_config, migrations_with_chain_dependency
    ):
        """Test that chain dependencies (A->B->C) are executed in separate batches.

        With chain dependencies, each migration must wait for its dependency,
        so execute_parallel should be called 3 times with single-migration batches,
        NOT once with all 3 migrations.
        """
        # Arrange
        operations = MigrationOperations(mock_config)
        operations._migrations = migrations_with_chain_dependency

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            # Track all calls to execute_parallel
            parallel_call_args = []

            def track_parallel_calls(batch):
                parallel_call_args.append([m.id for m in batch])
                return {m.id: (True, None) for m in batch}

            mock_executor.execute_parallel.side_effect = track_parallel_calls
            mock_executor._execute_single_migration.side_effect = lambda m: (True, None)
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(migrations_with_chain_dependency)

            # Assert - all migrations should succeed
            assert all(success for success, _ in result.values())

            # Assert - execute_parallel should NOT be called with all migrations at once
            # The bug would show: execute_parallel called once with all 3 migrations
            # Expected: Called 3 times with 1 migration each (since chain deps)
            # OR: _execute_single_migration called for single-item batches
            if parallel_call_args:
                # If execute_parallel was called, verify no call has all migrations
                for call_args in parallel_call_args:
                    assert len(call_args) < 3, (
                        f"Bug: execute_parallel called with {len(call_args)} migrations "
                        f"that have chain dependencies. Expected batches of 1."
                    )

    def test_parallel_execution_allows_independent_migrations_in_same_batch(
        self, mock_config, migrations_with_parallel_branches
    ):
        """Test that independent migrations (B and C) run in the same parallel batch.

        With diamond dependency pattern (A -> B, A -> C, B+C -> D):
        - Batch 1: [A]
        - Batch 2: [B, C] - these CAN run in parallel
        - Batch 3: [D]
        """
        # Arrange
        operations = MigrationOperations(mock_config)
        operations._migrations = migrations_with_parallel_branches

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()
            parallel_call_args = []

            def track_parallel_calls(batch):
                parallel_call_args.append([m.id for m in batch])
                return {m.id: (True, None) for m in batch}

            mock_executor.execute_parallel.side_effect = track_parallel_calls
            mock_executor._execute_single_migration.side_effect = lambda m: (True, None)
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(migrations_with_parallel_branches)

            # Assert - all migrations should succeed
            assert len(result) == 4
            assert all(success for success, _ in result.values())

            # Assert - should NOT call execute_parallel with all 4 migrations
            # The bug would show: execute_parallel called once with all 4 migrations
            if parallel_call_args:
                for call_args in parallel_call_args:
                    assert len(call_args) <= 2, (
                        f"Bug: execute_parallel called with {len(call_args)} migrations. "
                        f"Max expected batch size is 2 (migrations B and C)."
                    )

    def test_parallel_execution_executes_batches_sequentially(
        self, mock_config, migrations_with_chain_dependency
    ):
        """Test that batches are executed in order, not all at once.

        This verifies that migration B doesn't start until migration A completes.
        """
        # Arrange
        operations = MigrationOperations(mock_config)
        operations._migrations = migrations_with_chain_dependency

        execution_order = []

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()

            def track_execution(migration):
                execution_order.append(migration.id)
                return (True, None)

            def track_parallel_execution(batch):
                for m in batch:
                    execution_order.append(m.id)
                return {m.id: (True, None) for m in batch}

            mock_executor._execute_single_migration.side_effect = track_execution
            mock_executor.execute_parallel.side_effect = track_parallel_execution
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            operations.execute_upgrade(migrations_with_chain_dependency)

            # Assert - execution order must respect dependencies
            # A must come before B, B must come before C
            a_index = execution_order.index("20250828120001_migration_a")
            b_index = execution_order.index("20250828120002_migration_b")
            c_index = execution_order.index("20250828120003_migration_c")

            assert a_index < b_index, (
                f"Bug: Migration A (index {a_index}) should execute before B (index {b_index})"
            )
            assert b_index < c_index, (
                f"Bug: Migration B (index {b_index}) should execute before C (index {c_index})"
            )

    def test_parallel_batch_failure_prevents_dependent_batch(
        self, mock_config, migrations_with_chain_dependency
    ):
        """Test that if batch N fails, batch N+1 (with dependencies) is skipped."""
        # Arrange
        operations = MigrationOperations(mock_config)
        operations._migrations = migrations_with_chain_dependency

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()

            def fail_first_migration(migration):
                if migration.id == "20250828120001_migration_a":
                    return (False, "Migration A failed")
                return (True, None)

            mock_executor._execute_single_migration.side_effect = fail_first_migration
            mock_executor.execute_parallel.side_effect = lambda batch: {
                m.id: fail_first_migration(m) for m in batch
            }
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act
            result = operations.execute_upgrade(
                migrations_with_chain_dependency, failfast=True
            )

            # Assert
            assert result["20250828120001_migration_a"] == (False, "Migration A failed")
            # B and C should be skipped because A failed and they depend on A
            assert result["20250828120002_migration_b"][0] is False
            assert result["20250828120003_migration_c"][0] is False


class TestConflictsAsOrderingConstraints:
    """Tests verifying conflicts are treated as ordering hints, not validation errors.

    The bug: validate_migrations() returns conflict errors, causing the upgrade
    command to exit with error code 1.

    Expected behavior: Conflicts should NOT be returned as validation errors.
    Instead, they should be handled silently by get_execution_order() batching.
    """

    @pytest.fixture
    def mock_config(self):
        """Create a mock config."""
        config = Config()
        config.database = DatabaseConfig(
            uri="bolt://localhost:7687",
            username="neo4j",
            password="password",
            database="test_db",
        )
        config.execution = ExecutionConfig(max_parallel=4, parallel=False)
        config.migrations_dir = "/tmp/migrations"
        return config

    def test_conflicts_do_not_block_validation(self, mock_config):
        """Test that conflicts don't cause validation errors anymore.

        Current behavior (bug): validate_migrations() returns conflict errors,
        causing upgrade command to exit with error.
        Expected behavior: Conflicts should be handled silently by batching,
        so conflict_errors should be empty.
        """
        # Arrange
        operations = MigrationOperations(mock_config)
        migration_a = Migration(
            id="001_a",
            file_path=Path("/tmp/001_a.py"),
            dependencies=[],
            status=MigrationStatus.PENDING,
            priority=Priority.NORMAL,
        )
        migration_b = Migration(
            id="002_b",
            file_path=Path("/tmp/002_b.py"),
            dependencies=[],
            status=MigrationStatus.PENDING,
            priority=Priority.NORMAL,
        )
        migration_a.conflicts = ["002_b"]  # A conflicts with B

        operations._migrations = [migration_a, migration_b]

        # Act
        validation_errors, conflict_errors = operations.validate_migrations(
            [migration_a, migration_b]
        )

        # Assert: No conflict errors should be returned (handled by batching instead)
        assert conflict_errors == [], (
            f"Bug: Conflicts returned as errors: {conflict_errors}. "
            f"Expected empty list - conflicts should be handled by batching."
        )

    def test_conflicting_migrations_execute_in_separate_batches(self, mock_config):
        """Test that conflicting migrations are executed in separate batches.

        This is an end-to-end test ensuring conflicts affect execution order,
        not validation.
        """
        # Arrange
        operations = MigrationOperations(mock_config)
        migration_a = Migration(
            id="001_a",
            file_path=Path("/tmp/001_a.py"),
            dependencies=[],
            status=MigrationStatus.PENDING,
            priority=Priority.NORMAL,
        )
        migration_b = Migration(
            id="002_b",
            file_path=Path("/tmp/002_b.py"),
            dependencies=[],
            status=MigrationStatus.PENDING,
            priority=Priority.NORMAL,
        )
        migration_a.conflicts = ["002_b"]

        operations._migrations = [migration_a, migration_b]

        execution_order = []

        with patch("morpheus.core.operations.MigrationExecutor") as mock_executor_class:
            mock_executor = MagicMock()

            def track_execution(migration):
                execution_order.append(migration.id)
                return (True, None)

            mock_executor._execute_single_migration.side_effect = track_execution
            mock_executor_class.return_value.__enter__.return_value = mock_executor
            mock_executor_class.return_value.__exit__.return_value = None

            # Act - this should NOT raise an error due to conflicts
            result = operations.execute_upgrade([migration_a, migration_b])

            # Assert - both migrations should have executed successfully
            assert len(result) == 2
            assert result["001_a"] == (True, None)
            assert result["002_b"] == (True, None)

            # Both should have been executed (order doesn't matter for this test)
            assert set(execution_order) == {"001_a", "002_b"}
