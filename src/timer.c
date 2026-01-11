// Standard library
#if defined(_WIN32)
#elif defined(__linux__)

#include <time.h>

#elif defined(__APPLE__)
#endif // OS check

// Local
#include "timer.h"


/**
 * Set timer to current time
 *
 * @param timer     timer to set
**/
void Timer_set_now(Timer_t *timer)
{
    #if defined(_WIN32)
    #elif defined(__linux__)

    struct timespec ts;
    int ret = clock_gettime(CLOCK_MONOTONIC, &ts);

    timer->t_sec = ts.tv_sec;
    timer->t_nsec = ts.tv_nsec;

    #elif defined(__APPLE__)
    #endif // OS check
}


/**
 * Calculate elapsed time
 *
 * @param timer     timer used as reference
**/
double Timer_get_elapsed_time(Timer_t *timer)
{
    if (!timer)
    {
        return -1;
    }
    double t_delta = 0.0;

    #if defined(_WIN32)
    #elif defined(__linux__)

    struct timespec ts;
    int ret = clock_gettime(CLOCK_MONOTONIC, &ts);

    double t_start = timer->t_sec + (double)timer->t_nsec * 1e-9;
    double t_now = ts.tv_sec + (double)ts.tv_nsec * 1e-9;
    t_delta = t_now - t_start;

    #elif defined(__APPLE__)
    #endif // OS check

    return t_delta;
}


/**
 * Compute time delta between timers
 *
 * @param timer_a   first timer
 * @param timer_b   second timer
**/
double Timer_get_delta(Timer_t *timer_a, Timer_t *timer_b)
{
    if (!timer_a || !timer_b)
    {
        return -1;
    }
    double t_a = timer_a->t_sec + (double)timer_a->t_nsec * 1e-9;
    double t_b = timer_b->t_sec + (double)timer_b->t_nsec * 1e-9;

    return t_a - t_b;
}
