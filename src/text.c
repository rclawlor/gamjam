// Standard library
#include <string.h>
#include <stdlib.h>

// Local
#include "constants.h"
#include "text.h"
#include "draw.h"
#include "utils.h"


const int MAX_KERNING_PAIRS = 256;


/**
 * Render text
 *
 * @param x         x coordinate of text
 * @param y         y coordinate of text
 * @param text      text to render
 * @param font      font to use (NOTE: must start at a for fast indexing)
 * @param palette   palette to colour font
**/
void TEXT_render(
    uint32_t x,
    uint32_t y,
    TextAlignment_e alignment,
    char *text,
    uint8_t font[][32],
    uint32_t palette[]
)
{
    int i;
    int idx;
    int offset = 0;
    unsigned long len = strlen(text);
    int *offsets = malloc(sizeof(int) * len);
    TEXT_kern(text, offsets);

    int pos_x;
    switch (alignment)
    {
        case ALIGN_LEFT:
            pos_x = x;
            break;
        case ALIGN_RIGHT:
            pos_x = x - (TILE_WIDTH * len + sum(offsets, len));
            break;
        case ALIGN_CENTRE:
        default:
            // Default to centre alignment
            pos_x = x - (TILE_WIDTH * len + sum(offsets, len)) / 2;
            break;
    }

    for (i = 0; i < len; i++)
    {
        // Find idx from '0' and add 1 as first tile is a space
        if (text[i] == ' ')
        {
            idx = 0;
        }
        else
        {
            idx = text[i] - (int)'0' + 1;
        }
        DRAW_tile(font[idx], pos_x + offset, y - TILE_WIDTH / 2, palette);
        offset += offsets[i] + TILE_WIDTH;
    }
    free(offsets);
}


/**
 * Calculate required offsets for text kerning
 *
 * @param text      text to calculate offsets for
 * @param offsets   array to store offsets in
**/
void TEXT_kern(char *text, int offsets[])
{
    int i;
    char left;
    char right;
    for (i = 0; i < strlen(text) - 1; i++)
    {
        left = text[i];
        right = text[i + 1];

        offsets[i] = TEXT_lookup_kerning_offset(left, right);
    }
    offsets[strlen(text) - 1] = 0;
}


/**
 * Find kerning offset for provided character pair
 *
 * @param left      left character
 * @param right     right character
**/
int TEXT_lookup_kerning_offset(char left, char right)
{
    int i;
    for (i = 0; i < MAX_KERNING_PAIRS; i++)
    {
        if (font_kerning[i].left == '\0')
        {
            return 0;
        }
        else if (font_kerning[i].left == left)
        {
            if (font_kerning[i].right == right)
            {
                return font_kerning[i].offset;
            }
        }
    }

    return 0;
}


/**
 * Kerning data for main game font
**/
KerningPair_t font_kerning[] = {
    // 0
    { .left = '0', .right = '1', .offset = -2 },
    { .left = '0', .right = '8', .offset = -2 },
    { .left = '0', .right = 'X', .offset = -2 },
    // 1
    { .left = '1', .right = '0', .offset = -1 },
    { .left = '1', .right = '2', .offset = -2 },
    { .left = '1', .right = '4', .offset = -2 },
    { .left = '1', .right = '6', .offset = -2 },
    { .left = '1', .right = '9', .offset = -2 },
    // 2
    { .left = '2', .right = '1', .offset = -1 },
    { .left = '2', .right = '3', .offset = -1 },
    { .left = '2', .right = '5', .offset = -1 },
    { .left = '2', .right = '8', .offset = -1 },
    // 3
    { .left = '3', .right = '4', .offset = -1 },
    { .left = '3', .right = '8', .offset = -2 },
    // 4
    { .left = '4', .right = '0', .offset = -1 },
    { .left = '4', .right = '4', .offset = -1 },
    { .left = '4', .right = '5', .offset = -2 },
    // 5
    { .left = '5', .right = '1', .offset = -2 },
    { .left = '5', .right = '2', .offset = -2 },
    { .left = '5', .right = '3', .offset = -2 },
    { .left = '5', .right = '5', .offset = -2 },
    { .left = '5', .right = '6', .offset = -2 },
    { .left = '5', .right = '7', .offset = -2 },
    { .left = '5', .right = '8', .offset = -2 },
    { .left = '5', .right = '9', .offset = -2 },
    // 6
    { .left = '6', .right = '1', .offset = -1 },
    { .left = '6', .right = '2', .offset = -1 },
    { .left = '6', .right = '3', .offset = -1 },
    { .left = '6', .right = '5', .offset = -1 },
    { .left = '6', .right = '6', .offset = -1 },
    { .left = '6', .right = '7', .offset = -1 },
    { .left = '6', .right = '8', .offset = -1 },
    { .left = '6', .right = '9', .offset = -1 },
    // 7
    { .left = '7', .right = '2', .offset = -2 },
    { .left = '7', .right = '8', .offset = -2 },
    // 8
    { .left = '8', .right = '0', .offset = -1 },
    { .left = '8', .right = '4', .offset = -1 },
    { .left = '8', .right = '9', .offset = -2 },
    // 9
    { .left = '9', .right = '2', .offset = -2 },
    // A
    // B
    // C
    // D
    // E
    { .left = 'E', .right = 'L', .offset = -3 },
    { .left = 'E', .right = 'S', .offset = -3 },
    { .left = 'E', .right = 'T', .offset = -3 },
    { .left = 'E', .right = 'V', .offset = -2 },
    // F
    // G
    { .left = 'G', .right = 'S', .offset = -2 },
    // H
    // I
    { .left = 'I', .right = 'N', .offset = -4 },
    { .left = 'I', .right = 'O', .offset = -3 },
    { .left = 'I', .right = 'T', .offset = -4 },
    // J
    // K
    // L
    { .left = 'L', .right = 'E', .offset = -3 },
    { .left = 'L', .right = 'U', .offset = -4 },
    // M
    // N
    { .left = 'N', .right = 'G', .offset = -1 },
    // O
    { .left = 'O', .right = 'L', .offset = -4 },
    { .left = 'O', .right = 'N', .offset = -3 },
    // P
    { .left = 'P', .right = 'L', .offset = -3 },
    // Q
    { .left = 'Q', .right = 'U', .offset = -3 },
    // R
    { .left = 'R', .right = 'E', .offset = -2 },
    { .left = 'R', .right = 'N', .offset = -3 },
    // S
    { .left = 'S', .right = 'E', .offset = -2 },
    { .left = 'S', .right = 'O', .offset = -2 },
    { .left = 'S', .right = 'U', .offset = -3 },
    // T
    { .left = 'T', .right = 'E', .offset = -2 },
    { .left = 'T', .right = 'I', .offset = -4 },
    { .left = 'T', .right = 'T', .offset = -3 },
    { .left = 'T', .right = 'U', .offset = -3 },
    // U
    { .left = 'U', .right = 'I', .offset = -4 },
    { .left = 'U', .right = 'M', .offset = -1 },
    { .left = 'U', .right = 'R', .offset = -3 },
    { .left = 'U', .right = 'T', .offset = -3 },
    // V
    { .left = 'V', .right = 'E', .offset = -2 },
    // W
    // X
    { .left = 'X', .right = '1', .offset = -1 },
    { .left = 'X', .right = '7', .offset = -2 },
    // Y
    // Z
    // End of array
    { .left = '\0', .right = '\0', .offset = 0 },
};
