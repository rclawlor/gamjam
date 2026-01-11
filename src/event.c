// Third party
#include <SDL.h>
#include <SDL_events.h>

// Local
#include "event.h"
#include "observer.h"
#include "vector.h"
#include "window.h"


/**
 * Poll incoming events
**/
void EVENT_poll()
{
    SDL_Event e;
    KeyEvent_t k_evt;
    MouseClickEvent_t mouse_evt;
    Coordinate_t mouse_pos;
    while (SDL_PollEvent(&e))
    {
        switch (e.type)
        {
            case SDL_QUIT:
                WindowMgr_quit();
                break;
            case SDL_WINDOWEVENT:
                /* Unused */
                break;
            case SDL_KEYDOWN:
                k_evt.key = e.key.keysym.sym;
                OBSERVER_Publish_KEYDOWN(&k_evt);
                break;
            case SDL_KEYUP:
                k_evt.key = e.key.keysym.sym;
                OBSERVER_Publish_KEYUP(&k_evt);
                break;
            case SDL_MOUSEBUTTONDOWN:
                mouse_pos.x = e.button.x;
                mouse_pos.y = e.button.y;
                WindowMgr_map_screen_to_px(&mouse_pos);
                mouse_evt.x = mouse_pos.x;
                mouse_evt.y = mouse_pos.y;
                OBSERVER_Publish_MOUSE_CLICK(&mouse_evt);
                break;
            default:
                break;
        }
    }
}
