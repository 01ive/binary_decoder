// protocol.h
#pragma pack(push, 1)

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
    SubStructure data_8;
    NestedStructure data_9;
    char data_10[16];
    int64_t data_11;
} MainMessage;

#pragma pack(pop)