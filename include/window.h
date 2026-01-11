#ifndef WINDOW_H_
#define WINDOW_H_

// Standard library
#include <SDL_events.h>
#include <stdbool.h>

// Third party
#include <SDL.h>
#include <SDL_render.h>

// Local
#include "vector.h"

// Screen dimension constants
extern const int SCREEN_WIDTH;
extern const int SCREEN_HEIGHT;
extern const int RENDER_WIDTH;
extern const int RENDER_HEIGHT;
extern const float VIEW_ASPECT;


typedef struct {
    int width;
    int height;
    int view_width;
    int view_height;
    SDL_Window *window;
    SDL_Renderer *renderer;
    SDL_Texture *texture;
    SDL_Surface *surface;
    bool quit;
    bool resized;
} WindowManager_t;


typedef enum {
    RESOLUTION_1280x720 = 0,
    RESOLUTION_1920x1080,
    RESOLUTION_2560x1440,
    RESOLUTION_3840x2160,
    NUM_SCREEN_RESOLUTION
} ScreenResolution_e;


int WindowMgr_init();
void WindowMgr_quit();
bool WindowMgr_should_quit();
bool WindowMgr_should_resize();
void WindowMgr_update_size(int);
void WindowMgr_resize_window();
void WindowMgr_map_screen_to_px(Coordinate_t*);
void WindowMgr_render();
void WindowMgr_destroy();


#endif // WINDOW_H_
