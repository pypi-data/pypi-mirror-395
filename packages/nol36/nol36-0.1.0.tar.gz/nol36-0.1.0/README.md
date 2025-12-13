# NOL36 Encoding Scheme - Technical Yellow Paper

## Abstract

**NOL36** is a base-36 encoding protocol designed for robust, portable, and verifiable data representation across constrained and standard computing environments. It combines compact alphanumeric encoding with a chunking architecture, versioning system, and integrity verification to enable reliable data transmission, storage, and inter-process communication in contexts ranging from embedded systems to WebAssembly modules.

---

## 1. Design Principles

NOL36 is architected around four core principles:

1. **Universality**: Operates identically in `std`, `no_std`, and WebAssembly environments without protocol changes
2. **Scalability**: Handles arbitrary data sizes through transparent chunking with minimal overhead
3. **Verifiability**: Provides per-chunk integrity checking and protocol version negotiation
4. **Portability**: Produces output using only unambiguous alphanumeric characters (0-9, A-Z) suitable for URLs, filenames, and human inspection

---

## 2. Mathematical Foundation

### 2.1 Numeral System

Let **D₃₆** be the digit set `{0,1,...,9,A,B,...,Z}` representing values `0` to `35`. Each symbol `s ∈ D₃₆` encodes **log₂(36) ≈ 5.1699** bits of information, yielding an encoding efficiency of **64.0%** relative to binary.

### 2.2 Alphabet Mapping

The bijective function `φ: [0,35] → D₃₆` is defined as:
```
φ(d) = 
  d + 48          if 0 ≤ d ≤ 9    (ASCII '0'-'9')
  d + 55          if 10 ≤ d ≤ 35  (ASCII 'A'-'Z')
```

---

## 3. Data Structures

### 3.1 Chunk Metadata

All encoded payloads carry a self-describing header:

```
Header = { version: u8, type: u8, index: u32 }
```

**Constraints:**
- `version < 64` (6-bit version space)
- `type = 0` (binary payload type)
- `index` sequence begins at 0; final chunk sets bit 31 (`index | 0x80000000`)

### 3.2 Payload Formats

NOL36 defines three payload structures:

#### Format A: Compact Payload (Single Message)
For `len(data) ≤ 255`:
```
[PREFIX:8=0x01][VERSION:8][TYPE:8=0x00][LEN:8][DATA:8×LEN]
```
*No checksum; length field provides implicit validation.*

#### Format B: Data Chunk (Multi-Part)
```
[PREFIX:8=0x01][VERSION:8][TYPE:8=0x00][INDEX:32][CHECKSUM:32][DATALEN:32][DATA:8×DATALEN]
```
`CHECKSUM = Σ(data[i]) mod 2³²` (additive rolling sum)

#### Format C: Finalization Chunk (Stream Terminator)
```
[PREFIX:8=0x01][VERSION:8][TYPE:8=0x00][INDEX:32|0x80000000][0:32][0:32]
```
Signals end of chunk sequence; carries no data.

---

## 4. Encoding Algorithm

### 4.1 Base-36 Conversion

The function `ENCODE36: Byte[] → D₃₆*` performs arbitrary-precision base conversion:

1. **Input**: Byte array `B` prefixed with `0x01`
2. **Process**: Treat `B` as big-endian integer `N`; repeatedly divide `N` by 36, emitting remainders
3. **Output**: Reverse of remainder sequence mapped through `φ`

**Termination**: Conversion stops when quotient reaches zero. If no digits produced, emit `'0'`.

### 4.2 Chunking Strategy

For input data `D` where `|D| > 255`:

1. **Split**: Partition `D` into contiguous blocks `C₀, C₁, ..., Cₙ₋₁` where `|Cᵢ| = 64` (configurable)
2. **Encode**: Each block `Cᵢ` → Format B chunk with `INDEX = i`
3. **Terminate**: Append Format C chunk with `INDEX = n | 0x80000000`
4. **Join**: Concatenate all base36 strings with delimiter `'.'`

### 4.3 Parallelization

When `std` feature is enabled, encoding of independent chunks utilizes available parallelism:
```
threads = min(available_parallelism(), chunk_count)
```
Each thread processes a disjoint subset of chunks; results are reassembled in order.

---

## 5. Decoding Algorithm

### 5.1 Base-36 Decoding

The function `DECODE36: D₃₆* → Byte[]` performs inverse conversion:

1. **Input**: String `S` over alphabet `D₃₆`
2. **Process**: Parse as base-36 integer; expand to byte array in big-endian order
3. **Validation**: Reject if first byte ≠ `0x01`

### 5.2 State Machine Parser

The decoder maintains state `Σ = {expv: Option<u8>, rcvd: Vec<(index, Chunk)>}`

**State Transitions:**
- **Init**: `expv = None`, `rcvd = []`
- **Feed(chunk)**:
  - Parse chunk; reject on checksum/version mismatch
  - Insert `(index, chunk)` into `rcvd`
  - If `index` has bit 31 set → **Finalize**
  - Else → **Continue**
- **Finalize**: Sort `rcvd` by index; verify contiguous sequence `0..n`; concatenate data payloads

---

## 6. Feature Analysis

### 6.1 Strengths

| Feature | Benefit | Implementation |
|---------|---------|----------------|
| **Alphabet Efficiency** | 36% more compact than hex; human-readable | Fixed 36-symbol set, no padding |
| **Environmental Portability** | Runs on microcontrollers to servers | `no_std` + custom WASM allocator |
| **Scalable Throughput** | No hard size limits | Automatic chunking with 64-byte blocks |
| **Version Governance** | Protocol evolution without breaking changes | Embedded 6-bit version field |
| **Weak-Link Integrity** | Detects random corruption per chunk | Fast additive checksum (Σ data) |
| **Parallel Speedup** | Leverages multicore for large data | Work-stealing chunk distribution |
| **Streaming Decoding** | Memory-efficient for large messages | State-based incremental assembly |
| **URL Safety** | No escaping required | Alphanumeric-only output |
| **Deterministic Output** | Same input → same encoding | No randomization or compression |

### 6.2 Trade-offs

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| **Checksum Strength** | Additive sum (weak) | Speed over cryptographic security; suitable for transmission errors, not malicious tampering |
| **Chunk Size** | 64 bytes default | Balances overhead (14-byte header) vs. flexibility; tunable per use-case |
| **Alphabet Size** | Base-36 (not 64) | Avoids `-` and `_` symbols; maximizes human readability |
| **No Compression** | Raw data only | Keeps implementation simple; compression should be applied at application layer |
| **Version Encoding** | 6-bit limit | Sufficient space for protocol evolution; keeps header compact |

---

## 7. Comparative Performance

### 7.1 Efficiency Metrics

| Encoding | Bits/Char | Overhead (100B) | Human Readable | Chunking | Versioning |
|----------|-----------|-----------------|----------------|----------|------------|
| **Hex** | 4.0 | 100% | ✅ | ❌ | ❌ |
| **Base64** | 6.0 | 33% | ❌ | ❌ | ❌ |
| **Base64URL** | 6.0 | 33% | ❌ | ❌ | ❌ |
| **NOL36** | 5.17 | 42% | ✅ | ✅ | ✅ |
| **Ascii85** | 6.4 | 25% | ❌ | ❌ | ❌ |

*Overhead calculated for 100-byte payload; NOL36 overhead drops significantly for larger data due to chunking.*

### 7.2 Computational Complexity

- **Encode**: `O(n)` time, `O(n)` space
- **Decode**: `O(n)` time, `O(n)` space
- **Checksum**: `O(chunk_size)` per chunk, negligible overhead
- **Parallel Speedup**: Near-linear up to `min(chunks, cores)`

---

## 8. Use Cases & Applications

### 8.1 Embedded Systems
- **Firmware Updates**: Chunked delivery with integrity verification over serial/UART
- **Data Logging**: Compact alphanumeric logs stored in EEPROM
- **Protocol Buffers**: Versioned message exchange between device generations

### 8.2 WebAssembly
- **Host-Module Communication**: Passing structured data across WASM boundary without binary corruption
- **Blockchain**: Embedding versioned transaction data in smart contracts
- **Browser Storage**: URL-safe encoding for `localStorage`/`sessionStorage`

### 8.3 Network Protocols
- **IoT Sensor Data**: Low-bandwidth transmission over MQTT/CoAP
- **URL Shorteners**: Encoding binary metadata in short URLs
- **QR Codes**: Maximizing data density in alphanumeric mode

### 8.4 Cross-Platform Tooling
- **Configuration Files**: Human-editable binary config encoding
- **Debug Symbols**: Versioned symbol tables portable across toolchains
- **Database Keys**: Compact primary keys with embedded versioning

---

## 9. Implementation Reference

### 9.1 Core WASM Module

The NOL36 encoding logic is compiled to a single **nol36.wasm** module that exports the following functions:

```
// Memory Management
nol36_alloc(size: usize) -> *mut u8
nol36_free_alloc(ptr: *mut u8, size: usize)
nol36_free_with_len(ptr: *mut u8, len: usize)

// Encoding
nol36_encode_init(max_chunk_size: usize) -> i32
nol36_encode_feed(input_ptr: *const u8, input_len: usize) -> i32
nol36_encode_finalize(out_ptr_ptr: *mut u8, out_len_ptr: *mut u8) -> i32

// Decoding
nol36_decode_init() -> i32
nol36_decode_feed(chunk_ptr: *const u8, chunk_len: usize) -> i32
nol36_decode_finalize(out_ptr_ptr: *mut u8, out_len_ptr: *mut u8) -> i32

// Diagnostics
nol36_scratch_ptr() -> *mut u8  // Returns 14-byte debug buffer
```

The module uses a linear memory model with explicit allocation/deallocation. All string data is UTF-8 encoded. The scratch pointer provides diagnostic information about the most recently processed chunk (valid flag, version, index, checksum, data length).

### 9.2 Language-Specific Bindings

#### Rust Implementation

The Rust binding uses `wasmtime` for efficient WASM execution with full error propagation and thread safety.

**Installation:**
```toml
[dependencies]
nol36 = { path = "bindings/rust" }
```

**API:**
```rust
use nol36::{init, encode, decode, InitOptions, Nol36Error};

pub fn init(opts: Option<InitOptions>) -> Result<(), Nol36Error>
pub fn encode(data: &[u8]) -> Result<String, Nol36Error>
pub fn decode(encoded: &str) -> Result<Vec<u8>, Nol36Error>
```

**Initialization Options:**
```rust
pub struct InitOptions {
    pub diagnostics: bool,  // Enables all diagnostics
    pub feed: bool,         // Logs feed operation results
    pub chunks: bool,       // Logs chunk metadata via scratch buffer
}
```

**Usage Example:**
```rust
fn main() {
    // Initialize with diagnostic options
    init(Some(InitOptions {
        diagnostics: false,
        feed: false,
        chunks: false,
    })).expect("Failed to initialize nol36");

    let data = b"Programmable Transaction Blocks...";
    
    let encoded = encode(data).unwrap();
    println!("Encoded: {}", encoded);  // Base36 string, possibly with '.' delimiters
    
    let decoded = decode(&encoded).unwrap();
    assert_eq!(data, decoded.as_slice());
}
```

**Error Handling:**
- `Nol36Error::NotInitialized` - Call `init()` first
- `Nol36Error::InvalidInput` - Invalid UTF-8 or allocation failure
- `Nol36Error::FunctionError(i32)` - WASM function returned error code
- `Nol36Error::WasmRuntime` - WASM execution or memory access error

**Thread Safety:** The WASM instance is stored in a `OnceLock` with a `Mutex`-wrapped `Store`, enabling safe concurrent access from multiple threads.

---

#### JavaScript Implementation

The JavaScript binding provides universal module support for Node.js and browsers, with automatic WASM loading.

**Installation:**
```bash
npm install nol36  # Includes nol36.wasm in lib/
```

**API:**
```javascript
async function init(opts?: {
  diagnostics?: boolean,
  FEED?: boolean,
  CHUNKS?: boolean
}): Promise<void>

function encode(data: Uint8Array): string
function decode(encoded: string): Uint8Array
```

**Usage Example:**
```javascript
const { init, encode, decode } = require('./nol36');

async function main() {
  // Initialize WASM with diagnostics
  await init({ CHUNKS: false, FEED: false });

  const original = new TextEncoder().encode('Programmable Transaction Blocks...');
  const encoded = encode(original);
  console.log('Encoded:', encoded);  // String like "14A9B..."

  const decoded = decode(encoded);
  console.log('Match:', Buffer.compare(original, decoded) === 0);
}

main().catch(console.error);
```

**WASM Loading Behavior:**
- **Node.js**: Loads WASM from filesystem via `fs.readFileSync`
- **Browser**: Fetches WASM from `/nol36.wasm` endpoint
- Both environments return the same API after initialization

**Error Handling:** Throws standard JavaScript `Error` objects with descriptive messages for initialization failures, invalid input types, and WASM function errors.

**Diagnostics:** When enabled, logs chunk metadata to console including version, index, checksum, and data length in real-time during decode operations.

---

#### Python Implementation

The Python binding uses `wasmtime-py` for runtime execution, supporting both development and PyInstaller-frozen deployments.

**Installation:**
```bash
pip install nol36  # Installs wasmtime dependency
```

**API:**
```python
async def init(opts: Optional[Dict[str, Any]] = None) -> None
def encode(data: bytes) -> str
def decode(encoded: str) -> bytes
```

**Initialization Options:**
```python
{
    "diagnostics": bool,  # Enables all diagnostics
    "FEED": bool,         # Logs feed operation results
    "CHUNKS": bool,       # Logs chunk metadata
}
```

**Usage Example:**
```python
import asyncio
from nol36 import init, encode, decode

async def main():
    # Initialize WASM runtime
    await init({"CHUNKS": False, "FEED": False})
    
    original_text = 'Programmable Transaction Blocks...'
    original = original_text.encode('utf-8')
    
    encoded = encode(original)
    print('Encoded:', encoded)  # Base36 string
    
    decoded = decode(encoded)
    print('Match:', original == decoded)

if __name__ == "__main__":
    asyncio.run(main())
```

**WASM Loading:**
- Searches for `nol36.wasm` in: `lib/`, current directory, and PyInstaller's `_MEIPASS`
- Requires `wasmtime` package: `pip install wasmtime`

**Error Handling:**
- `RuntimeError` - WASM initialization failures, function errors
- `TypeError` - Invalid input types (must be `bytes` and `str`)
- `FileNotFoundError` - WASM binary not found
- `ImportError` - `wasmtime` not installed

**Diagnostics:** Prints chunk analysis to stdout when enabled, showing version, index, checksum, and data length for each processed chunk.

---

## 9.3 Portability Guarantees

- **Memory Model**: Custom bump allocator for WASM targets (128KB heap) with explicit ownership
- **Thread Safety**: Rust binding uses `OnceLock` + `Mutex`; JavaScript/Python bindings use single-threaded WASM runtime
- **WASM Isolation**: All language bindings run the same `nol36.wasm` bytecode, ensuring bit-identical output across platforms
- **Panic Handling**: WASM module traps are converted to language-native errors (`Result`, `try/catch`, `try/except`)

---

## 10. Security Considerations

**Threat Model**: NOL36 is designed for **integrity**, not **confidentiality** or **authenticity**.

- **Collision Resistance**: Additive checksum is vulnerable to intentional collision.
- **DoS Resistance**: Chunk count limited by available memory; untrusted input should be size-limited
- **Version Rollback**: Attacker cannot downgrade version without breaking checksum validation
- **Injection**: Alphanumeric output prevents shell/JSON/SQL injection when used as string literal
- **WASM Sandboxing**: Language bindings execute WASM in a sandboxed environment with no system access

---

## 12. Conclusion

NOL36 occupies a unique design point: more compact than hex, more portable than base64, and more robust than either through integrated chunking and versioning. Its `no_std` foundation and WASM-native design make ideal for the emerging edge computing landscape where efficiency, readability, and reliability converge. The unified WASM core ensures consistent behavior across Rust, JavaScript, and Python environments while preserving idiomatic APIs for each ecosystem.