# C-to-Python Binary Protocol Decoder

A robust prototype demonstrating how to share "single source of truth" C headers between a low-level C producer and a high-level Python decoder. This project uses **CFFI** and the **GCC preprocessor** to dynamically parse C structures, handling complex memory layouts, bit-fields, and nested data.

## 🚀 Features

* **Header-Driven Decoding**: The Python decoder reads `.h` files directly—no need to maintain duplicate structure definitions in Python.
* **Complex Data Types**: Supports nested structures, enumerations (enums), and bit-fields.
* **Memory Alignment**: Handles C structure packing (`#pragma pack(1)`) to ensure byte-perfect synchronization between languages.
* **JSON Export**: Automatically converts decoded binary messages into structured JSON format via recursive introspection.
* **Multi-Header Support**: Uses the system's C preprocessor to resolve `#include` dependencies across multiple files.
* **PCAPNG Decoding**: Reads and decodes binary payloads from PCAPNG capture files, filtering for UDP packets.
* **Binary Sending**: Includes tools to send generated binary data over UDP for testing and simulation.

## 📂 Project Structure

```text
.
├── bin_tools/
│   ├── generate_bin.c        # C producer: Creates the binary sample
│   ├── send_bin.c            # C sender: Sends binary data over UDP
│   ├── Makefile              # Build system for the C tools
│   ├── generate_bin          # Compiled executable (generated)
│   ├── send_bin              # Compiled executable (generated)
│   └── message_data.bin      # The generated binary (output of generate_bin)
├── headers/
│   ├── protocol.h            # Main entry point
│   ├── enums.h               # Status and Mode definitions
│   ├── formats.h             # Bit-fields and Nested structures
│   └── vals.h                # Constants and Macros
├── decode.py                 # Python consumer: Decodes binary to JSON and from PCAPNG
├── capture.pcapng            # Sample PCAPNG capture file
├── message.json              # Decoded JSON output
├── requirements.txt          # Python dependencies
├── LICENSE
└── README.md
```

## 🛠 Prerequisites

* **C Compiler**: `gcc` (used for both compilation and header pre-processing).
* **Python 3.10+**
* **Dependencies**: 
    ```bash
    pip install -r requirements.txt
    ```
    This installs CFFI, pycparser, and scapy for PCAPNG handling.

## 🚦 How to Use

### 1. Build the C Tools
Navigate to the bin_tools directory and compile the binaries:
```bash
cd bin_tools
make all
```
This will create the `generate_bin` and `send_bin` executables and generate `message_data.bin`.

### 2. Decode the Binary Data in Python
Run the decoder script from the project root:
```bash
python decode.py
```
The script will:
1. Preprocess the C headers using GCC.
2. Decode the `bin_tools/message_data.bin` file.
3. Print the decoded fields to the console.
4. Generate a `message.json` file.
5. Read and decode UDP payloads from `capture.pcapng`.

### 3. Send Binary Data (Optional)
To send the generated binary over UDP for testing:
```bash
cd bin_tools
make send
```
This sends `message_data.bin` to localhost:8080.

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
