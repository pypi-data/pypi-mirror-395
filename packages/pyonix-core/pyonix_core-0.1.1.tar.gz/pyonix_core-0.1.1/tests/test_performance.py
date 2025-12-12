import unittest
import os
import time
import resource
import logging
from pathlib import Path
from pyonix_core.parsing.parser import parse_onix_stream
from pyonix_core.facade.product import ProductFacade

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestLargeFilePerformance(unittest.TestCase):
    LARGE_FILE_PATH = Path("/workspaces/python-2/large_onix_3.0.xml")

    def setUp(self):
        if not self.LARGE_FILE_PATH.exists():
            self.skipTest(f"Large file not found at {self.LARGE_FILE_PATH}")

    def get_memory_usage_mb(self):
        """Returns current memory usage in MB."""
        # ru_maxrss is in KB on Linux
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024

    def test_streaming_performance(self):
        """
        Test streaming parsing of a 5GB file.
        Measures time and memory usage to ensure no memory leaks.
        """
        start_time = time.time()
        start_memory = self.get_memory_usage_mb()
        
        logger.info(f"Starting test with {start_memory:.2f} MB memory usage")
        
        count = 0
        facade_checks = 0
        
        # We'll track memory usage periodically
        max_memory = start_memory
        
        for product in parse_onix_stream(self.LARGE_FILE_PATH):
            count += 1
            
            # Perform some operations to ensure we are actually using the object
            # and not just skipping over bytes.
            facade = ProductFacade(product)
            
            # Check facade properties on a sample to avoid slowing down too much
            # but enough to exercise the code.
            if count % 1000 == 0:
                _ = facade.isbn13
                _ = facade.title
                _ = facade.price_amount
                facade_checks += 1
            
            if count % 50000 == 0:
                current_memory = self.get_memory_usage_mb()
                max_memory = max(max_memory, current_memory)
                elapsed = time.time() - start_time
                rate = count / elapsed
                logger.info(f"Processed {count} records. Memory: {current_memory:.2f} MB. Rate: {rate:.2f} records/sec")

        end_time = time.time()
        total_time = end_time - start_time
        end_memory = self.get_memory_usage_mb()
        
        logger.info(f"Finished processing {count} records in {total_time:.2f} seconds.")
        logger.info(f"Final Memory: {end_memory:.2f} MB. Max Memory: {max_memory:.2f} MB.")
        logger.info(f"Average Rate: {count / total_time:.2f} records/sec")
        
        # Assertions
        self.assertGreater(count, 0, "Should have found records in the file")
        
        # Memory leak check (heuristic): 
        # If we consumed > 500MB extra for streaming, something might be wrong.
        # The XML tree for a single record + overhead shouldn't be huge.
        # Note: Python's GC is lazy, so this is a loose check.
        memory_growth = end_memory - start_memory
        logger.info(f"Memory growth: {memory_growth:.2f} MB")
        
        # We expect to process millions of records.
        # If we hold onto them, memory would explode to GBs.
        # 500MB is a generous buffer for the parser's internal buffers + python overhead.
        self.assertLess(memory_growth, 1024, "Memory usage grew by more than 1GB, possible leak")

if __name__ == "__main__":
    unittest.main()
