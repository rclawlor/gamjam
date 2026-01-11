// Standard library
#include <stdint.h>

// Local imports
#include "draw.h"
#include "colour.h"
#include "constants.h"
#include "utils.h"
#include "window.h"


// Module variables
uint32_t m_Pixels[SCREEN_PX] = {};


/**
 * Fill pixel array with colour
 *
 * @param argb      32-bit ARGB colour
**/
void DRAW_fill_screen(uint32_t argb)
{
    int i;
    for (i = 0; i < RENDER_WIDTH * RENDER_HEIGHT; i++)
    {
        m_Pixels[i] = argb;
    }
}


/**
 * Draw 8x8 tile at specified coordinates
 *
 * @param tile      tile to be rendered
 * @param x         x coordinate to render tile
 * @param y         y coordinate to render tile
 * @param palette   palette to colour tile with
**/
void DRAW_tile(
    uint8_t tile[],
    uint32_t x,
    uint32_t y,
    uint32_t palette[]
)
{
    int idx = 0;
    int i, j = 0;
    for (j = 0; j < TILE_WIDTH; j++)
    {
        for (i = 0; i < TILE_WIDTH / 2; i++)
        {
            idx = (x + 2 * i) + RENDER_WIDTH * (y + j);
            uint8_t a = (tile[i + (TILE_WIDTH * j) / 2] & 0b01110000) >> 4;
            uint8_t b = tile[i + (TILE_WIDTH * j) / 2] & 0b00000111;
            if (a != 0)
            {
                m_Pixels[idx] = palette[a];
            }
            if (b != 0)
            {
                m_Pixels[idx + 1] = palette[b];
            }
        }
    }
}


/**
 * Draw map of tiles
 *
 * @param map           map to draw
 * @param spritesheet   spritesheet to use for map
 * @param palette       palettes to use for map
**/
void DRAW_map(
    uint8_t map[2][SCREEN_TILES],
    uint8_t spritesheet[][TILE_SIZE],
    uint32_t palette[][PAL_LENGTH]
)
{
    int i;
    int j;
    for (j = 0; j < TILES_Y; j++)
    {
        for (i = 0; i < TILES_X; i++)
        {
            DRAW_tile(
                spritesheet[map[0][i + j * TILES_X]],
                TILE_WIDTH * i,
                TILE_WIDTH * j,
                palette[map[1][i + j * TILES_X]]
            );
        }
    }
}


/**
 * Draw line between (xs, ys) and (xe, ye) on pixel grid
 *
 * @param xs            start x coordinate
 * @param ys            start y coordinate
 * @param xe            end x coordinate
 * @param ye            end y coordinate
**/
void DRAW_line(int xs, int ys, int xe, int ye) {
    int xs_s = xs + RENDER_WIDTH / 2;
    int ys_s = RENDER_HEIGHT / 2 - ys;
    int xe_s = xe + RENDER_WIDTH / 2;
    int ye_s = RENDER_HEIGHT / 2 - ye;


    int dx = abs(xe_s - xs_s);
    int sx = xs_s < xe_s ? 1 : -1;
    int dy = -abs(ye_s - ys_s);
    int sy = ys_s < ye_s ? 1 : -1;
    int err = dx + dy;
    int e2 = 0;

    while (1)
    {
        if (xs_s >= 0 && ys_s >= 0)
        {
            m_Pixels[xs_s + RENDER_WIDTH * ys_s] = ARGB(0xff, 0x00, 0xff, 0x00);
        }
        if (xs_s == xe_s && ys_s == ye_s)
        {
            break;
        }

        e2 = 2 * err;
        if (e2 >= dy)
        {
            err += dy; xs_s += sx;
        }
        if (e2 <= dx)
        {
            err += dx; ys_s += sy;
        }
    }
}


/**
 * Apply blur to pixel array
**/
void DRAW_apply_blur()
{
    int i, j;
    for (j = 0; j < RENDER_HEIGHT; j++)
    {
        for (i = 0; i < RENDER_WIDTH; i++)
        {
            m_Pixels[i + RENDER_WIDTH * j] = COLOUR_argb_gaussian_5(
                m_Pixels[max(i - 2, 0) + RENDER_WIDTH * j],
                m_Pixels[max(i - 1, 0) + RENDER_WIDTH * j],
                m_Pixels[i + RENDER_WIDTH * j],
                m_Pixels[min(i + 1, RENDER_WIDTH - 1) + RENDER_WIDTH * j],
                m_Pixels[min(i + 2, RENDER_WIDTH - 1) + RENDER_WIDTH * j]
            );
        }
    }

    for (i = 0; i < RENDER_WIDTH; i++)
    {
        for (j = 0; j < RENDER_HEIGHT; j++)
        {
            m_Pixels[i + RENDER_WIDTH * j] = COLOUR_argb_gaussian_5(
                m_Pixels[i + RENDER_WIDTH * max(j - 2, 0)],
                m_Pixels[i + RENDER_WIDTH * max(j - 1, 0)],
                m_Pixels[i + RENDER_WIDTH * j],
                m_Pixels[i + RENDER_WIDTH * min(j + 1, RENDER_HEIGHT - 1)],
                m_Pixels[i + RENDER_WIDTH * min(j + 2, RENDER_HEIGHT - 1)]
            );
        }
    }
}


/**
 * Desaturate pixel array
 *
 * @param scale         saturation scale factor
**/
void DRAW_desaturate(float scale)
{
    int i, j;
    for (j = 0; j < RENDER_HEIGHT; j++)
    {
        for (i = 0; i < RENDER_WIDTH; i++)
        {
            m_Pixels[i + RENDER_WIDTH * j] = COLOUR_desaturate(m_Pixels[i + RENDER_WIDTH * j], scale);
        }
    }
}


/**
* Return screen pixel array
**/
uint32_t* DRAW_get_pixels()
{
    return m_Pixels;
}
