#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "protocol.h"

// On utilise l'attribut packed pour s'assurer que le compilateur ne rajoute pas
// d'octets invisibles (padding) entre les champs, facilitant le décodage futur.
#define PACKED __attribute__((packed))

int main() {
    // 1. Initialisation des données
    MainMessage msg;
    memset(&msg, 0, sizeof(MainMessage)); // Nettoyage de la mémoire

    msg.data_6 = 0xDEADBEEF;
    msg.data_7 = STATUS_ACTIVE;
    
    msg.data_8.data_1 = 1024;
    msg.data_8.data_2 = 3.14159f;

    msg.data_9.data_3 = 42;
    msg.data_9.data_4 = MODE_SLOW;
    msg.data_9.data_5 = 123.456789;

    strncpy(msg.data_10, "Hello Proto", sizeof(msg.data_10));
    msg.data_11 = -9223372036854775807LL; // Valeur min int64 environ

    // 2. Écriture dans un fichier binaire
    FILE *file = fopen("message_data.bin", "wb");
    if (file == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        return 1;
    }

    size_t written = fwrite(&msg, sizeof(MainMessage), 1, file);
    
    if (written == 1) {
        printf("Binaire genere avec succes !\n");
        printf("Taille totale du message : %zu octets\n", sizeof(MainMessage));
    }

    fclose(file);
    return 0;
}