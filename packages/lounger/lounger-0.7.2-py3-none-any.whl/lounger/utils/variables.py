import importlib.util
from pathlib import Path
from typing import Any, Callable

from lounger.log import log
from lounger.utils.config_utils import ConfigUtils


class ExtractVar:
    """
    Extract variables
    """
    _instance = None
    _functions = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_conftest_functions()
        return cls._instance

    def _load_conftest_functions(self):
        """
        Load the conftest function only once
        """
        conftest_path = Path("conftest.py")
        if not conftest_path.exists():
            log.debug("No conftest.py found, skip loading custom functions.")
            return

        try:
            spec = importlib.util.spec_from_file_location("conftest", conftest_path)
            conftest = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(conftest)

            for name in dir(conftest):
                obj = getattr(conftest, name)
                if callable(obj) and not name.startswith("pytest_"):
                    self._functions[name] = obj
                    log.debug(f"🔧 Loaded custom function: {name}")
        except Exception as e:
            log.error(f"Failed to load conftest.py: {e}")

    @staticmethod
    def config(key: str) -> Any:
        """
        Extract from the config file
        :param key:
        """
        config_utils = ConfigUtils("config/config.yaml")
        base_config = config_utils.get_config('global_test_config')
        try:
            return base_config.get(key)
        except Exception as e:
            log.error(f"getting config error: {e}")
            return None

    @staticmethod
    def extract(key: str) -> Any:
        """
        Extract from the cache
        :param key：
        """
        from lounger.utils import cache
        return cache.get(key)

    def __getattr__(self, name: str) -> Callable:
        if name in self._functions:
            return self._functions[name]
        raise AttributeError(f"Function '{name}' not found")
