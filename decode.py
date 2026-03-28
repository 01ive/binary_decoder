import os
import json
import re
import subprocess
import logging

from cffi import FFI
import scapy.all as scapy

class DecoderH(FFI):
    def __init__(self, main_header_path):
        """ Initialize the CFFI instance and preprocess the header file to handle includes and macros. """
        super().__init__()
        self._get_ffi_with_preprocess(main_header_path)

    def _get_ffi_with_preprocess(self, main_header_path):  
        """ Preprocess the header file using GCC to resolve includes and macros, then pass the result to CFFI. """
        include_dir = os.path.dirname(main_header_path)
        
        # GCC command to preprocess the header file: 
        # -x c : force C language
        # -E : stop after preprocessing
        # -P : suppress line markers in output
        # -I : add include directory for header resolution
        cmd = ["gcc", "-x", "c", "-E", "-P", f"-I{include_dir}", main_header_path]
        
        try:
            # Capture the preprocessed output, ignoring any warnings or errors from GCC
            content = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            logging.error(f"GCC preprocessing failed: {e}")
            raise

        # Remove any remaining #pragma directives that might not be handled by CFFI
        content = re.sub(r'#pragma.*', '', content)

        # Add basic type definitions to ensure CFFI can parse the header correctly, especially for fixed-width integer types
        declaration = """
            typedef unsigned char uint8_t;
            typedef unsigned short uint16_t;
            typedef unsigned int uint32_t;
            typedef long long int64_t;
        """ + content
        
        # pack=1 is crucial to ensure that the CFFI structures match the exact layout of the binary data, without any padding added by the compiler
        self.cdef(declaration, pack=1)

    def _struct_to_dict(self, obj):
        """ Convert a CFFI structure to a Python dictionary. """
        if isinstance(obj, (int, float, str, bool)):
            return obj

        try:
            t = self.typeof(obj)
        except TypeError:
            return obj 

        if t.kind == 'pointer':
            t = t.item
            obj = obj[0]

        if t.kind in ('struct', 'union'):
            res = {}
            for field, _ in t.fields:
                val = getattr(obj, field)
                res[field] = self._struct_to_dict(val)
            return res

        elif t.kind == 'array' and t.item.cname == 'char':
            try:
                return self.string(obj).decode('utf-8', errors='replace')
            except:
                return str(obj)

        elif t.kind == 'array':
            return [self._struct_to_dict(obj[i]) for i in range(t.length)]

        return obj
    
    def export_to_json(self, msg):
        """ Export the decoded message to a JSON file for easier analysis and visualization. """
        data_dict = self._struct_to_dict(msg)
        json_output = json.dumps(data_dict, indent=4)
        with open("message.json", "w") as f:
            f.write(json_output)
        logging.info("Message exported to message.json")

def print_decoded_data(ffi, msg):
    """ Print the decoded data in a human-readable format, including field values and bitfield analysis. """
    logging.info(f"Size of message detected: {ffi.sizeof(msg[0])} bytes")
    
    logging.info("--- Bits fields analysis (data_3) ---")
    logging.info(f"Active  : {msg.data_3.active}")
    logging.info(f"Version : {msg.data_3.version}")
    logging.info(f"Command : {msg.data_3.command}")
    
    logging.info("--- Main Data ---")
    logging.info(f"ID (data_1)     : {hex(msg.data_1)}")
    logging.info(f"Statut (data_2) : {msg.data_2}")
    logging.info(f"Texte (data_6)  : {ffi.string(msg.data_6).decode('utf-8')}")
    logging.info(f"Valeur (data_7) : {hex(msg.data_7)}")

def read_pcapng(ffi, file_path):
    """ Read a pcapng file, filter for UDP packets that do not contain DNS layers, and decode the payload using the provided CFFI instance. """
    packets = scapy.rdpcap(file_path)
    for pkt in packets:
        if pkt.haslayer(scapy.UDP) and not pkt.haslayer(scapy.DNS):
            logging.debug(f"Packet UDP : {pkt.summary()}")
            blob = pkt.load
            msg = ffi.cast("MainMessage *", ffi.from_buffer(blob))
            print_decoded_data(ffi, msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Path to files
    header_path = "bin_tools/headers/protocol.h"
    bin_path = "bin_tools/message_data.bin"
    pcap_path = "capture.pcapng"

    if not os.path.exists(bin_path):
        logging.error(f"Can't find {bin_path}.")
        exit(1)
    with open(bin_path, "rb") as f:
        blob = f.read()

    ffi = DecoderH(header_path)
    msg = ffi.cast("MainMessage *", ffi.from_buffer(blob))
    ffi.export_to_json(msg)

    # Print results
    print_decoded_data(ffi, msg)

    # Decod from pcapng file
    read_pcapng(ffi, pcap_path)