import os
import time
from typing import Dict, Any, List, Optional

from trino.dbapi import connect

from src.domain.ports.database_port import DatabasePort


class TrinoConfigError(RuntimeError):
    pass


class TrinoConnectionError(RuntimeError):
    pass


class TrinoQueryError(RuntimeError):
    pass


class TrinoDatabaseService(DatabasePort):
    REQUIRED_ENV_VARS = {"TRINO_HOST": str, "TRINO_PORT": int, "TRINO_USER": str, "TRINO_CATALOG": str,
                         "TRINO_SCHEMA": str, "TRINO_HTTP_SCHEMA": str, }

    def __init__(self, *, query_timeout_seconds: int = 60, max_retries: int = 2, retry_backoff_seconds: float = 0.5,
                 read_only: bool = True, ) -> None:
        self.query_timeout_seconds = query_timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.read_only = read_only

        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        missing = []
        config: Dict[str, Any] = {}

        for key, cast in self.REQUIRED_ENV_VARS.items():
            value = os.getenv(key)
            if value is None:
                missing.append(key)
                continue

            try:
                config[key] = cast(value)
            except ValueError:
                raise TrinoConfigError(f"Invalid value for env var {key}: {value}")

        if missing:
            raise TrinoConfigError(f"Missing required Trino env vars: {', '.join(missing)}")

        return config

    def _get_connection(self):
        try:
            return connect(host=self._config["TRINO_HOST"], port=self._config["TRINO_PORT"],
                           user=self._config["TRINO_USER"], catalog=self._config["TRINO_CATALOG"],
                           schema=self._config["TRINO_SCHEMA"], http_scheme=self._config["TRINO_HTTP_SCHEMA"],
                           session_properties={"query_max_run_time": f"{self.query_timeout_seconds}s"}, )
        except Exception as exc:
            raise TrinoConnectionError(str(exc)) from exc

    def _validate_read_only(self, query: str) -> None:
        if not self.read_only:
            return

        forbidden = ("insert", "update", "delete", "drop", "alter", "create", "truncate")
        normalized = query.strip().lower()
        if normalized.startswith(forbidden):
            raise TrinoQueryError("Write queries are not allowed in read-only mode")

    def query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a synchronous Trino query with automatic retries.
        """
        self._validate_read_only(query)

        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= self.max_retries:
            conn = None
            cur = None
            try:
                conn = self._get_connection()
                cur = conn.cursor()

                cur.execute(query)

                rows = cur.fetchall()
                # Handle cases where description might be None (e.g. non-select queries)
                columns = [col[0] for col in cur.description] if cur.description else []

                return [dict(zip(columns, row)) for row in rows]

            except Exception as exc:
                last_error = exc
                attempt += 1
                if attempt > self.max_retries:
                    break
                time.sleep(self.retry_backoff_seconds * attempt)

            finally:
                # Ensure resources are closed safely
                if cur:
                    try:
                        cur.close()
                    except Exception:
                        pass
                if conn:
                    try:
                        conn.close()
                    except Exception:
                        pass

        # If we exit the loop, we failed all retries
        raise TrinoQueryError(f"Query failed after {self.max_retries} retries: {str(last_error)}")

    def ping(self) -> bool:
        """
        Checks database connectivity synchronously.
        """
        try:
            rows = self.query("SELECT 1")
            return len(rows) > 0
        except Exception:
            return False
