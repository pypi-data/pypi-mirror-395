
import os
import shutil
import anyio
from pathlib import Path
from typing import Optional
from .core import DumpFile
from .logging import logger

class DatabaseDumper:
    """Handles database dumping for PostgreSQL and MySQL."""

    def __init__(
        self,
        provider: str,
        db_name: str,
        host: str = "localhost",
        port: Optional[int] = None,
        user: Optional[str] = None,
        password_env: Optional[str] = None,
    ):
        self.provider = provider.lower()
        self.db_name = db_name
        self.host = host
        self.port = port
        self.user = user
        self.password_env = password_env

    async def dump(self) -> DumpFile:
        """Executes the dump command and returns a DumpFile object."""
        if self.provider == "postgres":
            cmd = self._build_postgres_cmd()
            tool_name = "pg_dump"
        elif self.provider == "mysql":
            cmd = self._build_mysql_cmd()
            tool_name = "mysqldump"
        else:
            raise ValueError(f"Unsupported database provider: {self.provider}")

        # Check if tool exists
        if not shutil.which(cmd[0]):
            raise RuntimeError(f"{tool_name} not found in PATH. Please install it to use database dumping.")

        # Check password env var
        env = os.environ.copy()
        if self.password_env:
            if self.password_env not in env:
                raise ValueError(f"Environment variable {self.password_env} not set")
            # For Postgres, we can set PGPASSWORD. For MySQL, MYSQL_PWD.
            # However, the user might have provided a custom env var name.
            # We need to map it to what the tool expects, or assume the user set the correct one.
            # Actually, the user provides the name of the env var that holds the password.
            # We should read it and set the tool-specific env var.
            password = env[self.password_env]
            if self.provider == "postgres":
                env["PGPASSWORD"] = password
            elif self.provider == "mysql":
                env["MYSQL_PWD"] = password

        logger.info(f"Starting {self.provider} dump", db=self.db_name, host=self.host)

        try:
            result = await anyio.run_process(cmd, env=env, stderr=None) # stderr=None means stderr goes to parent stderr (visible)
            content = result.stdout.decode("utf-8")

            return DumpFile(
                path="database.sql",
                content=content,
                size=len(content)
            )
        except Exception as e:
             logger.error(f"Database dump failed: {e}")
             raise

    def _build_postgres_cmd(self) -> list[str]:
        cmd = ["pg_dump", "-h", self.host]
        if self.port:
            cmd.extend(["-p", str(self.port)])
        if self.user:
            cmd.extend(["-U", self.user])
        cmd.append(self.db_name)
        return cmd

    def _build_mysql_cmd(self) -> list[str]:
        cmd = ["mysqldump", "-h", self.host]
        if self.port:
            cmd.extend(["-P", str(self.port)])
        if self.user:
            cmd.extend(["-u", self.user])
        cmd.append(self.db_name)
        return cmd
