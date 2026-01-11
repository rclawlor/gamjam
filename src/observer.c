// Local
#include "error.h"
#include "observer.h"


TopicSubscribers_t topic_table[NUM_OBSERVER_TOPICS] = {
    [TOPIC_KEYDOWN]     = { .subscribers = {}, .count = 0 },
    [TOPIC_KEYUP]       = { .subscribers = {}, .count = 0 },
    [TOPIC_MOUSE_CLICK] = { .subscribers = {}, .count = 0 },
};

char* ObserverTopic_str[NUM_OBSERVER_TOPICS] = {
    [TOPIC_KEYDOWN] = "TOPIC_KEYDOWN",
    [TOPIC_KEYUP] = "TOPIC_KEYUP",
    [TOPIC_MOUSE_CLICK] = "TOPIC_MOUSE_CLICK"
};


/**
 * Publish to a topic
 *
 * @param topic     topic to publish to
 * @param data      data to send to subscribers
**/
void OBSERVER_Publish(ObserverTopic_e topic, void *data)
{
    TopicSubscribers_t *ts = &topic_table[topic];
    int i;
    for (i = 0; i < ts->count; i++)
    {
        if (ts->subscribers[i])
        {
            ts->subscribers[i](data);
        }
    }
}


/**
 * Subscribe to a topic
 *
 * @param topic     topic to subscribe to
 * @param cb        callback function
**/
Error_e OBSERVER_Subscribe(ObserverTopic_e topic, SubscriberCb_t cb)
{
    TopicSubscribers_t *ts = &topic_table[topic];

    int sub_idx = ts->count;
    if (sub_idx >= MAX_SLOTS)
    {
        return ERROR_OUT_OF_BOUNDS;
    }

    int i;
    for (i = 0; i < ts->count; i++)
    {
        if (ts->subscribers[i] == cb)
        {
            return ERROR_SUBSCRIPTION_EXISTS;
        }
    }

    ts->subscribers[sub_idx] = cb;
    ts->count += 1;

    return OK;
}


/**
 * Unsubscribe from a topic
 *
 * @param topic     topic to unsubscribe from
 * @param cb        callback function to unregister
**/
void OBSERVER_Unsubscribe(ObserverTopic_e topic, SubscriberCb_t cb)
{
    TopicSubscribers_t *ts = &topic_table[topic];

    int i;
    for (i = 0; i < ts->count; i++)
    {
        if (ts->subscribers[i] == cb)
        {
            int j;
            for (j = i; j < ts->count - 1; j++)
            {
                ts->subscribers[j] = ts->subscribers[j+1];
            }
            ts->count -= 1;
            break;
        }
    }

    return;
}
