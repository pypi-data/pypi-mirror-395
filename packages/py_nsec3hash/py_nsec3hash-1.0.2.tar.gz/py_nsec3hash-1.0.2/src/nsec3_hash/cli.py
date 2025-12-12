#!/usr/bin/env python3

import hashlib
import binascii
import struct
import argparse

__version__ = "1.0.1"

# RFC 4648, section 7: Base 32 Encoding with Extended Hex Alphabet
# NSEC3 requires this alphabet ('0'-'9' and 'A'-'V') and no padding.
NSEC3_BASE32_ALPHABET: str = "0123456789ABCDEFGHIJKLMNOPQRSTUV"

def canonicalize_name(name: str) -> bytes:
    """
    Converts a DNS name string to its canonical wire format (length-prefixed labels).

    Example: 'www.example.com.' -> b'\x03www\x07example\x03com\x00'
    The input name MUST be fully qualified (end with a dot) for correct canonicalization.
    DNS names are case-insensitive, so they are lowercased for canonical form.

    Input names without a trailing dot will be appended with a dot.
    """
    if not name.endswith('.'):
        name += '.'
    
    name_bytes = name.lower().encode('ascii')
    
    canonical_bytes = b''
    for label in name_bytes.split(b'.'):
        if not label:
            # Reached the root label (after the final dot)
            break
        # Prepend the length octet to the label bytes
        canonical_bytes += struct.pack('!B', len(label)) + label
    
    # The final label (root) is represented by a single zero octet.
    canonical_bytes += b'\x00'
    return canonical_bytes

def nsec3_hash(name_str: str, salt_hex: str, iterations: int) -> str:
    """
    Computes the NSEC3 hash of a domain name using the iterative SHA-1 algorithm.

    :param name_str: The domain name string (e.g., 'www.example.com.').
    :param salt_hex: The NSEC3 salt as a hexadecimal string (e.g., 'AABBCCDD').
    :param iterations: The number of ADDITIONAL hashing iterations (integer, 0 or greater).
    :return: The Base32-encoded NSEC3 hash string.
    """
    # 1. Canonicalize the name
    canonical_name = canonicalize_name(name_str)
    
    # 2. Decode the salt from hex to bytes
    salt_bytes = binascii.unhexlify(salt_hex) if salt_hex else b''
    
    # NSEC3 Hashing: (iterations + 1) applications of SHA-1.
    
    # Initial hash (k=0): H_0 = SHA-1(Canonical(n) || s)
    input_bytes = canonical_name + salt_bytes
    current_hash = hashlib.sha1(input_bytes).digest()
    
    # Subsequent hashes (k=1 to iterations): H_k = SHA-1(H_{k-1} || s)
    for i in range(1, iterations + 1):
        input_bytes = current_hash + salt_bytes
        current_hash = hashlib.sha1(input_bytes).digest()
    
    # 3. Base32 (with special alphabet) Encode the final hash
    # SHA-1 produces 20 bytes (160 bits), which is exactly 32 Base32 characters (32 * 5 bits = 160).
    
    base32_hash = ''
    hash_int = int.from_bytes(current_hash, byteorder='big')
    
    # Process 32 chunks of 5 bits each.
    for i in range(32):
        shift = (31 - i) * 5
        index = (hash_int >> shift) & 0b11111 
        base32_hash += NSEC3_BASE32_ALPHABET[index]
        
    return base32_hash

def valid_hex(s: str) -> str:
    if s:
        try:
            binascii.unhexlify(s)
        except binascii.Error:
            raise argparse.ArgumentTypeError(f"Salt '{s}' is not a valid hexadecimal string.")
    return s

def main() -> None:
    """Parses command-line arguments and calls the NSEC3 hash function."""
    parser = argparse.ArgumentParser(
        description="Compute the NSEC3 hash of a fully qualified domain name (FQDN).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    # 'name' remains a required positional argument
    parser.add_argument(
        'name',
        type=str,
        help="The FQDN to hash (e.g., 'host.example.com.'). Must end with a dot for canonical form."
    )

    parser.add_argument(
        '-s', '--salt',
        type=valid_hex,
        default="",
        help="The NSEC3 salt value in hexadecimal (e.g., 'AABBCCDD'). (Default: '')"
    )

    parser.add_argument(
        '-i', '--iterations',
        type=int,
        default=0,
        help="The number of ADDITIONAL hashing iterations (integer, e.g., 10 for 11 total hashes). (Default: 0)"
    )
    
    args = parser.parse_args()
    
    hash_value = nsec3_hash(args.name, args.salt, args.iterations)
    print(hash_value)

if __name__ == "__main__":
    main()
