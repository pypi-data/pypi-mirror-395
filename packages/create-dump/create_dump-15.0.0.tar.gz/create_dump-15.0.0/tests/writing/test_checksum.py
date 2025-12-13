# tests/writing/test_checksum.py

"""
Tests for Phase 3: src/create_dump/writing/checksum.py
"""

from __future__ import annotations
import pytest
import hashlib

import anyio

# Import the class to test
from create_dump.writing.checksum import ChecksumWriter

# Mark all tests in this file as async-capable
pytestmark = pytest.mark.anyio


async def test_checksum_writer_write(test_project):
    """
    Tests that the ChecksumWriter.write() method correctly calculates
    the SHA256 hash of a file and writes the corresponding .sha256 file.
    """
    # 1. Setup: Create a test file
    file_content = "Hello, create-dump!"
    file_name = "test_file.txt"
    
    await test_project.create({
        file_name: file_content
    })
    
    file_path = test_project.path(file_name)
    
    # 2. Calculate expected hash
    expected_hash = hashlib.sha256(file_content.encode("utf-8")).hexdigest()
    expected_checksum_string = f"{expected_hash}  {file_name}"
    
    # 3. Run the writer
    writer = ChecksumWriter()
    returned_checksum = await writer.write(file_path)
    
    # 4. Assert the return value
    assert returned_checksum == expected_checksum_string
    
    # 5. Assert the created .sha256 file
    checksum_file_path = anyio.Path(file_path.with_suffix(".sha256"))
    assert await checksum_file_path.exists()
    
    # Read the content and check it
    checksum_file_content = await checksum_file_path.read_text()
    assert checksum_file_content.strip() == expected_checksum_string
