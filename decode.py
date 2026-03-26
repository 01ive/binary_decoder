import os
from cffi import FFI

def get_ffi_from_header(header_path):
    ffi = FFI()
    
    if not os.path.exists(header_path):
        raise FileNotFoundError(f"Impossible de trouver {header_path}")

    with open(header_path, "r") as f:
        header_content = f.read()
        
        # Astuce : CFFI a besoin des types standard comme uint32_t.
        # Soit on les ajoute à la main, soit on s'assure qu'ils sont définis.
        # Ici on ajoute les types de base au début de la string pour aider le parser.
        header_clean = """
            typedef unsigned char uint8_t;
            typedef unsigned short uint16_t;
            typedef unsigned int uint32_t;
            typedef long long int64_t;
        """ + header_content
        
        ffi.cdef(header_clean)
    return ffi

def decode_binary(bin_file, header_file):
    ffi = get_ffi_from_header(header_file)
    
    with open(bin_file, "rb") as f:
        data = f.read()

    # On mappe le binaire sur la structure MainMessage
    msg = ffi.cast("MainMessage *", ffi.from_buffer(data))

    print(f"--- Données lues depuis {header_file} ---")
    print(f"ID : {hex(msg.data_6)}")
    print(f"Chaîne : {ffi.string(msg.data_10).decode()}")
    print(f"Valeur imbriquée : {msg.data_9.data_5}")

if __name__ == "__main__":
    decode_binary("generate_bin/message_data.bin", "generate_bin/protocol.h")