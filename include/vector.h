#ifndef VECTOR_H_
#define VECTOR_H_


typedef struct {
    int x;
    int y;
} Coordinate_t;

typedef struct {
    double x;
    double y;
} Vector2D_t;


void VECTOR_normalise(Vector2D_t*);


#endif // VECTOR_H_
