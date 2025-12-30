"""
Unit tests for CSV cache utility
"""
import unittest
import os
import tempfile
import time
from utils.csv_cache import CSVCache

class TestCSVCache(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.cache = CSVCache()
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv')
        self.temp_file.write("test,data\n1,2\n")
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
        self.cache.clear_cache()
    
    def test_is_file_changed(self):
        """Test file change detection"""
        # File not in cache should be considered changed
        self.assertTrue(self.cache.is_file_changed(self.temp_file.name))
        
        # Update cache
        self.cache.update_cache(self.temp_file.name, ["test", "data"])
        
        # File should not be changed
        self.assertFalse(self.cache.is_file_changed(self.temp_file.name))
        
        # Modify file
        time.sleep(0.1)  # Ensure different mtime
        with open(self.temp_file.name, 'a') as f:
            f.write("3,4\n")
        
        # File should be changed
        self.assertTrue(self.cache.is_file_changed(self.temp_file.name))
    
    def test_update_cache(self):
        """Test cache update"""
        data = ["test", "data"]
        self.cache.update_cache(self.temp_file.name, data)
        
        cached = self.cache.get_cached_data(self.temp_file.name)
        self.assertEqual(cached, data)
    
    def test_clear_cache(self):
        """Test cache clearing"""
        self.cache.update_cache(self.temp_file.name, ["test"])
        self.cache.clear_cache(self.temp_file.name)
        
        cached = self.cache.get_cached_data(self.temp_file.name)
        self.assertIsNone(cached)

if __name__ == "__main__":
    unittest.main()

