#ifndef DRAW_H_
#define DRAW_H_

// Standard library
#include <stdint.h>
#include <stdbool.h>

// Local
#include "constants.h"


void DRAW_fill_screen(uint32_t);
void DRAW_tile(uint8_t[], uint32_t, uint32_t, uint32_t[]);
void DRAW_map(uint8_t[2][SCREEN_TILES], uint8_t[][TILE_SIZE], uint32_t[][PAL_LENGTH]);
void DRAW_line(int, int, int, int);
void DRAW_apply_blur();
void DRAW_desaturate(float);
uint32_t* DRAW_get_pixels();


#endif // DRAW_H_
