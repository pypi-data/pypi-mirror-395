"""
Test script for the enhanced dumps.py functionality
"""

import datetime
import decimal

from flight_profiler.common.dumps import encode_obj_to_transfer


def test_basic_types():
    print("Testing basic types:")

    # Test string
    print(f"String: {encode_obj_to_transfer('hello')}")

    # Test number
    print(f"Integer: {encode_obj_to_transfer(42)}")
    print(f"Float: {encode_obj_to_transfer(3.14)}")
    print(f"Complex: {encode_obj_to_transfer(1+2j)}")

    # Test boolean and None
    print(f"True: {encode_obj_to_transfer(True)}")
    print(f"False: {encode_obj_to_transfer(False)}")
    print(f"None: {encode_obj_to_transfer(None)}")

    print()

def test_collections():
    print("Testing collections:")

    # Test list
    print(f"List: {encode_obj_to_transfer([1, 2, 3])}")

    # Test tuple
    print(f"Tuple: {encode_obj_to_transfer((1, 2, 3))}")
    print(f"Single element tuple: {encode_obj_to_transfer((1,))}")
    print(f"Empty tuple: {encode_obj_to_transfer(())}")

    # Test set
    print(f"Set: {encode_obj_to_transfer({3, 1, 2})}")
    print(f"Empty set: {encode_obj_to_transfer(set())}")

    # Test nested structures
    nested = {
        'list': [1, 2, {'nested': 'dict'}],
        'tuple': (1, 2, 3),
        'set': {1, 2, 3}
    }
    print(f"Nested: {encode_obj_to_transfer(nested)}")

    print()

def test_special_types():
    print("Testing special types:")

    # Test datetime
    dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
    print(f"Datetime: {encode_obj_to_transfer(dt)}")

    # Test date
    date = datetime.date(2023, 10, 5)
    print(f"Date: {encode_obj_to_transfer(date)}")

    # Test time
    time = datetime.time(14, 30, 45)
    print(f"Time: {encode_obj_to_transfer(time)}")

    # Test decimal
    dec = decimal.Decimal('3.14159')
    print(f"Decimal: {encode_obj_to_transfer(dec)}")

    # Test bytes
    b = b'hello world'
    print(f"Bytes: {encode_obj_to_transfer(b)}")

    print()

def test_custom_objects():
    print("Testing custom objects:")

    class TestClass:
        def __init__(self):
            self.attr1 = "value1"
            self.attr2 = 42
            self._private = "private_value"

    obj = TestClass()
    print(f"Custom object: {encode_obj_to_transfer(obj)}")

    print()

def test_depth_limiting():
    print("Testing depth limiting:")

    # Deeply nested structure
    deep = {'a': {'b': {'c': {'d': {'e': 'value'}}}}}
    print(f"Deep structure at max_depth=3: {encode_obj_to_transfer(deep, max_depth=3)}")
    print(f"Deep structure at max_depth=5: {encode_obj_to_transfer(deep, max_depth=5)}")

    print()

def test_verbose_mode():
    large_list = list(range(100))
    print("=== Testing with large list (verbose=False) ===")
    result_verbose_false = encode_obj_to_transfer(large_list, verbose=False)
    print(result_verbose_false)
    print("\n=== Testing with large list (verbose=True) ===")
    result_verbose_true = encode_obj_to_transfer(large_list, verbose=True)
    print(result_verbose_true)

    print("\n" + "=" * 50)

    # Test with a large dictionary
    large_dict = {f"key_{i}": f"value_{i}" for i in range(100)}
    print("=== Testing with large dict (verbose=False) ===")
    result_dict_verbose_false = encode_obj_to_transfer(large_dict, verbose=False)
    print(result_dict_verbose_false)
    print("\n=== Testing with large dict (verbose=True) ===")
    result_dict_verbose_true = encode_obj_to_transfer(large_dict, verbose=True)
    print(result_dict_verbose_true)


if __name__ == "__main__":
    print("Running tests for dumps.py enhanced functionality\n")

    test_basic_types()
    test_collections()
    test_special_types()
    test_custom_objects()
    test_depth_limiting()

    print("All tests completed!")
