"""Tests for thread safety.

Tests for T048: Thread safety verification.
"""

import concurrent.futures
import threading

from hashid_field.hashid import Hashid


class TestThreadSafety:
    """T048: Tests for thread-safe encoding/decoding."""

    def test_concurrent_hashid_creation(self):
        """Multiple threads can create Hashid objects safely."""
        results = []
        errors = []
        lock = threading.Lock()

        def create_hashid(value):
            try:
                h = Hashid(value, salt="test-salt")
                with lock:
                    results.append((value, h.hashid))
            except Exception as e:
                with lock:
                    errors.append((value, str(e)))

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_hashid, i) for i in range(100)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 100

        # Verify all hashids are unique
        hashids = [h for _, h in results]
        assert len(set(hashids)) == 100

    def test_concurrent_encoding_same_value(self):
        """Same value encoded concurrently produces same hashid."""
        results = []
        lock = threading.Lock()

        def encode_value():
            h = Hashid(42, salt="consistent-salt")
            with lock:
                results.append(h.hashid)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(encode_value) for _ in range(50)]
            concurrent.futures.wait(futures)

        # All results should be identical
        assert len(set(results)) == 1

    def test_concurrent_decoding(self):
        """Decoding works correctly under concurrent access."""
        # Create a known hashid
        h = Hashid(12345, salt="decode-test")
        hashid_str = h.hashid

        results = []
        lock = threading.Lock()

        def decode_hashid():
            decoded = Hashid(hashid_str, salt="decode-test")
            with lock:
                results.append(decoded.id)

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(decode_hashid) for _ in range(50)]
            concurrent.futures.wait(futures)

        # All decoded values should be the same
        assert all(r == 12345 for r in results)

    def test_field_encoding_thread_safety(self):
        """Field encoding is thread-safe."""
        from hashid_field import HashidField

        field = HashidField(salt="field-test")
        results = []
        lock = threading.Lock()

        def encode_with_field(value):
            encoded = field.encode_id(value)
            with lock:
                results.append((value, str(encoded)))

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(encode_with_field, i) for i in range(100)]
            concurrent.futures.wait(futures)

        assert len(results) == 100

        # Same values should produce same hashids
        value_to_hashid = {}
        for value, hashid in results:
            if value in value_to_hashid:
                assert value_to_hashid[value] == hashid
            else:
                value_to_hashid[value] = hashid

    def test_concurrent_mixed_operations(self):
        """Mixed encode/decode operations are thread-safe."""
        salt = "mixed-ops"
        errors = []
        lock = threading.Lock()

        def operation(i):
            try:
                if i % 2 == 0:
                    # Encode
                    h = Hashid(i, salt=salt)
                    # Immediately verify decode
                    decoded = Hashid(h.hashid, salt=salt)
                    assert decoded.id == i
                else:
                    # Create and verify
                    h1 = Hashid(i, salt=salt)
                    h2 = Hashid(i, salt=salt)
                    assert h1.hashid == h2.hashid
            except AssertionError as e:
                with lock:
                    errors.append((i, str(e)))

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(operation, i) for i in range(200)]
            concurrent.futures.wait(futures)

        assert len(errors) == 0, f"Errors occurred: {errors}"
