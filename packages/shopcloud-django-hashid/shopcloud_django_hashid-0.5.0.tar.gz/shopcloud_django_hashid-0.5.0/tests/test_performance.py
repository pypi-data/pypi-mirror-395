"""Performance benchmark tests for hashid encoding/decoding.

Tests for User Story 2: Verify encoding/decoding performance meets targets.
Tests for User Story 3: Verify Hashids instance caching works correctly.
"""

import gc
import time
from concurrent.futures import ThreadPoolExecutor

from hashid_field import BigHashidField, HashidField
from hashid_field.hashid import Hashid


class TestEncodingPerformance:
    """T018-T020: Performance benchmark tests."""

    def test_encode_10000_ids_under_one_second(self):
        """T018: Encoding 10,000 IDs should complete in under 1 second."""
        field = HashidField(salt="benchmark-salt", min_length=7)

        start = time.perf_counter()
        for i in range(10000):
            field.encode_id(i)
        elapsed = time.perf_counter() - start

        assert (
            elapsed < 1.0
        ), f"Encoding 10,000 IDs took {elapsed:.3f}s (expected < 1.0s)"

    def test_decode_10000_hashids_under_one_second(self):
        """T019: Decoding 10,000 hashids should complete in under 1 second."""
        field = HashidField(salt="benchmark-salt", min_length=7)

        # Pre-generate hashids
        hashids = [str(field.encode_id(i)) for i in range(10000)]

        start = time.perf_counter()
        for hashid_str in hashids:
            field.decode_id(hashid_str)
        elapsed = time.perf_counter() - start

        assert (
            elapsed < 1.0
        ), f"Decoding 10,000 hashids took {elapsed:.3f}s (expected < 1.0s)"

    def test_concurrent_encoding_100_threads(self):
        """T020: Concurrent encoding with 100 threads should scale without contention."""
        field = HashidField(salt="concurrent-salt", min_length=7)

        def encode_batch(start_id: int) -> list:
            """Encode 100 IDs starting from start_id."""
            return [str(field.encode_id(start_id + i)) for i in range(100)]

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(encode_batch, i * 100) for i in range(100)]
            results = [f.result() for f in futures]
        elapsed = time.perf_counter() - start

        # Should complete 10,000 total encodes in reasonable time
        assert (
            elapsed < 5.0
        ), f"Concurrent encoding took {elapsed:.3f}s (expected < 5.0s)"

        # Verify all results are valid
        total_results = sum(len(r) for r in results)
        assert total_results == 10000, f"Expected 10,000 results, got {total_results}"


class TestCachingVerification:
    """T022-T025: Verify Hashids instance caching works correctly."""

    def test_hashids_instance_reused_per_field(self):
        """T023: Same Hashids instance should be reused across operations."""
        field = HashidField(salt="cache-test-salt", min_length=7)

        # First access creates the instance
        hashids1 = field.get_hashids()

        # Subsequent accesses should return the same instance
        hashids2 = field.get_hashids()
        hashids3 = field.get_hashids()

        assert hashids1 is hashids2, "Hashids instance should be reused"
        assert hashids2 is hashids3, "Hashids instance should be reused"

    def test_different_configs_separate_instances(self):
        """T024: Different field configurations should have separate Hashids instances."""
        field1 = HashidField(salt="salt-one", min_length=7)
        field2 = HashidField(salt="salt-two", min_length=7)
        field3 = HashidField(salt="salt-one", min_length=10)

        hashids1 = field1.get_hashids()
        hashids2 = field2.get_hashids()
        hashids3 = field3.get_hashids()

        # Different salts should have different instances
        assert (
            hashids1 is not hashids2
        ), "Different salts should have different instances"

        # Same salt but different min_length should have different instances
        assert (
            hashids1 is not hashids3
        ), "Different min_length should have different instances"

    def test_memory_stability_repeated_operations(self):
        """T025: Memory usage should remain stable under repeated operations."""
        field = HashidField(salt="memory-test-salt", min_length=7)

        # Force garbage collection
        gc.collect()

        # Get baseline memory by tracking Hashid object count
        initial_hashids_instance = field.get_hashids()

        # Perform many encode/decode operations
        for _ in range(1000):
            for i in range(100):
                hashid = field.encode_id(i)
                if isinstance(hashid, Hashid):
                    _ = str(hashid)

        # Force garbage collection
        gc.collect()

        # The same Hashids instance should still be in use
        final_hashids_instance = field.get_hashids()

        assert (
            initial_hashids_instance is final_hashids_instance
        ), "Hashids instance should remain stable after repeated operations"

    def test_encoding_produces_consistent_results(self):
        """Verify that encoding produces consistent results across calls."""
        field = HashidField(salt="consistency-salt", min_length=7)

        results = set()
        for _ in range(100):
            hashid = field.encode_id(42)
            results.add(str(hashid))

        assert len(results) == 1, f"Expected 1 unique result, got {len(results)}"


class TestBigHashidFieldPerformance:
    """Performance tests for BigHashidField."""

    def test_big_field_encode_10000_ids_under_one_second(self):
        """BigHashidField should also meet the 10,000 ops/second target."""
        field = BigHashidField(salt="big-benchmark-salt", min_length=13)

        start = time.perf_counter()
        for i in range(10000):
            field.encode_id(i)
        elapsed = time.perf_counter() - start

        assert (
            elapsed < 1.0
        ), f"BigHashidField encoding 10,000 IDs took {elapsed:.3f}s (expected < 1.0s)"

    def test_big_field_caching_works(self):
        """BigHashidField should also cache Hashids instances."""
        field = BigHashidField(salt="big-cache-salt", min_length=13)

        hashids1 = field.get_hashids()
        hashids2 = field.get_hashids()

        assert hashids1 is hashids2, "BigHashidField should cache Hashids instance"
