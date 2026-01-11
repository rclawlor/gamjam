#ifndef TEXT_H_
#define TEXT_H_

// Standard library
#include <stdint.h>

// Local
#include "constants.h"


typedef enum {
    ALIGN_LEFT = 0,
    ALIGN_RIGHT,
    ALIGN_CENTRE,
    NUM_TEXT_ALIGNMENT
} TextAlignment_e;

typedef struct {
    char left;
    char right;
    int offset;
} KerningPair_t;

extern KerningPair_t font_kerning[];


void TEXT_render(uint32_t, uint32_t, TextAlignment_e, char*, uint8_t[][TILE_SIZE], uint32_t[]);
void TEXT_kern(char*, int*);
int TEXT_lookup_kerning_offset(char, char);


#endif // TEXT_H_
