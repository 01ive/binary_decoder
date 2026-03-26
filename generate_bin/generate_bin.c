#include <stdio.h>
#include <string.h>
#include <stddef.h>
#include "protocol.h"

int main() {
    MainMessage msg;
    memset(&msg, 0, sizeof(MainMessage));

    msg.data_1 = 0xABCDE000;
    msg.data_2 = STATUS_ACTIVE;

    // Initialisation des champs de bits
    msg.data_3.active = 1;      // True
    msg.data_3.version = 5;     // 101 en binaire
    msg.data_3.command = 12;    // 1100 en binaire

    msg.data_4.data_41 = 2024;
    msg.data_4.data_42 = 1.23f;

    msg.data_5.data_51 = 42;
    msg.data_5.data_52 = MODE_FAST;
    msg.data_5.data_53 = 3.14159;
    
    // ... remplissage du reste identique au précédent ...
    strncpy(msg.data_6, "Bitfield Test", sizeof(msg.data_6));

    msg.data_7 = 0x123456789ABCDEF0;

    FILE *file = fopen("message_data.bin", "wb");
    fwrite(&msg, sizeof(MainMessage), 1, file);
    fclose(file);

    printf("Binaire généré (Taille : %zu octets)\n", sizeof(MainMessage));
    printf("%zu\n", sizeof(msg));

    printf("data_3 est à l'offset : %zu\n", offsetof(MainMessage, data_3));

    return 0;
}