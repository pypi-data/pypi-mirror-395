# tests/test_rollback_coverage.py

import pytest
import hashlib
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from typer import Exit
import anyio

# Import the module to test
from create_dump.cli.rollback import async_rollback, rollback, _calculate_sha256, _find_most_recent_dump, _verify_integrity

@pytest.fixture
def mock_root(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    return root

@pytest.mark.anyio
class TestRollbackCoverage:

    async def test_calculate_sha256(self, mock_root):
        f = mock_root / "test.txt"
        f.write_text("hello world")

        expected = hashlib.sha256(b"hello world").hexdigest()
        actual = await _calculate_sha256(anyio.Path(f))

        assert actual == expected

    async def test_find_most_recent_dump_oserror(self, mock_root):
        # Create a file that will raise OSError on stat (simulated)
        f = mock_root / "test_all_create_dump_1.md"
        f.touch()

        # We need to mock anyio.Path.stat to raise OSError
        # But `_find_most_recent_dump` uses `async for file in anyio_root.glob(...)`
        # and then `await file.stat()`.
        # `file` here is an anyio.Path object yielded by glob.

        # It's hard to mock the stat method of the object yielded by glob without complex mocking.
        # Alternatively, verify the exception handling logic by mocking glob?

        async def mock_glob(pattern):
             mock_path = MagicMock()
             mock_path.stat = AsyncMock(side_effect=OSError("Access denied"))
             yield mock_path

        with patch("anyio.Path.glob", side_effect=mock_glob):
            result = await _find_most_recent_dump(mock_root)
            assert result is None

    async def test_verify_integrity_missing_sha(self, mock_root):
        md_file = mock_root / "test.md"
        md_file.touch()

        assert not await _verify_integrity(md_file)

    async def test_verify_integrity_mismatch(self, mock_root):
        md_file = mock_root / "test.md"
        md_file.write_text("content")
        sha_file = mock_root / "test.sha256"
        sha_file.write_text("wrong_hash  test.md")

        assert not await _verify_integrity(md_file)

    async def test_verify_integrity_exception(self, mock_root):
        md_file = mock_root / "test.md"
        md_file.touch()
        sha_file = mock_root / "test.sha256"
        sha_file.touch()

        # Mock _calculate_sha256 to raise exception
        with patch("create_dump.cli.rollback._calculate_sha256", side_effect=Exception("Calc Error")):
            assert not await _verify_integrity(md_file)

    async def test_async_rollback_file_not_found(self, mock_root):
        with pytest.raises(Exit) as exc:
            await async_rollback(
                root=mock_root,
                file_to_use=mock_root / "missing.md",
                yes=False,
                dry_run=False,
                quiet=False
            )
        assert exc.value.exit_code == 1

    async def test_async_rollback_no_dump_found(self, mock_root):
        with pytest.raises(Exit) as exc:
            await async_rollback(
                root=mock_root,
                file_to_use=None,
                yes=False,
                dry_run=False,
                quiet=False
            )
        assert exc.value.exit_code == 1

    async def test_async_rollback_integrity_fail(self, mock_root):
        md_file = mock_root / "test_all_create_dump_1.md"
        md_file.touch()
        # Missing SHA

        with pytest.raises(Exit) as exc:
            await async_rollback(
                root=mock_root,
                file_to_use=None,
                yes=False,
                dry_run=False,
                quiet=False
            )
        assert exc.value.exit_code == 1

    async def test_async_rollback_user_cancel(self, mock_root):
        md_file = mock_root / "test_all_create_dump_1.md"
        md_file.write_text("content")
        sha_file = mock_root / "test_all_create_dump_1.sha256"
        sha = hashlib.sha256(b"content").hexdigest()
        sha_file.write_text(f"{sha}  test.md")

        with patch("create_dump.cli.rollback.confirm", return_value=False):
            with pytest.raises(Exit) as exc:
                await async_rollback(
                    root=mock_root,
                    file_to_use=None,
                    yes=False,
                    dry_run=False,
                    quiet=False
                )
            # Exit with None/default code usually means 0, but here checking cancellation flow
            # The code raises `raise typer.Exit()` which defaults to 0.

    async def test_rollback_cli_wrapper(self, mock_root):
        # Test the sync wrapper function `rollback`

        mock_ctx = MagicMock()
        mock_ctx.find_root().params = {}

        with patch("create_dump.cli.rollback.anyio.run") as mock_run:
            rollback(mock_ctx, root=mock_root, file=None, yes=True, dry_run=True, no_dry_run=False, verbose=True, quiet=False)
            assert mock_run.called

    async def test_rollback_cli_exception(self, mock_root):
        mock_ctx = MagicMock()
        mock_ctx.find_root().params = {}

        with patch("create_dump.cli.rollback.anyio.run", side_effect=Exception("Boom")):
            with pytest.raises(Exit) as exc:
                 rollback(mock_ctx, root=mock_root)
            assert exc.value.exit_code == 1

    async def test_rollback_cli_value_error(self, mock_root):
        mock_ctx = MagicMock()
        mock_ctx.find_root().params = {}

        with patch("create_dump.cli.rollback.anyio.run", side_effect=ValueError("Bad Value")):
            with pytest.raises(Exit) as exc:
                 rollback(mock_ctx, root=mock_root)
            assert exc.value.exit_code == 1
