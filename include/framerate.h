#ifndef FRAMERATE_H_
#define FRAMERATE_H_

// Standard library
#include <stdint.h>
#include <stdbool.h>

// Third party
#include <SDL_render.h>

// Local
#include "timer.h"

// Constants
static const double TARGET_FPS = 60.0;


typedef struct {
    Timer_t frame_start;
    uint64_t frame_length_ms;
    uint64_t frame_times_ms[10];
    double frame_average_ms;
} FramerateManager_t;

void FramerateMgr_frame_start();
void FramerateMgr_update_average();
void FramerateMgr_fix_framerate();


#endif // FRAMERATE_H_
