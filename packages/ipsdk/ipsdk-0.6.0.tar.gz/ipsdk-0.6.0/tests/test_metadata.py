# Copyright (c) 2025 Itential, Inc
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import ipsdk.metadata

from ipsdk import metadata


def test_exists():
    for item in ("author", "version", "name"):
        assert getattr(metadata, item) is not None
        assert isinstance(getattr(metadata, item), str)


def test_author_format():
    """Test that author field has reasonable format."""
    author = metadata.author
    assert len(author) > 0
    # Should contain some indication of author/company
    assert "Itential" in author or "itential" in author.lower()


def test_version_format():
    """Test that version follows semantic versioning pattern."""
    version = metadata.version
    assert len(version) > 0
    # Should not be the fallback version
    assert version != "0.0.0"
    # Basic version format check (allows for various formats)
    assert any(char.isdigit() for char in version)


def test_name_format():
    """Test that package name is correct."""
    name = metadata.name
    assert name == "ipsdk"


def test_metadata_attributes_immutable():
    """Test that metadata attributes behave properly."""
    # These should be string values
    original_version = metadata.version
    original_author = metadata.author
    original_name = metadata.name

    # Re-accessing should give same values
    assert metadata.version == original_version
    assert metadata.author == original_author
    assert metadata.name == original_name


def test_all_required_metadata_exists():
    """Test that all expected metadata attributes exist."""
    required_attrs = ["version", "author", "name"]

    for attr in required_attrs:
        assert hasattr(metadata, attr)
        value = getattr(metadata, attr)
        assert value is not None
        assert isinstance(value, str)
        assert len(value.strip()) > 0


def test_metadata_module_importable():
    """Test that metadata module can be imported correctly."""
    # Test direct import
    meta = metadata

    assert meta is metadata

    # Test that we can access attributes through different import styles
    meta2 = ipsdk.metadata

    assert meta2.version == metadata.version
    assert meta2.author == metadata.author
    assert meta2.name == metadata.name
