import multiprocessing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

try:
    from joblib import Parallel, delayed

    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False


class ParallelExecutor:
    def __init__(self, n_jobs: int = -1, backend: str = "multiprocessing", min_checks_for_parallel: int = 3):
        """Initialise parallel executor.

        Args:
            n_jobs (int, optional): Number of worker processes/threads. -1: Use all available cores, 1: Serial Execution, n > 1: Use n workers. Defaults to -1.
            backend (str, optional): Parallelisation backend. "multiprocessing": Process Pool (CPU-bound), "threading": Thread Pool (I/O-bound), "joblib": Joblib Parallel. Defaults to "multiprocessing".
            min_checks_for_parallel (int, optional): Minimum number of checks required to trigger parallel execution. Defaults to 3.

        Raises:
            ImportError: If joblib is not installed and backend is set to "joblib".
            ValueError: If n_jobs is not -1 or a positive integer.
        """
        self.backend = backend
        self.min_checks_for_parallel = min_checks_for_parallel

        if backend == "joblib" and not JOBLIB_AVAILABLE:
            raise ImportError(
                "joblib is not installed. Please install via 'pip install joblib' to use this backend. "
                "Alternatively, choose 'multiprocessing' or 'threading' backend."
            )

        if n_jobs == -1:
            self.n_jobs = multiprocessing.cpu_count()
        elif n_jobs < 1:
            raise ValueError("n_jobs must be -1 or a positive integer.")
        else:
            self.n_jobs = n_jobs

    def should_parallelise(self, n_checks: int, df_size: int) -> bool:
        """Determine if parallelisation would be beneficial.

        Args:
            n_checks (int): Number of checks to execute.
            df_size (int): Size of DataFrame (number of rows).

        Returns:
            bool: Whether parallelisation should be used.
        """
        if self.n_jobs == 1:
            return False

        if n_checks < self.min_checks_for_parallel:
            return False

        return not df_size < 1000

    def _execute_serial(
        self,
        check_functions: List[Callable],
        df: pd.DataFrame,
        check_kwargs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, List[str]]:
        """Execute checks serially."""
        results = {}

        for func in check_functions:
            func_name = func.__name__
            kwargs = check_kwargs.get(func_name, {})

            try:
                warnings = func(df, **kwargs)
                results[func_name] = warnings
            except Exception as e:
                results[func_name] = [f"Check failed with error: {type(e).__name__}: {e!s}"]

        return results

    def _execute_multiprocessing(
        self,
        check_functions: List[Callable],
        df: pd.DataFrame,
        check_kwargs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, List[str]]:
        """Execute checks using multiprocessing."""
        results = {}

        with ProcessPoolExecutor(max_workers=self.n_jobs) as executor:
            future_to_func = {}

            for func in check_functions:
                func_name = func.__name__
                kwargs = check_kwargs.get(func_name, {})
                future = executor.submit(self._run_check, func, df, kwargs)
                future_to_func[future] = func_name

            for future in as_completed(future_to_func):
                func_name = future_to_func[future]
                try:
                    warnings = future.result()
                    results[func_name] = warnings
                except Exception as e:
                    results[func_name] = [f"Check failed with error: {type(e).__name__}: {e!s}"]

        return results

    def _execute_threading(
        self, check_functions: List[Callable], df: pd.DataFrame, check_kwargs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Execute checks using threading."""
        results = {}

        with ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            future_to_func = {}
            for func in check_functions:
                func_name = func.__name__
                kwargs = check_kwargs.get(func_name, {})
                future = executor.submit(self._run_check, func, df, kwargs)
                future_to_func[future] = func_name

            for future in as_completed(future_to_func):
                func_name = future_to_func[future]
                try:
                    warnings = future.result()
                    results[func_name] = warnings
                except Exception as e:
                    results[func_name] = [f"Check failed with error: {type(e).__name__}: {e!s}"]

        return results

    def _execute_joblib(
        self,
        check_functions: List[Callable],
        df: pd.DataFrame,
        check_kwargs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, List[str]]:
        """Execute checks using joblib."""
        if not JOBLIB_AVAILABLE:
            raise ImportError("joblib is not installed.")

        tasks = []
        func_names = []
        for func in check_functions:
            func_name = func.__name__
            kwargs = check_kwargs.get(func_name, {})
            tasks.append(delayed(self._run_check_safe)(func, df, kwargs))  # type: ignore
            func_names.append(func_name)

        parallel_results = Parallel(n_jobs=self.n_jobs, prefer="processes", verbose=0)(tasks)  # type: ignore
        results = dict(zip(func_names, parallel_results))
        return results  # type: ignore

    @staticmethod
    def _run_check(func: Callable, df: pd.DataFrame, kwargs: Dict[str, Any]) -> List[str]:
        """
        Run a single check function.

        This is a static method to ensure it can be pickled for multiprocessing.
        """
        return func(df, **kwargs)

    @staticmethod
    def _run_check_safe(func: Callable, df: pd.DataFrame, kwargs: Dict[str, Any]) -> List[str]:
        """
        Run a single check function with error handling.

        Used in joblib backend to capture exceptions.
        """
        try:
            return func(df, **kwargs)
        except Exception as e:
            return [f"Check failed with error: {type(e).__name__}: {e!s}"]

    def execute_checks(
        self,
        check_functions: List[Callable],
        df: pd.DataFrame,
        check_kwargs: Optional[Dict[str, Dict[str, Any]]] = None,
    ) -> Dict[str, List[str]]:
        """Execute multiple check functions in parallel.

        Args:
            check_functions (List[Callable]): List of check functions to execute
            df (pd.DataFrame): DataFrame to check
            check_kwargs (Optional[Dict[str, Dict[str, Any]]], optional): Keyword arguments for each check function.

        Raises:
            ValueError: If an unknown backend is specified.

        Returns:
            Dict[str, List[str]]: Dictionary mapping check function names to their warning messages.
        """
        check_kwargs = check_kwargs or {}

        if not self.should_parallelise(len(check_functions), len(df)):
            return self._execute_serial(check_functions, df, check_kwargs)

        if self.backend == "multiprocessing":
            return self._execute_multiprocessing(check_functions, df, check_kwargs)
        elif self.backend == "threading":
            return self._execute_threading(check_functions, df, check_kwargs)
        elif self.backend == "joblib":
            return self._execute_joblib(check_functions, df, check_kwargs)
        else:
            raise ValueError(f"Unknown backend: {self.backend}. Choose from: 'multiprocessing', 'threading', 'joblib'")


def get_optimal_workers() -> int:
    """Get optimal number of worker processes based on CPU count.

    Returns:
        int: Optimal number of worker processes.
    """
    cpu_count = multiprocessing.cpu_count()

    if cpu_count > 2:
        return cpu_count - 1
    return 1
