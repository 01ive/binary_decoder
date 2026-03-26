#pragma pack(push, 1)

// protocol.h
#include "enums.h"
#include "formats.h"
#include "vals.h"



typedef struct {
    uint32_t data_1;
    EnumStatus data_2;
    ControlBits data_3;       // Nouveau champ : 1 octet de bits
    SubStructure data_4;
    NestedStructure data_5;
    char data_6[C_STRING_SIZE];
    int64_t data_7;
} MainMessage;

#pragma pack(pop)