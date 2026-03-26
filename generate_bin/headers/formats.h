// Structure de bit-fields (tient sur 1 octet au total)
typedef struct {
    uint8_t active  : 1;  // 1 bit : 0 ou 1
    uint8_t version : 3;  // 3 bits : valeur de 0 à 7
    uint8_t command : 4;  // 4 bits : valeur de 0 à 15
} ControlBits;

typedef struct {
    uint16_t data_41;
    float data_42;
} SubStructure;

typedef struct {
    uint8_t data_51;
    EnumMode data_52;
    double data_53;
} NestedStructure;