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
    uint16_t data_41;
    float data_42;
} SubStructure;

typedef struct {
    uint8_t data_51;
    EnumMode data_52;
    double data_53;
} NestedStructure;

typedef struct {
    uint32_t data_1;
    EnumStatus data_2;
    ControlBits data_3;       // Nouveau champ : 1 octet de bits
    SubStructure data_4;
    NestedStructure data_5;
    char data_6[16];
    int64_t data_7;
} MainMessage;

#pragma pack(pop)