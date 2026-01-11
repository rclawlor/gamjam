#ifndef TIMER_H_
#define TIMER_H_

#include <stdint.h>


typedef struct {
    uint64_t t_sec;
    uint64_t t_nsec;
} Timer_t;

void Timer_set_now(Timer_t*);
double Timer_get_elapsed_time(Timer_t*);
double Timer_get_delta(Timer_t*, Timer_t*);


#endif // TIMER_H_
