// Standard library
#include <stdint.h>

// Local
#include "animation.h"
#include "timer.h"


/**
 * Initialise and start animation
 *
 * @param animation     animation to start
 * @param timestep      timestep between frames
 * @param n_frames      number of animation frames
**/
void ANIMATION_start(SpriteAnimation_t *animation, double timestep, uint8_t n_frames)
{
    Timer_t anim_timer = {};
    animation->anim_timer = anim_timer;
    Timer_set_now(&animation->anim_timer);
    animation->timestep = timestep;
    animation->n_frames = n_frames;
    animation->current_frame = 0;
}


/**
 * Step through animation
 *
 * @param animation     animation to start
**/
void ANIMATION_step(SpriteAnimation_t *animation)
{
    if (Timer_get_elapsed_time(&animation->anim_timer) >= animation->timestep)
    {
        Timer_set_now(&animation->anim_timer);
        animation->current_frame += 1;
        if (animation->current_frame >= animation->n_frames)
        {
            animation->current_frame = 0;
        }
    }
}
