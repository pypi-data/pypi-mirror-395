"""
Demo examples for the api-key-rotator package.

This file demonstrates various usage patterns of the KeyRotator class.
"""

from api_key_rotator import KeyRotator, with_key_rotation
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import random

# Configure logging to see rotation activity
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def example_1_basic_usage():
    """Example 1: Basic key rotation."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Create rotator with 3 keys
    rotator = KeyRotator(['key_alpha', 'key_beta', 'key_gamma'])
    
    # Get keys in round-robin fashion
    for i in range(5):
        key = rotator.get_key()
        print(f"Request {i+1}: Using key '{key}'")
    
    # Mark a key as expired
    print("\nMarking 'key_beta' as expired...")
    rotator.mark_expired('key_beta')
    
    # Continue getting keys (key_beta will be skipped)
    print("\nContinuing rotation (key_beta should be skipped):")
    for i in range(4):
        key = rotator.get_key()
        print(f"Request {i+6}: Using key '{key}'")
    
    # Show statistics
    print("\nStatistics:")
    print(rotator.get_stats())


def example_2_ttl():
    """Example 2: Time-to-live (TTL) functionality."""
    print("\n" + "="*60)
    print("EXAMPLE 2: TTL (Time-to-Live)")
    print("="*60)
    
    # Create rotator with 5-second TTL
    rotator = KeyRotator(
        keys=['short_lived_key_1', 'short_lived_key_2'],
        ttl_seconds=5
    )
    
    print("Using keys (they expire after 5 seconds)...")
    for i in range(3):
        key = rotator.get_key()
        print(f"Request {i+1}: Using key '{key}'")
        time.sleep(1)
    
    print("\nWaiting 5 seconds for TTL to expire...")
    time.sleep(5)
    
    print("\nTrying to get a key after TTL expired...")
    try:
        key = rotator.get_key()
        print(f"Got key: '{key}'")
    except RuntimeError as e:
        print(f"Error: {e}")
        print("All keys expired due to TTL and no key_fetcher configured!")


def example_3_dynamic_fetching():
    """Example 3: Dynamic key fetching."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Dynamic Key Fetching")
    print("="*60)
    
    # Simulated key counter
    key_counter = {'count': 0}
    
    def fetch_new_key():
        """Simulate fetching a new key from an API."""
        key_counter['count'] += 1
        new_key = f"dynamically_fetched_key_{key_counter['count']}"
        print(f"  → Fetching new key: '{new_key}'")
        return new_key
    
    # Create rotator with initial key and fetcher
    rotator = KeyRotator(
        keys=['initial_key'],
        key_fetcher=fetch_new_key
    )
    
    print("Using initial key...")
    key = rotator.get_key()
    print(f"Got key: '{key}'")
    
    print("\nMarking initial key as expired...")
    rotator.mark_expired(key)
    
    print("\nRequesting a new key (should trigger fetcher):")
    key = rotator.get_key()
    print(f"Got key: '{key}'")
    
    print("\nStatistics:")
    stats = rotator.get_stats()
    print(f"Total keys: {stats['total_keys']}")
    print(f"Available keys: {stats['available_keys']}")


def example_4_decorator():
    """Example 4: Using the @with_key_rotation decorator."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Decorator for Automatic Retry")
    print("="*60)
    
    rotator = KeyRotator(['decorator_key_1', 'decorator_key_2', 'decorator_key_3'])
    
    # Simulated API call that fails randomly
    call_count = {'count': 0}
    
    @with_key_rotation(rotator, max_retries=3)
    def simulated_api_call(endpoint, api_key=None):
        """Simulate an API call that might fail."""
        call_count['count'] += 1
        print(f"  Attempt {call_count['count']}: Calling {endpoint} with key '{api_key}'")
        
        # Simulate random failures (for demo purposes)
        if random.random() < 0.6:  # 60% chance of failure
            print(f"  ✗ Failed with key '{api_key}'")
            raise Exception("API rate limit exceeded")
        
        print(f"  ✓ Success with key '{api_key}'")
        return {"status": "success", "data": "some data"}
    
    # Make the API call - it will automatically retry with new keys
    try:
        result = simulated_api_call("/api/users")
        print(f"\nFinal result: {result}")
    except Exception as e:
        print(f"\nAll retries failed: {e}")
    
    print(f"\nTotal attempts made: {call_count['count']}")
    print("\nRotator statistics:")
    print(rotator.get_stats())


def example_5_thread_safety():
    """Example 5: Thread-safe concurrent usage."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Thread-Safe Concurrent Usage")
    print("="*60)
    
    rotator = KeyRotator(['thread_key_A', 'thread_key_B', 'thread_key_C'])
    
    def worker(worker_id):
        """Simulate a worker thread making API calls."""
        key = rotator.get_key()
        # Simulate some work
        time.sleep(random.uniform(0.01, 0.05))
        return f"Worker {worker_id} used key '{key}'"
    
    print("Running 20 concurrent workers...")
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(worker, range(20)))
    
    # Display results
    for result in results[:5]:  # Show first 5
        print(result)
    print(f"... and {len(results) - 5} more workers")
    
    print("\nStatistics after concurrent usage:")
    stats = rotator.get_stats()
    for key, meta in stats['keys_metadata'].items():
        print(f"  {key}: used {meta['use_count']} times")


def example_6_complete_workflow():
    """Example 6: Complete real-world workflow."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Complete Real-World Workflow")
    print("="*60)
    
    # Setup: Create rotator with multiple features
    backup_keys = {'pool': ['backup_key_1', 'backup_key_2']}
    
    def get_backup_key():
        """Fetch a backup key when needed."""
        if backup_keys['pool']:
            key = backup_keys['pool'].pop(0)
            print(f"  → Fetched backup key: '{key}'")
            return key
        raise RuntimeError("No more backup keys available!")
    
    rotator = KeyRotator(
        keys=['primary_key_1', 'primary_key_2', 'primary_key_3'],
        ttl_seconds=10,  # 10 seconds for demo
        key_fetcher=get_backup_key
    )
    
    print("Initial setup with 3 primary keys")
    print(f"Statistics: {rotator.get_stats()['total_keys']} total keys\n")
    
    # Simulate normal operations
    print("Making 5 API calls...")
    for i in range(5):
        key = rotator.get_key()
        print(f"  Call {i+1}: Using '{key}'")
    
    # Simulate a key failure
    print("\nSimulating key failure (marking primary_key_2 as expired)...")
    rotator.mark_expired('primary_key_2')
    
    # Continue operations
    print("\nContinuing operations (expired key should be skipped)...")
    for i in range(3):
        key = rotator.get_key()
        print(f"  Call {i+6}: Using '{key}'")
    
    # Add a new key manually
    print("\nAdding a new key manually...")
    rotator.add_key('manually_added_key')
    
    # Show final statistics
    print("\nFinal Statistics:")
    stats = rotator.get_stats()
    print(f"  Total keys: {stats['total_keys']}")
    print(f"  Available keys: {stats['available_keys']}")
    print(f"  Expired keys: {stats['expired_keys']}")
    print(f"  Has key fetcher: {stats['has_key_fetcher']}")
    print("\n  Key usage details:")
    for key, meta in stats['keys_metadata'].items():
        status = "EXPIRED" if meta['is_expired'] else "ACTIVE"
        print(f"    {key}: {status}, used {meta['use_count']} times")


def main():
    """Run all examples."""
    print("╔" + "="*58 + "╗")
    print("║" + " "*12 + "API KEY ROTATOR - DEMO EXAMPLES" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    # Run all examples
    example_1_basic_usage()
    example_2_ttl()
    example_3_dynamic_fetching()
    example_4_decorator()
    example_5_thread_safety()
    example_6_complete_workflow()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
