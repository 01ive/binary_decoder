// protocol.h
#include <stdint.h>

#pragma pack(push, 1)

// Structure de bit-fields (tient sur 1 octet au total)
typedef struct {
    uint8_t active  : 1;  // 1 bit : 0 ou 1
    uint8_t version : 3;  // 3 bits : valeur de 0 à 7
    uint8_t command : 4;  // 4 bits : valeur de 0 à 15
} ControlBits;

typedef enum {
    STATUS_IDLE = 0,
    STATUS_ACTIVE = 1,
    STATUS_ERROR = 255
} EnumStatus;

typedef enum {
    MODE_FAST = 10,
    MODE_SLOW = 20
} EnumMode;

typedef struct {
    uint16_t data_1;
    float data_2;
} SubStructure;

typedef struct {
    uint8_t data_3;
    EnumMode data_4;
    double data_5;
} NestedStructure;

typedef struct {
    uint32_t data_6;
    EnumStatus data_7;
    ControlBits data_8;       // Nouveau champ : 1 octet de bits
    SubStructure data_9;
    NestedStructure data_10;
    char data_11[16];
    int64_t data_12;
} MainMessage;

#pragma pack(pop)