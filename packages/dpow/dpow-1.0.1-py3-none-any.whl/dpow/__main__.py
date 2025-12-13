import sys
import os

# Support both direct execution and module execution
if __package__ is None or __package__ == '':
    # Direct execution: add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from dpow.client import PoWClient, create_multi_pow_challenge
    from dpow.server import PoWServer
    from dpow.downloader import ensure_binaries
else:
    # Module execution
    from .client import PoWClient, create_multi_pow_challenge
    from .server import PoWServer
    from .downloader import ensure_binaries

# Test parameters
TEST_TEXT = b"hello world"
DIFFICULTY = 12
MAX_NONCE = 100000000

def run_tests():
    # Ensure binaries are present
    ensure_binaries()

    print("=" * 80)
    print("Enhanced Proof-of-Work Test Suite")
    print("=" * 80)
    
    # Initialize client and server
    try:
        client = PoWClient()
        server = PoWServer()
    except (FileNotFoundError, OSError) as e:
        print(f"\nERROR: Failed to load DLL files")
        print(f"{e}")
        return

    # ============================================================================
    # PART 1: Single Hash Algorithm Tests
    # ============================================================================
    print("\n" + "=" * 80)
    print("PART 1: Single Hash Algorithm Tests")
    print("=" * 80)
    
    single_tests = [
        "MD4",
        "MD5", 
        "SHA2-256",
        "BLAKE2s-256",
        "SHA3-256"
    ]
    
    for algo in single_tests:
        print(f"\n{algo}:")
        result = client.generate_single(TEST_TEXT, algo, DIFFICULTY, 0, MAX_NONCE)
        
        if result['success']:
            print(f"  Nonce: {result['nonce']}")
            print(f"  Hash:  {client.hash_to_hex(result['hash'])}")
            
            # Verify
            valid = server.verify_single(TEST_TEXT, result['nonce'], algo, DIFFICULTY)
            status = "PASSED" if valid else "FAILED"
            print(f"  Verification: {status}")
        else:
            print(f"  FAILED: No nonce found within {MAX_NONCE} attempts")
    
    # ============================================================================
    # PART 2: Multi-Hash PoW Tests
    # ============================================================================
    print("\n" + "=" * 80)
    print("PART 2: Multi-Hash Proof-of-Work Tests")
    print("=" * 80)
    
    # FAST Multi-Hash (4 algorithms)
    print("\n" + "-" * 80)
    print("Test 1: Fast Multi-Hash (4 algorithms)")
    print("-" * 80)
    algos_test1 = create_multi_pow_challenge(4, DIFFICULTY)
    print(f"Algorithms: {', '.join(algos_test1)}")
    
    result = client.generate_multi(TEST_TEXT, algos_test1, DIFFICULTY, 0, MAX_NONCE)
    if result['success']:
        print(f"Nonce found: {result['nonce']}")
        
        # Verify
        valid = server.verify_multi(TEST_TEXT, result['nonce'], algos_test1, DIFFICULTY)
        status = "PASSED" if valid else "FAILED"
        print(f"\nVerification: {status}")
    else:
        print(f"FAILED: No nonce found")

if __name__ == "__main__":
    run_tests()
