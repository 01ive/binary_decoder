import os
import json
import re
import subprocess
from cffi import FFI

def struct_to_dict(ffi, obj):
    """ Convertit récursivement une structure CFFI en dictionnaire Python. """
    if isinstance(obj, (int, float, str, bool)):
        return obj

    try:
        t = ffi.typeof(obj)
    except TypeError:
        return obj 

    if t.kind == 'pointer':
        t = t.item
        obj = obj[0]

    if t.kind in ('struct', 'union'):
        res = {}
        for field, _ in t.fields:
            val = getattr(obj, field)
            res[field] = struct_to_dict(ffi, val)
        return res

    elif t.kind == 'array' and t.item.cname == 'char':
        try:
            return ffi.string(obj).decode('utf-8', errors='replace')
        except:
            return str(obj)

    elif t.kind == 'array':
        return [struct_to_dict(ffi, obj[i]) for i in range(t.length)]

    return obj

def get_ffi_with_preprocess(main_header_path):
    ffi = FFI()
    
    # On récupère le dossier du header pour que GCC trouve les fichiers inclus
    include_dir = os.path.dirname(main_header_path)
    
    # Commande GCC : 
    # -x c : force le langage C
    # -I : définit le chemin de recherche des headers
    cmd = ["gcc", "-x", "c", "-E", "-P", f"-I{include_dir}", main_header_path]
    
    try:
        # On ne capture QUE stdout pour éviter que les warnings ne polluent le code C
        content = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, encoding='utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Erreur GCC lors du pré-processing")
        raise

    # On prépare la déclaration finale
    # On retire les #pragma restants car CFFI va râler (UserWarning)
    content = re.sub(r'#pragma.*', '', content)

    declaration = """
        typedef unsigned char uint8_t;
        typedef unsigned short uint16_t;
        typedef unsigned int uint32_t;
        typedef long long int64_t;
    """ + content
    
    # pack=1 est indispensable ici pour correspondre au #pragma pack(1) du C
    ffi.cdef(declaration, pack=1)
    return ffi

def export_to_json(msg, ffi):
    data_dict = struct_to_dict(ffi, msg)
    json_output = json.dumps(data_dict, indent=4)
    with open("message.json", "w") as f:
        f.write(json_output)
    print("\n--- Message exporté dans message.json ---")

def run_decoder():
    # Chemin vers ton header principal
    header_path = "bin_tools/headers/protocol.h"
    bin_path = "bin_tools/message_data.bin"

    ffi = get_ffi_with_preprocess(header_path)
    
    if not os.path.exists(bin_path):
        print(f"Erreur : {bin_path} introuvable. Lance 'make all' d'abord.")
        return

    with open(bin_path, "rb") as f:
        blob = f.read()

    msg = ffi.cast("MainMessage *", ffi.from_buffer(blob))

    print(f"Taille du message détectée : {ffi.sizeof(msg[0])} octets")
    
    print("\n--- Analyse des Champs de Bits (data_3) ---")
    print(f"Active  : {msg.data_3.active}")
    print(f"Version : {msg.data_3.version}")
    print(f"Command : {msg.data_3.command}")
    
    print("\n--- Données Principales ---")
    print(f"ID (data_1)     : {hex(msg.data_1)}")
    print(f"Statut (data_2) : {msg.data_2}")
    print(f"Texte (data_6)  : {ffi.string(msg.data_6).decode('utf-8')}")
    print(f"Valeur (data_7) : {hex(msg.data_7)}")

    export_to_json(msg, ffi)

if __name__ == "__main__":
    run_decoder()