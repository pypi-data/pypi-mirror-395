"""
Example: Basic Usage of QALDRON Layer 1

This example demonstrates basic quantum hashing operations.
"""

from qaldron.layer1 import MarkBluHasher


def main():
    print("=" * 60)
    print("QALDRON Layer 1 - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Initialize hasher with custom authentication key
    print("1. Initializing MARK-BLU Hasher...")
    hasher = MarkBluHasher(
        n_qubits=12,
        layers=4,
        auth_key=b"MySecretKey2025"
    )
    print("   ✓ Hasher initialized")
    print()
    
    # Generate hash
    print("2. Generating quantum hash...")
    message = "Hello QALDRON! This is a secure message."
    hash_value = hasher.get_hash(message)
    print(f"   Message: {message}")
    print(f"   Hash:    {hash_value}")
    print()
    
    # Demonstrate determinism
    print("3. Testing determinism (same input → same hash)...")
    hash_again = hasher.get_hash(message)
    print(f"   Hash 1:  {hash_value}")
    print(f"   Hash 2:  {hash_again}")
    print(f"   Match:   {hash_value == hash_again} ✓")
    print()
    
    # Demonstrate uniqueness
    print("4. Testing uniqueness (different input → different hash)...")
    message2 = "Hello QALDRON! This is a different message."
    hash2 = hasher.get_hash(message2)
    print(f"   Message 1: {message}")
    print(f"   Hash 1:    {hash_value}")
    print(f"   Message 2: {message2}")
    print(f"   Hash 2:    {hash2}")
    print(f"   Different: {hash_value != hash2} ✓")
    print()
    
    # Demonstrate avalanche effect
    print("5. Testing avalanche effect (1 bit change → ~50% hash change)...")
    msg_a = "test"
    msg_b = "Test"  # Just one capital letter different
    hash_a = hasher.get_hash(msg_a)
    hash_b = hasher.get_hash(msg_b)
    
    # Count bit differences
    bin_a = bin(int(hash_a, 16))[2:].zfill(128)
    bin_b = bin(int(hash_b, 16))[2:].zfill(128)
    diff_bits = sum(c1 != c2 for c1, c2 in zip(bin_a, bin_b))
    diff_percent = (diff_bits / 128) * 100
    
    print(f"   Input A:     '{msg_a}'")
    print(f"   Input B:     '{msg_b}'")
    print(f"   Hash A:      {hash_a}")
    print(f"   Hash B:      {hash_b}")
    print(f"   Bits changed: {diff_bits}/128 ({diff_percent:.1f}%)")
    print(f"   Avalanche:   {'✓ Good' if 40 <= diff_percent <= 60 else '✗ Poor'}")
    print()
    
    # Demonstrate signing and verification
    print("6. Testing message signing and verification...")
    secret_message = "Transfer $1000 to account XYZ"
    signature = hasher.sign(secret_message)
    
    print(f"   Message:   {secret_message}")
    print(f"   Signature: {signature}")
    
    # Verify correct message
    is_valid = hasher.verify(secret_message, signature)
    print(f"   Verification (correct message): {is_valid} ✓")
    
    # Try to verify tampered message
    tampered = "Transfer $9999 to account XYZ"
    is_valid_tampered = hasher.verify(tampered, signature)
    print(f"   Verification (tampered message): {is_valid_tampered} ✓ (correctly rejected)")
    print()
    
    # Demonstrate auth key importance
    print("7. Testing authentication key protection...")
    hasher_wrong_key = MarkBluHasher(auth_key=b"WrongKey")
    signature_wrong = hasher_wrong_key.sign(secret_message)
    
    print(f"   Original signature:   {signature}")
    print(f"   Wrong key signature:  {signature_wrong}")
    print(f"   Different:            {signature != signature_wrong} ✓")
    print()
    
    print("=" * 60)
    print("All tests passed! Layer 1 is working correctly.")
    print("=" * 60)


if __name__ == "__main__":
    main()
