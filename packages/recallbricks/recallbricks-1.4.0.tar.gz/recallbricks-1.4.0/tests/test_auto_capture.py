"""
Test auto-capture functionality for RecallBricks Python SDK
"""

from recallbricks import RecallBricks
import time

# Initialize RecallBricks client
rb = RecallBricks(
    "rbk_secret_2025_x7h2p9",
    base_url="https://recallbricks-api-production.up.railway.app"
)

# Test auto-capture decorator
@rb.capture_function()
def process_email(sender, subject):
    """Simulate email processing"""
    return f"Processed email from {sender} about {subject}"

# Test auto-capture with custom settings
@rb.capture_function(save_inputs=True, save_outputs=True, include_errors=True)
def analyze_data(data_points):
    """Simulate data analysis"""
    if not data_points:
        raise ValueError("No data points provided")
    return {"total": len(data_points), "average": sum(data_points) / len(data_points)}

# Test auto-capture with error handling
@rb.capture_function(include_errors=True)
def risky_operation(value):
    """Simulate an operation that might fail"""
    if value < 0:
        raise ValueError("Value must be positive")
    return value * 2


if __name__ == "__main__":
    print("Testing RecallBricks Auto-Capture Functionality\n")
    print("=" * 50)

    # Test 1: Basic function capture
    print("\nTest 1: Basic email processing")
    result1 = process_email("boss@company.com", "Q4 Report")
    print(f"Function result: {result1}")

    # Test 2: Data analysis with multiple inputs
    print("\nTest 2: Data analysis")
    result2 = analyze_data([10, 20, 30, 40, 50])
    print(f"Analysis result: {result2}")

    # Test 3: Error handling
    print("\nTest 3: Error handling")
    try:
        result3 = risky_operation(-5)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # Test 4: Successful risky operation
    print("\nTest 4: Successful risky operation")
    result4 = risky_operation(10)
    print(f"Result: {result4}")

    # Wait for embeddings to process
    print("\n" + "=" * 50)
    print("\nWaiting 2 seconds for embeddings to process...")
    time.sleep(2)

    # Verify memories were saved
    print("\nVerifying saved memories:")
    try:
        memories = rb.get_all(limit=10)
        print(f"\nFound {len(memories)} recent memories:")
        for i, memory in enumerate(memories[:5], 1):
            print(f"{i}. [{memory.get('source', 'unknown')}] {memory.get('text', '')[:80]}...")
    except Exception as e:
        print(f"Error retrieving memories: {e}")

    print("\n" + "=" * 50)
    print("Auto-capture tests completed!")
