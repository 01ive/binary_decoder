#include <stdio.h>
#include <string.h>
#include <stddef.h>
#include "protocol.h"

int main() {
    MainMessage msg;
    memset(&msg, 0, sizeof(MainMessage));

    msg.data_6 = 0xABCDE000;
    msg.data_7 = STATUS_ACTIVE;

    // Initialisation des champs de bits
    msg.data_8.active = 1;      // True
    msg.data_8.version = 5;     // 101 en binaire
    msg.data_8.command = 12;    // 1100 en binaire

    msg.data_9.data_1 = 2024;
    msg.data_9.data_2 = 1.23f;
    
    // ... remplissage du reste identique au précédent ...
    strncpy(msg.data_11, "Bitfield Test", sizeof(msg.data_11));

    FILE *file = fopen("message_data.bin", "wb");
    fwrite(&msg, sizeof(MainMessage), 1, file);
    fclose(file);

    printf("Binaire généré (Taille : %zu octets)\n", sizeof(MainMessage));
    printf("%zu\n", sizeof(msg));

    printf("data_11 est à l'offset : %zu\n", offsetof(MainMessage, data_11));

    return 0;
}