#ifndef COLOUR_H_
#define COLOUR_H_


// Standard library
#include <stdint.h>


#define ARGB(a, r, g, b) ((a << 24) | (r << 16) | (g << 8) | b)


typedef struct {
    uint8_t a;
    uint8_t r;
    uint8_t g;
    uint8_t b;
} ColourARGB_t;

typedef struct {
    uint8_t a;
    uint32_t h;
    float s;
    float v;
} ColourAHSV_t;


uint32_t COLOUR_argb_average_3(uint32_t argb_a, uint32_t argb_b, uint32_t argb_c);
uint32_t COLOUR_argb_gaussian_5(uint32_t, uint32_t, uint32_t, uint32_t, uint32_t);
ColourARGB_t COLOUR_extract_argb(uint32_t argb);
ColourAHSV_t COLOUR_argb_to_ahsv(ColourARGB_t*);
ColourARGB_t COLOUR_ahsv_to_argb(ColourAHSV_t*);
uint32_t COLOUR_desaturate(uint32_t, float);


#endif // COLOUR_H_
