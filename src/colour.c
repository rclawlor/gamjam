// Standard library
#include <math.h>
#include <stdint.h>

// Local
#include "colour.h"


/**
 * Extract separate A, R, G and B values from 32 bit uint
 *
 * @param argb      ARGB8888 format colour
**/
ColourARGB_t COLOUR_extract_argb(uint32_t argb)
{
    uint8_t a, r, g, b = 0;
    a = (argb & 0xff000000) >> 24;
    r = (argb & 0x00ff0000) >> 16;
    g = (argb & 0x0000ff00) >> 8;
    b = argb & 0x000000ff;

    ColourARGB_t c = { a, r, g, b };

    return c;
}


/**
 * Compute ARGB average of 3 colours
 *
 * @param argb_a    first colour
 * @param argb_b    second colour
 * @param argb_c    third colour
**/
uint32_t COLOUR_argb_average_3(uint32_t argb_a, uint32_t argb_b, uint32_t argb_c)
{
    ColourARGB_t c_a, c_b, c_c;
    c_a = COLOUR_extract_argb(argb_a);
    c_b = COLOUR_extract_argb(argb_b);
    c_c = COLOUR_extract_argb(argb_c);

    uint32_t a, r, g, b = 0;
    a = (c_a.a + c_b.a + c_c.a) / 3;
    r = (c_a.r + c_b.r + c_c.r) / 3;
    g = (c_a.g + c_b.g + c_c.g) / 3;
    b = (c_a.b + c_b.b + c_c.b) / 3;

    return ARGB(a, r, g, b);
}


/**
 * Compute ARGB 1D gaussian of 5 colours
 *
 * @param argb_a    first colour
 * @param argb_b    second colour
 * @param argb_c    third colour
 * @param argb_d    fourth colour
 * @param argb_e    fifth colour
**/
uint32_t COLOUR_argb_gaussian_5(
    uint32_t argb_a,
    uint32_t argb_b,
    uint32_t argb_c,
    uint32_t argb_d,
    uint32_t argb_e
)
{
    ColourARGB_t c_a, c_b, c_c, c_d, c_e;
    c_a = COLOUR_extract_argb(argb_a);
    c_b = COLOUR_extract_argb(argb_b);
    c_c = COLOUR_extract_argb(argb_c);
    c_d = COLOUR_extract_argb(argb_d);
    c_e = COLOUR_extract_argb(argb_e);

    uint32_t a, r, g, b = 0;
    a = (c_a.a + 4 * c_b.a + 6 * c_c.a + 4 * c_d.a + c_e.a) / 16;
    r = (c_a.r + 4 * c_b.r + 6 * c_c.r + 4 * c_d.r + c_e.r) / 16;
    g = (c_a.g + 4 * c_b.g + 6 * c_c.g + 4 * c_d.g + c_e.g) / 16;
    b = (c_a.b + 4 * c_b.b + 6 * c_c.b + 4 * c_d.b + c_e.b) / 16;

    return ARGB(a, r, g, b);
}


/**
 * Convert ARGB to AHSV colourspace
 *
 * @param c     ARGB colour to convert
**/
ColourAHSV_t COLOUR_argb_to_ahsv(ColourARGB_t *c)
{
    double r, g, b;
    r = (double)c->r / 255.0;
    g = (double)c->g / 255.0;
    b = (double)c->b / 255.0;

    double cmax, cmin, delta;
    cmax = fmax(r, fmax(g, b));
    cmin = fmin(r, fmin(g, b));
    delta = cmax - cmin;

    int h;
    double s, v;
    if (r == cmax)
    {
        h = (int)(60.0 * ((g - b) / delta));
        h %= 360;
        if (h < 0)
        {
            h += 360;
        }
    }
    else if (g == cmax)
    {
        h = 60 * ((b - r) / delta + 2);
    }
    else if (b == cmax)
    {
        h = 60 * ((r - g) / delta + 4);
    }

    s = cmax == 0 ? 0 : delta / cmax;
    v = cmax;

    ColourAHSV_t output = { c->a, h, s, v };

    return output;
}


/**
 * Convert AHSV to ARGB colourspace
 *
 * @param c     AHSV colour to convert
**/
ColourARGB_t COLOUR_ahsv_to_argb(ColourAHSV_t *c)
{
    float r, g, b;

    float h = (float)c->h / 360;
	float s = c->s;
	float v = c->v;
	
	int i = floor(h * 6);
	float f = h * 6 - i;
	float p = v * (1 - s);
	float q = v * (1 - f * s);
	float t = v * (1 - (1 - f) * s);
	
	switch (i % 6) {
		case 0: r = v, g = t, b = p; break;
		case 1: r = q, g = v, b = p; break;
		case 2: r = p, g = v, b = t; break;
		case 3: r = p, g = q, b = v; break;
		case 4: r = t, g = p, b = v; break;
		case 5: r = v, g = p, b = q; break;
	}

    ColourARGB_t output = {
        c->a,
        r * 255,
        g * 255,
        b * 255
    };

    return output;
}


/**
 * Desaturate ARGB colour
 *
 * @param colour    colour to desaturate
 * @param scale     saturation scale factor
**/
uint32_t COLOUR_desaturate(uint32_t colour, float scale)
{
    ColourARGB_t argb = COLOUR_extract_argb(colour);
    ColourAHSV_t ahsv = COLOUR_argb_to_ahsv(&argb);
    ahsv.s *= scale;
    argb = COLOUR_ahsv_to_argb(&ahsv);

    return ARGB(argb.a, argb.r, argb.g, argb.b);
}
