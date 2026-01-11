#ifndef COLLISION_H_
#define COLLISION_H_

// Standard library
#include <stdint.h>
#include <stdbool.h>

// Local
#include "constants.h"
#include "entity.h"
#include "vector.h"


void COLLISION_get_map(uint8_t[TILE_WIDTH], uint8_t[TILE_WIDTH][TILE_WIDTH]);
Coordinate_t COLLISION_find_tile(float, float);
Coordinate_t COLLISION_find_offset(float, float, Coordinate_t*);
Vector2D_t COLLISION_check_map(EntityGeneric_t*, uint8_t[2][SCREEN_TILES], uint8_t[][TILE_SIZE]);
void COLLISION_resolve_map(EntityGeneric_t*, uint8_t[2][SCREEN_TILES], uint8_t[][TILE_SIZE]);
Vector2D_t COLLISION_check_entity(EntityGeneric_t*, EntityGeneric_t*);
void COLLISION_resolve_entity(EntityGeneric_t*, EntityGeneric_t*);


#endif // COLLISION_H_
