#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define SERVER_IP "127.0.0.1"
#define BUFFER_SIZE 1024

int main() {
    int sockfd;
    struct sockaddr_in servaddr;
    FILE *file;
    char buffer[BUFFER_SIZE];
    size_t bytes_read;

    // 1. Création de la socket UDP
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Erreur de création de la socket");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));

    // Configuration de l'adresse de destination
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(PORT);
    servaddr.sin_addr.s_addr = inet_addr(SERVER_IP);

    // 2. Ouverture du fichier binaire
    file = fopen("message_data.bin", "rb");
    if (file == NULL) {
        perror("Erreur lors de l'ouverture du fichier");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Envoi du fichier vers %s:%d...\n", SERVER_IP, PORT);

    // 3. Lecture et envoi par paquets
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
        if (sendto(sockfd, buffer, bytes_read, 0, 
                   (const struct sockaddr *) &servaddr, sizeof(servaddr)) < 0) {
            perror("Erreur d'envoi");
            break;
        }
    }

    printf("Envoi terminé.\n");

    // Nettoyage
    fclose(file);
    close(sockfd);
    return 0;
}