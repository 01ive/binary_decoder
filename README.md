# C-to-Python Binary Protocol Decoder

A robust prototype demonstrating how to share "single source of truth" C headers between a low-level C producer and a high-level Python decoder. This project uses **CFFI** and the **GCC preprocessor** to dynamically parse C structures, handling complex memory layouts, bit-fields, and nested data.

## 🚀 Features

* **Header-Driven Decoding**: The Python decoder reads `.h` files directly—no need to maintain duplicate structure definitions in Python.
* **Complex Data Types**: Supports nested structures, enumerations (enums), and bit-fields.
* **Memory Alignment**: Handles C structure packing (`#pragma pack(1)`) to ensure byte-perfect synchronization between languages.
* **JSON Export**: Automatically converts decoded binary messages into structured JSON format via recursive introspection.
* **Multi-Header Support**: Uses the system's C preprocessor to resolve `#include` dependencies across multiple files.

## 📂 Project Structure

```text
.
├── generate_bin.c        # C producer: Creates the binary sample
├── Makefile              # Build system for the C project
├── decode.py             # Python consumer: Decodes binary to JSON
├── generate_bin/         # Directory for generated artifacts
│   └── headers/          # C Header files (The "Source of Truth")
│       ├── protocol.h    # Main entry point
│       ├── enums.h       # Status and Mode definitions
│       ├── formats.h     # Bit-fields and Nested structures
│       └── vals.h        # Constants and Macros
└── message_data.bin      # The generated binary (output of C)
```

## 🛠 Prerequisites

* **C Compiler**: `gcc` (used for both compilation and header pre-processing).
* **Python 3.10+**
* **CFFI Library**: 
    ```bash
    pip install cffi
    ```

## 🚦 How to Use

### 1. Generate the Binary Data
Compile and run the C producer using the provided Makefile:
```bash
make all
```
This will create the `generate_bin` executable and produce a `message_data.bin` file containing a serialized `MainMessage` structure.

### 2. Decode in Python
Run the decoder script:
```bash
python decode.py
```
The script will:
1. Invoke `gcc -E` to flatten the C headers.
2. Map the `message_data.bin` file onto the C structure.
3. Print the decoded fields to the console.
4. Generate a `message.json` file.

## 🧠 Technical Highlights

### Handling Memory Padding
One of the core challenges in binary interfacing is **Memory Alignment**. Compilers often add "padding" bytes to optimize CPU access. This project forces a 1-byte alignment using:
* **C**: `#pragma pack(push, 1)`
* **Python (CFFI)**: `ffi.cdef(..., pack=1)`

This ensures that a `uint8_t` followed by a `uint32_t` takes exactly 5 bytes in both environments, preventing "shifts" that would otherwise corrupt the data.

### Bit-field Introspection
The project demonstrates how to handle C bit-fields (e.g., `uint8_t active : 1;`). CFFI treats these transparently as standard Python integers, allowing for easy manipulation of flag-based protocols.

## 📝 License
MIT
