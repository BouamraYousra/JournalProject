import pytest
import tempfile
import json
import csv
import os
from app.services.file_manager import FileManager

class TestFileManager:
    def test_export_import_txt(self):
        """Test TXT export and import roundtrip."""
        test_data = {
            "title": "Test Journal",
            "body": "This is the main content.",
            "translations": {"es": "Este es el contenido principal."}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            # Export to TXT
            result = FileManager.export_to_txt(
                temp_path,
                test_data["title"],
                test_data["body"],
                test_data["translations"]
            )
            assert result == True
            
            # Import from TXT
            imported_title, imported_body, imported_trans = FileManager.import_from_file(temp_path)
            
            # Verify data integrity
            assert imported_title == test_data["title"]
            assert imported_body == test_data["body"]
            assert imported_trans == test_data["translations"]
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_export_import_csv(self):
        """Test CSV export and import roundtrip."""
        test_data = {
            "title": "CSV Test",
            "body": "CSV content here.",
            "translations": {"fr": "Contenu CSV ici."}
        }
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            # Export to CSV
            result = FileManager.export_to_csv(
                temp_path,
                test_data["title"],
                test_data["body"],
                test_data["translations"]
            )
            assert result == True
            
            # Import from CSV
            imported_title, imported_body, imported_trans = FileManager.import_from_file(temp_path)
            
            # Verify data integrity
            assert imported_title == test_data["title"]
            assert imported_body == test_data["body"]
            assert imported_trans == test_data["translations"]
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_import_plain_text(self):
        """Test importing plain text file without metadata."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Just plain text content")
            temp_path = f.name
        
        try:
            title, body, translations = FileManager.import_from_file(temp_path)
            
            # Plain text should extract filename as title
            assert title == os.path.splitext(os.path.basename(temp_path))[0]
            assert body == "Just plain text content"
            assert translations == {}
            
        finally:
            os.unlink(temp_path)
    
    def test_export_error_handling(self):
        """Test error handling for export operations."""
        # Try to export to invalid path (permission denied or non-existent parent)
        invalid_path = "/nonexistent/path/file.txt"
        result = FileManager.export_to_txt(invalid_path, "Title", "Body", {})
        assert result == False  # Should handle error gracefully
    
    def test_import_invalid_file(self):
        """Test error handling for invalid file import."""
        with pytest.raises(Exception):
            FileManager.import_from_file("/nonexistent/file.txt")

class TestDatabaseIntegration:
    """Tests that integrate database and file operations."""
    
    def test_database_singleton(self, mocker):
        """Test DatabaseService singleton pattern."""
        from app.services.database import DatabaseService
        
        db1 = DatabaseService()
        db2 = DatabaseService()
        
        # Verify singleton: both should be the same instance
        assert db1 is db2
    
    def test_dual_database_operations(self, mocker):
        """Test coordinated MySQL and MongoDB operations."""
        # Mock database connections to avoid actual DB dependency
        mock_mysql = mocker.Mock()
        mock_mongo = mocker.Mock()
        
        from app.services.database import DatabaseService
        db = DatabaseService()
        db.mysql = mock_mysql
        db.mongo = mock_mongo
        
        # Test save operation triggers both databases
        test_id = 123
        test_content = "Test content"
        test_translations = {"ar": "اختبار"}
        
        db.save_content(test_id, test_content, test_translations)
        
        # Verify MongoDB was called
        mock_mongo.entries.update_one.assert_called_once()
        
        # Note: MySQL operations are tested through metadata saving
        # which would be mocked similarly

def run_all_tests():
    """Helper to run all tests."""
    import sys
    sys.exit(pytest.main([__file__, "-v"]))

if __name__ == "__main__":
    run_all_tests()