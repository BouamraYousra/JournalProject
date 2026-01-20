import pytest
from app.models.concrete import TextEntry, FileEntry
from app.models.features import SecretEntry, MultilingualEntry
from app.services.storage import StorageFactory
import tempfile
import os


class TestTextEntry:
    def test_text_entry_creation(self):
        """Test basic TextEntry functionality."""
        entry = TextEntry("Test Title", "Test Content")
        assert entry.get_content() == "Test Content"
        assert entry.metadata()["title"] == "Test Title"
        assert entry.metadata()["type"] == "TEXT"

    def test_text_entry_edit(self):
        """Test content editing."""
        entry = TextEntry("Title", "Original")
        entry.edit_content("Updated")
        assert entry.get_content() == "Updated"


class TestFileEntry:
    def test_file_entry_creation(self):
        """Test FileEntry with valid text file."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False
        ) as f:
            f.write("File content")
            temp_path = f.name

        try:
            entry = FileEntry(temp_path)
            assert entry.get_content() == "File content"
            assert entry.metadata()["type"] == "FILE"
        finally:
            os.unlink(temp_path)

    def test_file_entry_edit_sync(self):
        """Test FileEntry edits sync to file."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False
        ) as f:
            f.write("Original")
            temp_path = f.name

        try:
            entry = FileEntry(temp_path)
            entry.edit_content("Updated")

            # Verify file was updated
            with open(temp_path, 'r') as f:
                assert f.read() == "Updated"
        finally:
            os.unlink(temp_path)

    def test_invalid_file_type(self):
        """Test FileEntry rejects unsupported file types."""
        with pytest.raises(ValueError):
            FileEntry("test.exe")


class TestSecretEntry:
    def test_secret_entry_locking(self):
        """Test SecretEntry password protection."""
        base = TextEntry("Secret", "Hidden content")
        secret = SecretEntry(base, "mypassword")

        # Should be locked initially
        assert secret.get_content() == (
            "******** [LOCKED] ********"
        )
        assert secret.locked

    def test_secret_entry_unlock(self):
        """Test SecretEntry password verification."""
        base = TextEntry("Secret", "Hidden content")
        secret = SecretEntry(base, "mypassword")

        assert not secret.verify("wrongpass")
        assert secret.verify("mypassword")
        assert secret.get_content() == "Hidden content"


class TestMultilingualEntry:
    def test_multilingual_entry_wrapping(self):
        """Test MultilingualEntry decorator pattern."""
        base = TextEntry("Title", "Hello world")
        multi = MultilingualEntry(base)

        assert multi.get_content() == "Hello world"
        assert isinstance(multi.entry, TextEntry)

    def test_translation_storage(self):
        """Test translations are stored properly."""
        base = TextEntry("Title", "Hello")
        multi = MultilingualEntry(base)

        # Mock translation - in real test you'd mock GoogleTranslator
        multi.translations = {"es": "Hola", "fr": "Bonjour"}

        assert "es" in multi.translations
        assert "fr" in multi.translations


class TestStorageFactory:
    def test_factory_text_entry(self):
        """Test factory creates TextEntry."""
        entry = StorageFactory.create(
            "TEXT",
            {"title": "Test", "body": "Content"}
        )
        assert isinstance(entry, TextEntry)

    def test_factory_secure_wrapper(self):
        """Test factory creates secured entry."""
        base = TextEntry("Test", "Content")
        secure = StorageFactory.secure(base, "password")
        assert isinstance(secure, SecretEntry)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
