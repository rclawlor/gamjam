#ifndef OBSERVER_H_
#define OBSERVER_H_

// Third party
#include <SDL_events.h>
#include <SDL_keycode.h>

// Local
#include "error.h"


#define MAX_SLOTS 16

#define DECLARE_OBSERVER_TOPIC(name, type) \
    static inline void OBSERVER_Subscribe_##name(void (*cb)(type*)) { \
        OBSERVER_Subscribe(TOPIC_##name, (SubscriberCb_t)cb); \
    } \
    static inline void OBSERVER_Unsubscribe_##name(void (*cb)(type*)) { \
        OBSERVER_Unsubscribe(TOPIC_##name, (SubscriberCb_t)cb); \
    } \
    static inline void OBSERVER_Publish_##name(type* data) { \
        OBSERVER_Publish(TOPIC_##name, (void*)data); \
    }


// Topic data types
typedef struct {
    SDL_Keycode key;
} KeyEvent_t;

typedef struct {
    uint32_t x;
    uint32_t y;
} MouseClickEvent_t;


typedef void (*SubscriberCb_t)(void* data);

typedef struct {
    SubscriberCb_t subscribers[MAX_SLOTS];
    int count;
} TopicSubscribers_t;

typedef enum {
    TOPIC_KEYDOWN = 0,
    TOPIC_KEYUP,
    TOPIC_MOUSE_CLICK,
    NUM_OBSERVER_TOPICS
} ObserverTopic_e;

extern char* ObserverTopic_str[NUM_OBSERVER_TOPICS];


void OBSERVER_Publish(ObserverTopic_e, void*);
Error_e OBSERVER_Subscribe(ObserverTopic_e, SubscriberCb_t);
void OBSERVER_Unsubscribe(ObserverTopic_e, SubscriberCb_t);

// Topic declarations
DECLARE_OBSERVER_TOPIC(KEYDOWN, KeyEvent_t);
DECLARE_OBSERVER_TOPIC(KEYUP, KeyEvent_t);
DECLARE_OBSERVER_TOPIC(MOUSE_CLICK, MouseClickEvent_t);


#endif // OBSERVER_H_
