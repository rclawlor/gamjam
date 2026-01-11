#ifndef ANIMATION_H_
#define ANIMATION_H_

// Standard library
#include <stdint.h>

// Local
#include "timer.h"


typedef struct {
    Timer_t anim_timer;
    double timestep;
    uint8_t current_frame;
    uint8_t n_frames;
} SpriteAnimation_t;


void ANIMATION_start(SpriteAnimation_t*, double, uint8_t);
void ANIMATION_step(SpriteAnimation_t*);


#endif // ANIMATION_H_
