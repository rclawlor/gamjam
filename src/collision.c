// Standard library
#include <math.h>

// Local
#include "collision.h"
#include "constants.h"
#include "draw.h"
#include "entity.h"
#include "vector.h"


/**
 * Find collision map for given tile
 *
 * @param tile      tile to extract collision map from
 * @param map       2D array to store collision map in
**/
void COLLISION_get_map(uint8_t tile[], uint8_t map[TILE_WIDTH][TILE_WIDTH])
{
    int i, j;
    for (j = 0; j < TILE_WIDTH; j++)
    {
        for (i = 0; i < TILE_WIDTH / 2; i++)
        {
            uint8_t a = (tile[i + (TILE_WIDTH * j) / 2] & 0b10000000) >> 7;
            uint8_t b = (tile[i + (TILE_WIDTH * j) / 2] & 0b00001000) >> 3;

            map[j][2 * i] = a;
            map[j][2 * i + 1] = b;
        }
    }
}


/**
 * Find tile index corresponding to pixel (x, y) coordinates
 *
 * @param x         x pixel coordinate
 * @param y         y pixel coordinate
**/
Coordinate_t COLLISION_find_tile(float x, float y)
{
    uint32_t x_tile = (uint32_t)((x / 8) + ((float)TILES_X / 2.0));
    uint32_t y_tile = floorf(((float)TILES_Y / 2.0) - (y / 8));

    Coordinate_t c = { .x = x_tile, .y = y_tile };
    return c;
}


/**
 * Find offset into tile coordinate
 *
 * @param x         x pixel coordinate
 * @param y         y pixel coordinate
 * @param c         tile coordinate
**/
Coordinate_t COLLISION_find_offset(float x, float y, Coordinate_t *c)
{
    uint32_t dx = (uint32_t)roundf(x - TILE_WIDTH * c->x) + (TILE_WIDTH * TILES_X / 2);
    uint32_t dy = ((float)TILE_WIDTH * (float)TILES_Y / 2.0) - (uint32_t)roundf(y + TILE_WIDTH * c->y);
    Coordinate_t offset = { .x = dx, .y = dy };
    return offset;
}


/**
 * Check collision between sprite and surrounding tiles
 *
 * @param sprite        sprite to check collision for
 * @param map           current map
 * @param spritesheet   sprites used in map
 * @param x             x pixel coordinate of sprite
 * @param y             y pixel coordinate of sprite
**/
Vector2D_t COLLISION_check_map(
    EntityGeneric_t *entity,
    uint8_t map[2][SCREEN_TILES],
    uint8_t spritesheet[][TILE_SIZE]
)
{
    Coordinate_t c;
    Coordinate_t offset;
    double x = floorf(entity->pos.x);
    double y = ceilf(entity->pos.y);

    uint8_t collision_map[TILE_WIDTH][TILE_WIDTH] = { 0 };
    c = COLLISION_find_tile(x, y);
    offset = COLLISION_find_offset(x, y, &c);

    // Stores collision maps: {TL, TR, BL, BR}
    uint8_t collision_maps[4][TILE_WIDTH][TILE_WIDTH];
    int ud, lr;
    for (ud = 0; ud < 2; ud++)
    {
        for (lr = 0; lr < 2; lr++)
        {
            c = COLLISION_find_tile(x + lr * TILE_WIDTH, y - ud * TILE_WIDTH);
            COLLISION_get_map(spritesheet[map[0][c.x + c.y * TILES_X]], collision_maps[2 * ud + lr]);
        }
    }

    // Calculate overlap and corresponding direction vector
    int i, j, collide;
    uint8_t sprite_collision[TILE_WIDTH][TILE_WIDTH];
    Vector2D_t direction = { 0 };
    COLLISION_get_map(entity->sprite, sprite_collision);
    uint8_t force;
    for (j = 0; j < TILE_WIDTH; j++)
    {
        for (i = 0; i < TILE_WIDTH; i++)
        {
            ud = offset.y + j >= TILE_WIDTH ? 1 : 0;
            lr = offset.x + i >= TILE_WIDTH ? 1 : 0;
            collide = (
                collision_maps[2 * ud + lr][i + offset.x - TILE_WIDTH * lr][j + offset.y - TILE_WIDTH * ud]
                && sprite_collision[j][i]
            );
            if (collide)
            {
                direction.x += 1 - 2 * (float)(i < TILE_WIDTH / 2);
                direction.y += 1 - 2 * (float)(j < TILE_WIDTH / 2);
                force += 1;
            }
        }
    }

    VECTOR_normalise(&direction);
    direction.x *= force;
    direction.y *= force;

    return direction;
}



/**
 * Resolve collision for an entity by adjusting (x, y)
**/
void COLLISION_resolve_map(
    EntityGeneric_t *entity,
    uint8_t map[2][SCREEN_TILES],
    uint8_t spritesheet[][TILE_SIZE]
)
{
    Vector2D_t direction;
    direction = COLLISION_check_map(entity, map, spritesheet);

    while (direction.y != 0 || direction.x != 0)
    {
        if (fabs(direction.y) > fabs(direction.x))
        {
            entity->pos.y += direction.y > 0 ? 1 : -1;
            entity->vel.y = 0;
        }
        else
        {
            entity->pos.x += direction.x > 0 ? -1 : 1;
            entity->vel.x = 0;
        }
        direction = COLLISION_check_map(entity, map, spritesheet);
    }
}


Vector2D_t COLLISION_check_entity(
    EntityGeneric_t *entity_a,
    EntityGeneric_t *entity_b
)
{
    Vector2D_t direction = { 0 };
    Coordinate_t offset = {
        .x = entity_b->pos.x - entity_a->pos.x,
        .y = entity_b->pos.y - entity_a->pos.y
    };
    printf("(%d, %d)\n", offset.x, offset.y);

    if (abs(offset.x) >= TILE_WIDTH || abs(offset.y) >= TILE_WIDTH)
    {
        return direction;
    }

    uint8_t collision_map_a[TILE_WIDTH][TILE_WIDTH] = { 0 };
    uint8_t collision_map_b[TILE_WIDTH][TILE_WIDTH] = { 0 };

    COLLISION_get_map(entity_a->sprite, collision_map_a);
    COLLISION_get_map(entity_b->sprite, collision_map_b);

    // Calculate overlap and corresponding direction vector
    int i, j, collide, imin, jmin, imax, jmax;
    uint8_t sprite_collision[TILE_WIDTH][TILE_WIDTH];
    uint8_t force;
    
    if (offset.x < 0)
    {
        imin = 0;
        imax = TILE_WIDTH + offset.x;
    }
    else
    {
        imin = offset.x;
        imax = TILE_WIDTH;
    }

    if (offset.y < 0)
    {
        jmin = 0;
        jmax = TILE_WIDTH + offset.y;
    }
    else
    {
        jmin = offset.y;
        jmax = TILE_WIDTH;
    }

    for (j = jmin; j < jmax; j++)
    {
        for (i = imin; i < imax; i++)
        {
            collide = (
                collision_map_a[j + offset.y][i + offset.x]
                && collision_map_b[j][i]
            );
            if (collide)
            {
                direction.x += 1 - 2 * (float)(i < TILE_WIDTH / 2);
                direction.y += 1 - 2 * (float)(j < TILE_WIDTH / 2);
                force += 1;
            }
        }
    }

    VECTOR_normalise(&direction);
    direction.x *= force;
    direction.y *= force;

    return direction;
}


/**
 * Resolve collision for an entity by adjusting (x, y)
**/
void COLLISION_resolve_entity(
    EntityGeneric_t *entity_a,
    EntityGeneric_t *entity_b
)
{
    Vector2D_t direction;
    direction = COLLISION_check_entity(entity_a, entity_b);
    DRAW_line(
        entity_a->pos.x,
        entity_a->pos.y,
        entity_a->pos.x + direction.x,
        entity_a->pos.y + direction.y
    );
}
