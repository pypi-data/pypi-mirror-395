# NSEC3 Hash Utility

This project provides a Python CLI tool to compute the [NSEC3](https://datatracker.ietf.org/doc/html/rfc5155#section-4) hash for a Fully-Qualified Domain Name (FQDN). The NSEC3 hash is commonly used in DNSSEC deployments to provide authenticated denial of existence without leaking zone contents.

## Features

- Converts a domain name into its canonical DNS wire format.
- Hashes the name using SHA-1 with optional salt and iterations, as defined by the NSEC3 specification.
- Outputs the hash as an NSEC3-compliant Base32hex string (without padding, using characters `0-9` and `A-V`).

## Usage

1. **Ensure your input is a Fully-Qualified Domain Name (FQDN):**
   - The name **must** end with a dot (e.g., `www.example.com.`).
   - The trailing dot denotes the root of the DNS tree; omitting it will canonicalize the name by appending a dot automatically, but for correctness and standard compliance, always provide FQDN.

2. **Running from the command line:**

   ```
   python3 hash_nsec3.py <name> [--salt SALT] [--iterations N]
   ```

   - `<name>`: The domain name to hash, e.g., `host.example.com.`
   - `--salt SALT`: _(Optional)_ Hexadecimal salt string, e.g., `AABBCCDD` (default is no salt).
   - `--iterations N`: _(Optional)_ Number of **additional** hash iterations (default: 0).

   ### Examples

   ```
   python3 hash_nsec3.py www.example.com.
   python3 hash_nsec3.py www.example.com. --salt AABBCC
   python3 hash_nsec3.py www.example.com. --salt AABBCC --iterations 5
   ```


## About NSEC3 Hashing

- **Canonicalization:** The tool converts domain names to the DNS wire format (length-prefixed labels, lowercased).
- **Hashing:** It applies SHA-1, followed by the specified number of additional iterations, salting each hash.
- **Base32hex Encoding:** The raw 20-byte SHA-1 digest is encoded according to RFC 4648 section 7, without padding and using the restricted alphabet.

For example, the hash of `www.example.com.` with no salt and zero iterations will be a 32-character Base32-encoded string, `MIFDNDT3NFF3OD53O7TLA1HRFF95JKUK`

## References

- [RFC 5155 - DNSSEC Hashed Authenticated Denial of Existence (NSEC3)](https://datatracker.ietf.org/doc/html/rfc5155)
- [RFC 4648 - The Base16, Base32, and Base64 Data Encodings](https://datatracker.ietf.org/doc/html/rfc4648#section-7)

## Alternatives

ISC have a similar command, called [`nsec3hash`](https://gitlab.isc.org/isc-projects/bind9/-/blob/v9.9.1-P4/bin/tools/nsec3hash.c?ref_type=tags) written in C as part of [BIND](https://www.isc.org/bind/)

