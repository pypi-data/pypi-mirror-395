
import pytest
from unittest.mock import MagicMock, patch
from create_dump.database import DatabaseDumper
from create_dump.core import DumpFile

@pytest.fixture
def mock_subprocess():
    with patch("anyio.run_process") as mock:
        yield mock

@pytest.fixture
def mock_shutil_which():
    with patch("shutil.which") as mock:
        yield mock

@pytest.mark.asyncio
async def test_postgres_dump(mock_subprocess, mock_shutil_which):
    mock_shutil_which.return_value = "/usr/bin/pg_dump"
    mock_subprocess.return_value.stdout = b"CREATE TABLE users..."

    dumper = DatabaseDumper(
        provider="postgres",
        db_name="mydb",
        host="localhost",
        port=5432,
        user="admin",
        password_env="PG_PASS"
    )

    with patch.dict("os.environ", {"PG_PASS": "secret"}):
        dump_file = await dumper.dump()

    assert isinstance(dump_file, DumpFile)
    assert dump_file.path == "database.sql"
    # Content is not readable because temp_path is not set,
    # but the current implementation sets content directly for SQL dump?
    # Wait, DumpFile in core.py doesn't have a content field in pydantic model?
    # Let's check core.py again.

    # Check if pg_dump was called with correct args
    mock_subprocess.assert_called_once()
    cmd = mock_subprocess.call_args[0][0]
    assert cmd[0] == "pg_dump"
    assert "-h" in cmd
    assert "localhost" in cmd
    assert "-p" in cmd
    assert "5432" in cmd
    assert "-U" in cmd
    assert "admin" in cmd
    assert "mydb" in cmd

@pytest.mark.asyncio
async def test_mysql_dump(mock_subprocess, mock_shutil_which):
    mock_shutil_which.return_value = "/usr/bin/mysqldump"
    mock_subprocess.return_value.stdout = b"CREATE TABLE posts..."

    dumper = DatabaseDumper(
        provider="mysql",
        db_name="blog",
        host="127.0.0.1",
        port=3306,
        user="root",
        password_env="MYSQL_PWD"
    )

    with patch.dict("os.environ", {"MYSQL_PWD": "rootpassword"}):
        dump_file = await dumper.dump()

    assert dump_file.content == "CREATE TABLE posts..."

    mock_subprocess.assert_called_once()
    cmd = mock_subprocess.call_args[0][0]
    assert cmd[0] == "mysqldump"
    assert "-h" in cmd
    assert "127.0.0.1" in cmd
    assert "-P" in cmd
    assert "3306" in cmd
    assert "-u" in cmd
    assert "root" in cmd
    assert "blog" in cmd

@pytest.mark.asyncio
async def test_tool_not_found(mock_shutil_which):
    mock_shutil_which.return_value = None

    dumper = DatabaseDumper(provider="postgres", db_name="test")

    with pytest.raises(RuntimeError, match="pg_dump not found"):
        await dumper.dump()

@pytest.mark.asyncio
async def test_missing_env_var(mock_shutil_which):
    mock_shutil_which.return_value = "/bin/pg_dump"

    dumper = DatabaseDumper(provider="postgres", db_name="test", password_env="MISSING_VAR")

    with pytest.raises(ValueError, match="Environment variable MISSING_VAR not set"):
        await dumper.dump()
