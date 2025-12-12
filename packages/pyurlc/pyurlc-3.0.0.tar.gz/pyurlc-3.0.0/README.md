# pyurlc

Ultra-fast URL encoding/decoding in C with SIMD optimizations (30-35x faster than urllib.parse)

## Features

- **30-35x faster** than Python's `urllib.parse`
- **SIMD optimized** (ARM NEON / x86 SSE)
- **Fully compatible** with `urllib.parse` API
- **Memory efficient** with proper allocation
- **Full Unicode support**
- **Error handling** with strict/replace/ignore modes

## Installation

```bash
pip install pyurlc
```

Usage

```python
import pyurlc

# Basic encoding/decoding
encoded = pyurlc.encode("Hello World!")
decoded = pyurlc.decode(encoded)

# Quote/Unquote (compatible with urllib.parse)
quoted = pyurlc.quote("test@example.com")
unquoted = pyurlc.unquote(quoted)

# Quote/Unquote with plus signs
quoted_plus = pyurlc.quote_plus("Hello World")
unquoted_plus = pyurlc.unquote_plus(quoted_plus)

# Check if string is encoded
is_encoded = pyurlc.is_encoded("Hello%20World")  # True

# Get performance info
info = pyurlc.performance_info()
```

Performance

String Size pyurlc urllib.parse Speedup
100 chars 0.003s 0.111s 33.7x
1,000 chars 0.028s 0.986s 34.6x
10,000 chars 0.354s 11.049s 31.2x
50,000 chars 1.973s 59.572s 30.2x

Average speedup: 32.4x

License

Apache License 2.0

# Thank you for using my project!
# Goobye!