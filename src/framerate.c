// Standard library
#include <math.h>
#include <stdbool.h>

// Third party
#include <SDL_timer.h>

// Local
#include "framerate.h"
#include "timer.h"


// Module variables
FramerateManager_t m_FramerateMgr = {0};


/**
 * Set start of frame time
**/
void FramerateMgr_frame_start()
{
    Timer_set_now(&m_FramerateMgr.frame_start);
}


/**
 * Add current frame time to FIFO queue
 * and return average
**/
void FramerateMgr_update_average()
{
    int i;
    float sum = m_FramerateMgr.frame_length_ms;
    for (i = 0; i < 9; i++)
    {
        m_FramerateMgr.frame_times_ms[i] = m_FramerateMgr.frame_times_ms[i + 1];
        sum += m_FramerateMgr.frame_times_ms[i];
    }
    m_FramerateMgr.frame_times_ms[9] = m_FramerateMgr.frame_length_ms;

    m_FramerateMgr.frame_average_ms = sum / 10;
}


/**
 * Fix framerate by delaying correct time
**/
void FramerateMgr_fix_framerate()
{
    double t_delay = (1000.0 / TARGET_FPS) - 1000 * Timer_get_elapsed_time(&m_FramerateMgr.frame_start);
    if (t_delay > 0)
    {
        SDL_Delay(floor(t_delay));
    }
    m_FramerateMgr.frame_length_ms = 1000 * Timer_get_elapsed_time(&m_FramerateMgr.frame_start);
}
