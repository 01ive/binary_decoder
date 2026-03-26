import os
import json
from cffi import FFI

def struct_to_dict(ffi, obj):
    # Si c'est déjà un type Python de base (int, float, etc.), on le renvoie
    if isinstance(obj, (int, float, str, bool)):
        return obj

    try:
        t = ffi.typeof(obj)
    except TypeError:
        return obj # Déjà converti ou type inconnu

    if t.kind == 'pointer':
        t = t.item
        obj = obj[0]

    if t.kind in ('struct', 'union'):
        res = {}
        for field, field_info in t.fields:
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

# --- Exemple d'utilisation dans votre script ---

def export_to_json(msg, ffi):
    # Conversion en dictionnaire
    data_dict = struct_to_dict(ffi, msg)
    
    # Génération du JSON (indenté pour la lisibilité)
    json_output = json.dumps(data_dict, indent=4)
    
    print("--- Message au format JSON ---")
    print(json_output)
    
    # Sauvegarde dans un fichier
    with open("message.json", "w") as f:
        f.write(json_output)

import re

def get_ffi_from_header(header_path):
    ffi = FFI()
    with open(header_path, "r") as f:
        content = f.read()

    # 1. Nettoyage agressif des directives préprocesseur (#include, #pragma, #define)
    # On enlève tout ce qui commence par '#'
    content = re.sub(r'#.*', '', content)
    
    # 2. Nettoyage des caractères invisibles (espaces insécables)
    content = content.replace('\xa0', ' ')
    
    # 3. On enlève les résidus d'attributs PACKED si présents
    content = content.replace('PACKED', '')
    content = content.replace('__attribute__((packed))', '')

    # 4. Déclarations de base
    declaration = """
        typedef unsigned char uint8_t;
        typedef unsigned short uint16_t;
        typedef unsigned int uint32_t;
        typedef long long int64_t;
    """ + content
    
    # 5. Utilisation de l'argument pack=1 (équivalent de #pragma pack(1))
    # C'est ici qu'on force CFFI à coller les données sans padding
    ffi.cdef(declaration, pack=1)
    return ffi

def debug_offsets(ffi):
    print(f"{'Champ':<15} | {'Offset Python':<15}")
    print("-" * 35)
    for field in ["data_6", "data_7", "data_8", "data_9", "data_10", "data_11", "data_12"]:
        off = ffi.offsetof("MainMessage", field)
        print(f"{field:<15} | {off:<15}")

# Appelez debug_offsets(ffi) dans votre run_decoder

def run_decoder():
    ffi = get_ffi_from_header("generate_bin/protocol.h")
    
    with open("generate_bin/message_data.bin", "rb") as f:
        blob = f.read()

    msg = ffi.cast("MainMessage *", ffi.from_buffer(blob))

    print(f"Taille du message : {ffi.sizeof(msg[0])} octets")

    print("--- Analyse des Champs de Bits ---")
    # L'accès est totalement transparent
    print(f"Active  : {msg.data_8.active}")
    print(f"Version : {msg.data_8.version}")
    print(f"Command : {msg.data_8.command}")
    
    print("\n--- Reste du message ---")
    print(f"ID (data_6) : {hex(msg.data_6)}")
    print(f"Texte       : {ffi.string(msg.data_11).decode()}")

    debug_offsets(ffi)

    export_to_json(msg, ffi)

if __name__ == "__main__":
    run_decoder()