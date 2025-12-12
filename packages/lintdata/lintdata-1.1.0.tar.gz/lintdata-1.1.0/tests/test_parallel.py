"""Tests for parallel execution functionality."""

import pandas as pd
import pytest

from lintdata.parallel import JOBLIB_AVAILABLE, ParallelExecutor, get_optimal_workers


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "A": [1, 2, None, 4, 5],
            "B": ["a", "b", "c", "d", "e"],
            "C": [1.0, 2.0, 3.0, 4.0, 5.0],
        }
    )


@pytest.fixture
def sample_checks():
    """Create sample check functions."""

    def check_missing(df):
        """Check for missing values."""
        missing = df.isna().sum()
        if missing.any():
            return [f"Found {missing.sum()} missing values"]
        return []

    def check_duplicates(df):
        """Check for duplicate rows."""
        dupes = df.duplicated().sum()
        if dupes > 0:
            return [f"Found {dupes} duplicate rows"]
        return []

    def check_negatives(df):
        """Check for negative values."""
        numeric_cols = df.select_dtypes(include=["number"]).columns
        has_negatives = (df[numeric_cols] < 0).any().any()
        if has_negatives:
            return ["Found negative values"]
        return []

    return [check_missing, check_duplicates, check_negatives]


class TestParallelExecutor:
    """Test ParallelExecutor class."""

    def test_init_default(self):
        """Test default initialisation."""
        executor = ParallelExecutor()
        assert executor.n_jobs > 0
        assert executor.backend == "multiprocessing"
        assert executor.min_checks_for_parallel == 3

    def test_init_custom_workers(self):
        """Test initialisation with custom n_jobs."""
        executor = ParallelExecutor(n_jobs=4)
        assert executor.n_jobs == 4

    def test_init_all_cores(self):
        """Test initialisation with n_jobs=-1."""
        executor = ParallelExecutor(n_jobs=-1)
        assert executor.n_jobs > 0

    def test_init_invalid_workers(self):
        """Test initialisation with invalid n_jobs."""
        with pytest.raises(ValueError, match="n_jobs must be -1 or a positive integer"):
            ParallelExecutor(n_jobs=0)

        with pytest.raises(ValueError, match="n_jobs must be -1 or a positive integer"):
            ParallelExecutor(n_jobs=-2)

    def test_init_threading_backend(self):
        """Test initialisation with threading backend."""
        executor = ParallelExecutor(backend="threading")
        assert executor.backend == "threading"

    @pytest.mark.skipif(not JOBLIB_AVAILABLE, reason="joblib not installed")
    def test_init_joblib_backend(self):
        """Test initialisation with joblib backend."""
        executor = ParallelExecutor(backend="joblib")
        assert executor.backend == "joblib"

    @pytest.mark.skipif(JOBLIB_AVAILABLE, reason="joblib is installed")
    def test_init_joblib_backend_not_installed(self):
        """Test initialisation with joblib backend when not installed."""
        with pytest.raises(ImportError, match="joblib backend requires joblib"):
            ParallelExecutor(backend="joblib")

    def test_should_parallelise_too_few_checks(self):
        """Test that parallelisation is disabled for too few checks."""
        executor = ParallelExecutor(min_checks_for_parallel=3)
        assert not executor.should_parallelise(n_checks=2, df_size=10000)

    def test_should_parallelise_small_dataframe(self):
        """Test that parallelisation is disabled for small DataFrames."""
        executor = ParallelExecutor()
        assert not executor.should_parallelise(n_checks=5, df_size=100)

    def test_should_parallelise_serial_mode(self):
        """Test that parallelisation is disabled when n_jobs=1."""
        executor = ParallelExecutor(n_jobs=1)
        assert not executor.should_parallelise(n_checks=10, df_size=10000)

    def test_should_parallelise_valid_case(self):
        """Test that parallelisation is enabled for valid cases."""
        executor = ParallelExecutor(n_jobs=4, min_checks_for_parallel=3)
        assert executor.should_parallelise(n_checks=5, df_size=10000)

    def test_execute_serial(self, sample_df, sample_checks):
        """Test serial execution."""
        executor = ParallelExecutor(n_jobs=1)
        results = executor.execute_checks(sample_checks, sample_df)

        assert "check_missing" in results
        assert "check_duplicates" in results
        assert "check_negatives" in results
        assert len(results["check_missing"]) > 0  # Should find missing values

    def test_execute_multiprocessing(self, sample_df, sample_checks):
        """Test multiprocessing execution."""
        executor = ParallelExecutor(n_jobs=2, backend="multiprocessing")

        # Force parallel execution
        executor.min_checks_for_parallel = 1
        results = executor.execute_checks(sample_checks, sample_df)

        assert "check_missing" in results
        assert "check_duplicates" in results
        assert "check_negatives" in results

    def test_execute_threading(self, sample_df, sample_checks):
        """Test threading execution."""
        executor = ParallelExecutor(n_jobs=2, backend="threading")

        # Force parallel execution
        executor.min_checks_for_parallel = 1
        results = executor.execute_checks(sample_checks, sample_df)

        assert "check_missing" in results
        assert "check_duplicates" in results
        assert "check_negatives" in results

    @pytest.mark.skipif(not JOBLIB_AVAILABLE, reason="joblib not installed")
    def test_execute_joblib(self, sample_df, sample_checks):
        """Test joblib execution."""
        executor = ParallelExecutor(n_jobs=2, backend="joblib")

        # Force parallel execution
        executor.min_checks_for_parallel = 1
        results = executor.execute_checks(sample_checks, sample_df)

        assert "check_missing" in results
        assert "check_duplicates" in results
        assert "check_negatives" in results

    def test_execute_with_check_kwargs(self, sample_df):
        """Test execution with check keyword arguments."""

        def check_with_threshold(df, threshold=0):
            """Check with threshold parameter."""
            numeric_cols = df.select_dtypes(include=["number"]).columns
            max_val = df[numeric_cols].max().max()
            if max_val > threshold:
                return [f"Max value {max_val} exceeds threshold {threshold}"]
            return []

        executor = ParallelExecutor(n_jobs=1)
        check_kwargs = {"check_with_threshold": {"threshold": 3}}

        results = executor.execute_checks([check_with_threshold], sample_df, check_kwargs)
        assert "check_with_threshold" in results
        assert len(results["check_with_threshold"]) > 0

    def test_execute_with_failing_check(self, sample_df):
        """Test that failing checks are isolated and don't crash execution."""

        def failing_check(df):
            """Check that always fails."""
            raise ValueError("Intentional error")

        def passing_check(df):
            """Check that passes."""
            return ["Passing check warning"]

        executor = ParallelExecutor(n_jobs=1)
        results = executor.execute_checks([failing_check, passing_check], sample_df)

        assert "failing_check" in results
        assert "Check failed with error" in results["failing_check"][0]
        assert "passing_check" in results
        assert results["passing_check"] == ["Passing check warning"]

    @pytest.mark.skipif(not JOBLIB_AVAILABLE, reason="joblib not installed")
    def test_execute_joblib_with_failing_check(self, sample_df):
        """Test that joblib handles failing checks gracefully."""

        def failing_check(df):
            """Check that always fails."""
            raise ValueError("Intentional error")

        def passing_check(df):
            """Check that passes."""
            return ["Passing check warning"]

        executor = ParallelExecutor(n_jobs=2, backend="joblib")
        executor.min_checks_for_parallel = 1
        results = executor.execute_checks([failing_check, passing_check], sample_df)

        assert "failing_check" in results
        assert "Check failed with error" in results["failing_check"][0]
        assert "passing_check" in results
        assert results["passing_check"] == ["Passing check warning"]

    def test_execute_empty_checks_list(self, sample_df):
        """Test execution with empty checks list."""
        executor = ParallelExecutor()
        results = executor.execute_checks([], sample_df)
        assert results == {}

    def test_auto_parallelise_decision(self, sample_df, sample_checks):
        """Test automatic parallelisation decision."""
        # Small DataFrame and few checks -> serial
        small_df = pd.DataFrame({"A": [1, 2, 3]})
        executor = ParallelExecutor()
        assert not executor.should_parallelise(len(sample_checks), len(small_df))

        # Large DataFrame and many checks -> parallel
        large_df = pd.DataFrame({"A": range(10000)})
        assert executor.should_parallelise(len(sample_checks), len(large_df))


class TestGetOptimalWorkers:
    """Test get_optimal_workers function."""

    def test_get_optimal_workers(self):
        """Test that optimal workers is calculated correctly."""
        workers = get_optimal_workers()
        assert workers > 0
        assert isinstance(workers, int)


class TestParallelIntegration:
    """Integration tests with actual LintDataAccessor."""

    def test_report_with_parallel_true(self):
        """Test report() with parallel=True."""
        df = pd.DataFrame(
            {
                "A": [1, 2, None, 4, 5] * 200,  # Make it large enough
                "B": ["a", "b", "c", "d", "e"] * 200,
            }
        )

        report = df.lint.report(return_dict=True)
        assert isinstance(report, dict)
        assert "Missing Values" in report["issues"][0]["check"]

    def test_report_with_parallel_false(self):
        """Test report() with parallel=False."""
        df = pd.DataFrame({"A": [1, 2, None, 4, 5], "B": ["a", "b", "c", "d", "e"]})

        report = df.lint.report(return_dict=True)
        assert isinstance(report, dict)

    def test_report_with_auto_parallel(self):
        """Test report() with automatic parallelisation."""
        # Small DataFrame - should use serial
        small_df = pd.DataFrame({"A": [1, 2, 3]})
        report = small_df.lint.report(return_dict=True)
        assert isinstance(report, dict)

        # Large DataFrame - should use parallel (if enough cores)
        large_df = pd.DataFrame({"A": range(10000), "B": range(10000)})
        report = large_df.lint.report(return_dict=True)
        assert isinstance(report, dict)

    def test_report_with_custom_workers(self):
        """Test report() with custom n_jobs."""
        df = pd.DataFrame({"A": range(1000), "B": range(1000)})

        report = df.lint.report(n_jobs=2, return_dict=True)
        assert isinstance(report, dict)

    def test_report_with_threading_backend(self):
        """Test report() with threading backend."""
        df = pd.DataFrame({"A": range(1000), "B": range(1000)})

        report = df.lint.report(backend="threading", return_dict=True)
        assert isinstance(report, dict)

    @pytest.mark.skipif(not JOBLIB_AVAILABLE, reason="joblib not installed")
    def test_report_with_joblib_backend(self):
        """Test report() with joblib backend."""
        df = pd.DataFrame({"A": range(1000), "B": range(1000)})

        report = df.lint.report(backend="joblib", return_dict=True)
        assert isinstance(report, dict)
