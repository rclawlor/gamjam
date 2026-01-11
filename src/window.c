// Third party
#include <SDL.h>
#include <math.h>

// Local
#include "draw.h"
#include "vector.h"
#include "window.h"


// Constants
const int SCREEN_WIDTH = 1920;
const int SCREEN_HEIGHT = 1080;
const int RENDER_WIDTH = 320;
const int RENDER_HEIGHT = 200;
const float VIEW_ASPECT = 1.6;

// Module variables
WindowManager_t m_WindowMgr = {};


/**
 * Initialise window manager
**/
int WindowMgr_init()
{
    m_WindowMgr.quit = false;
    m_WindowMgr.resized = false;

    m_WindowMgr.width = SCREEN_WIDTH;
    m_WindowMgr.height = SCREEN_HEIGHT;

    m_WindowMgr.view_width = m_WindowMgr.width;
    m_WindowMgr.view_height = m_WindowMgr.height;
    
    m_WindowMgr.window = SDL_CreateWindow(
        "GamJam",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SDL_WINDOW_SHOWN
    );
    if (m_WindowMgr.window == NULL)
    {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    m_WindowMgr.renderer = SDL_CreateRenderer(
        m_WindowMgr.window, 
        -1,
        SDL_RENDERER_ACCELERATED
    );
    if (m_WindowMgr.renderer == NULL)
    {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    m_WindowMgr.texture = SDL_CreateTexture(
        m_WindowMgr.renderer,
        SDL_PIXELFORMAT_ARGB8888,
        SDL_TEXTUREACCESS_STATIC,
        RENDER_WIDTH,
        RENDER_HEIGHT
    );
    if (m_WindowMgr.texture == NULL)
    {
        printf("Texture could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    m_WindowMgr.surface = SDL_GetWindowSurface(m_WindowMgr.window);
    if (m_WindowMgr.surface == NULL)
    {
        printf("Surface could not be created! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    // Fill the surface white
    int ret = SDL_FillRect(m_WindowMgr.surface, NULL, SDL_MapRGB(m_WindowMgr.surface->format, 0xff, 0xff, 0xff));
    if (ret < 0)
    {
        printf("Surface could not be filled! SDL_Error: %s\n", SDL_GetError());
        return 1;
    }

    return 0;
}


/**
 * Update window manager dimensions
 *
 * @param res       window resolution
**/
void WindowMgr_update_size(int res)
{
    switch (res)
    {
        case RESOLUTION_1280x720:
            m_WindowMgr.width = 1280;
            m_WindowMgr.height = 720;
            break;
        case RESOLUTION_1920x1080:
            m_WindowMgr.width = 1920;
            m_WindowMgr.height = 1080;
            break;
        case RESOLUTION_2560x1440:
            m_WindowMgr.width = 2560;
            m_WindowMgr.height = 1440;
            break;
        case RESOLUTION_3840x2160:
            m_WindowMgr.width = 3840;
            m_WindowMgr.height = 2160;
            break;
        default:
            return;
    }
    m_WindowMgr.resized = true;
}


/**
 * Resize window using set screen dimensions
**/
void WindowMgr_resize_window()
{
    m_WindowMgr.resized = false;
    SDL_SetWindowSize(m_WindowMgr.window, m_WindowMgr.width, m_WindowMgr.height);
    m_WindowMgr.view_width = m_WindowMgr.width;
    m_WindowMgr.view_height = m_WindowMgr.height;

    SDL_Surface *surface = SDL_GetWindowSurface(m_WindowMgr.window);
    SDL_FillRect(surface, NULL, SDL_MapRGB(surface->format, 0x00, 0x00, 0x00));
    SDL_UpdateWindowSurface(m_WindowMgr.window);
}


/**
* Map (x, y) screen coordinates to pixel coordinates
*
* @param c              coordinate to map
**/
void WindowMgr_map_screen_to_px(Coordinate_t *c)
{
    c->x = roundf(RENDER_WIDTH * (float)(c->x) / (float)m_WindowMgr.width);
    c->y = roundf(RENDER_HEIGHT * (float)c->y / (float)m_WindowMgr.height);
}


/**
 * Should application quit?
**/
bool WindowMgr_should_quit()
{
    return m_WindowMgr.quit;
}


/**
* Set application to quit
**/
void WindowMgr_quit()
{
    m_WindowMgr.quit = true;
}


/**
 * Should window resize?
**/
bool WindowMgr_should_resize()
{
    return m_WindowMgr.resized;
}


/**
* Render pixels to screen
**/
void WindowMgr_render()
{
    SDL_SetRenderTarget(m_WindowMgr.renderer, m_WindowMgr.texture);
    SDL_UpdateTexture(m_WindowMgr.texture, NULL, DRAW_get_pixels(), RENDER_WIDTH * sizeof(uint32_t));
    
    // Set rendering space and render to screen
    SDL_Rect renderQuad = {
        m_WindowMgr.width / 2 - m_WindowMgr.view_width / 2,
        m_WindowMgr.height / 2 - m_WindowMgr.view_height / 2,
        m_WindowMgr.view_width,
        m_WindowMgr.view_height
    };
    SDL_RenderCopyEx(m_WindowMgr.renderer, m_WindowMgr.texture, NULL, &renderQuad, 0, 0, false);
    SDL_RenderPresent(m_WindowMgr.renderer);
}


/**
 * Destroy window
**/
void WindowMgr_destroy()
{
    SDL_DestroyWindow(m_WindowMgr.window);
}
