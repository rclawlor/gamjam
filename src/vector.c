// Standard library
#include <math.h>

// Local
#include "vector.h"


/**
 * Normalise 2D vector
 *
 * @param vec       vector to normalise
**/
void VECTOR_normalise(Vector2D_t *vec)
{
    double x = vec->x;
    double y = vec->y;
    double den = sqrt(vec->x * vec->x + vec->y * vec->y);
    if (den == 0)
    {
        return;
    }

    vec->x = x / den;
    vec->y = y / den;
}
