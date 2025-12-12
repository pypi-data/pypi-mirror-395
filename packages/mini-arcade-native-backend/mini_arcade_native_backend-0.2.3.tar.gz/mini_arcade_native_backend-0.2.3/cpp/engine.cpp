#include "engine.h"

#include <stdexcept>
#include <iostream>

namespace mini {

    Engine::Engine()
        : window_(nullptr),
          renderer_(nullptr),
          initialized_(false)
    {
    }

    Engine::~Engine()
    {
        if (renderer_ != nullptr) {
            SDL_DestroyRenderer(renderer_);
            renderer_ = nullptr;
        }

        if (window_ != nullptr) {
            SDL_DestroyWindow(window_);
            window_ = nullptr;
        }

        if (initialized_) {
            SDL_Quit();
            initialized_ = false;
        }
    }

    void Engine::init(int width, int height, const char* title)
    {
        if (initialized_) {
            return; // already initialized
        }

        if (SDL_Init(SDL_INIT_VIDEO) != 0) {
            throw std::runtime_error(std::string("SDL_Init Error: ") + SDL_GetError());
        }

        window_ = SDL_CreateWindow(
            title,
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            width,
            height,
            SDL_WINDOW_SHOWN
        );

        if (window_ == nullptr) {
            std::string msg = std::string("SDL_CreateWindow Error: ") + SDL_GetError();
            SDL_Quit();
            throw std::runtime_error(msg);
        }

        renderer_ = SDL_CreateRenderer(
            window_,
            -1,
            SDL_RENDERER_ACCELERATED
        );

        if (renderer_ == nullptr) {
            std::string msg = std::string("SDL_CreateRenderer Error: ") + SDL_GetError();
            SDL_DestroyWindow(window_);
            window_ = nullptr;
            SDL_Quit();
            throw std::runtime_error(msg);
        }

        initialized_ = true;
    }

    void Engine::begin_frame()
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        // Clear to black
        SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
        SDL_RenderClear(renderer_);
    }

    void Engine::end_frame()
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        SDL_RenderPresent(renderer_);
    }

    void Engine::draw_rect(int x, int y, int w, int h)
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        SDL_Rect rect;
        rect.x = x;
        rect.y = y;
        rect.w = w;
        rect.h = h;

        // White rectangle for now (you can parameterize later).
        SDL_SetRenderDrawColor(renderer_, 255, 255, 255, 255);
        SDL_RenderFillRect(renderer_, &rect);
    }

    void Engine::draw_sprite(int /*texture_id*/, int /*x*/, int /*y*/, int /*w*/, int /*h*/)
    {
        // TODO: placeholder for later texture management.
    }

    std::vector<Event> Engine::poll_events()
    {
        std::vector<Event> events;
        SDL_Event sdl_event;

        while (SDL_PollEvent(&sdl_event)) {
            Event ev;
            ev.type = EventType::Unknown;
            ev.key = 0;

            switch (sdl_event.type) {
            case SDL_QUIT:
                ev.type = EventType::Quit;
                break;

            case SDL_KEYDOWN:
                ev.type = EventType::KeyDown;
                ev.key = sdl_event.key.keysym.sym;
                break;

            case SDL_KEYUP:
                ev.type = EventType::KeyUp;
                ev.key = sdl_event.key.keysym.sym;
                break;

            default:
                ev.type = EventType::Unknown;
                break;
            }

            events.push_back(ev);
        }

        return events;
    }

} // namespace mini
