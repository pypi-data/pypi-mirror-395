#include "engine.h"

#include <stdexcept>
#include <iostream>

namespace mini {

    Engine::Engine()
        : window_(nullptr),
            renderer_(nullptr),
            initialized_(false),
            font_(nullptr),
            clear_color_{0, 0, 0, 255}
    {
    }

    Engine::~Engine()
    {
        if (font_ != nullptr) {
            TTF_CloseFont(font_);
            font_ = nullptr;
        }

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

        if (TTF_Init() != 0) {
            std::string msg = std::string("TTF_Init Error: ") + TTF_GetError();
            SDL_Quit();
            throw std::runtime_error(msg);
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
            TTF_Quit();
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
            TTF_Quit();
            SDL_Quit();
            throw std::runtime_error(msg);
        }

        initialized_ = true;
    }

    void Engine::set_clear_color(int r, int g, int b)
    {
        auto clamp = [](int v) {
            if (v < 0) return 0;
            if (v > 255) return 255;
            return v;
        };

        clear_color_.r = static_cast<Uint8>(clamp(r));
        clear_color_.g = static_cast<Uint8>(clamp(g));
        clear_color_.b = static_cast<Uint8>(clamp(b));
        clear_color_.a = 255;
    }

    void Engine::begin_frame()
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        // use stored clear color instead of hard-coded black
        SDL_SetRenderDrawColor(
            renderer_,
            clear_color_.r,
            clear_color_.g,
            clear_color_.b,
            clear_color_.a
        );
        SDL_RenderClear(renderer_);
    }

    void Engine::end_frame()
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        SDL_RenderPresent(renderer_);
    }

    void Engine::draw_rect(int x, int y, int w, int h, int r, int g, int b)
    {
        if (!initialized_ || renderer_ == nullptr) {
            return;
        }

        auto clamp = [](int v) {
            if (v < 0) return 0;
            if (v > 255) return 255;
            return v;
        };

        SDL_Rect rect{ x, y, w, h };

        SDL_SetRenderDrawColor(
            renderer_,
            static_cast<Uint8>(clamp(r)),
            static_cast<Uint8>(clamp(g)),
            static_cast<Uint8>(clamp(b)),
            255
        );
        SDL_RenderFillRect(renderer_, &rect);

    }

    void Engine::draw_sprite(int /*texture_id*/, int /*x*/, int /*y*/, int /*w*/, int /*h*/)
    {
        // TODO: placeholder for later texture management.
    }

    // Load a TTF font from file at specified point size.
    void Engine::load_font(const char* path, int pt_size)
    {
        if (!initialized_) {
            throw std::runtime_error("Engine::init must be called before load_font");
        }

        if (font_ != nullptr) {
            TTF_CloseFont(font_);
            font_ = nullptr;
        }

        font_ = TTF_OpenFont(path, pt_size);
        if (!font_) {
            std::string msg = std::string("TTF_OpenFont Error: ") + TTF_GetError();
            throw std::runtime_error(msg);
        }
    }

    // Draw text at specified position.
    void Engine::draw_text(const char* text, int x, int y, int r, int g, int b)
    {
        if (!initialized_ || renderer_ == nullptr || font_ == nullptr) {
            return;
        }

        // clamp a bit to be safe
        auto clamp = [](int v) {
            if (v < 0) return 0;
            if (v > 255) return 255;
            return v;
        };

        SDL_Color color = { (Uint8)clamp(r), (Uint8)clamp(g), (Uint8)clamp(b), 255 }; // white text
        SDL_Surface* surface = TTF_RenderUTF8_Blended(font_, text, color);
        if (!surface) {
            std::cerr << "TTF_RenderUTF8_Blended Error: " << TTF_GetError() << std::endl;
            return;
        }

        SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer_, surface);
        if (!texture) {
            std::cerr << "SDL_CreateTextureFromSurface Error: " << SDL_GetError() << std::endl;
            SDL_FreeSurface(surface);
            return;
        }

        SDL_Rect dstRect;
        dstRect.x = x;
        dstRect.y = y;
        dstRect.w = surface->w;
        dstRect.h = surface->h;

        SDL_FreeSurface(surface);

        SDL_RenderCopy(renderer_, texture, nullptr, &dstRect);
        SDL_DestroyTexture(texture);
    }

    bool Engine::capture_frame(const char* path)
    {
        if (!initialized_ || renderer_ == nullptr) {
            return false;
        }

        int width = 0;
        int height = 0;
        if (SDL_GetRendererOutputSize(renderer_, &width, &height) != 0) {
            std::cerr << "SDL_GetRendererOutputSize Error: " << SDL_GetError() << std::endl;
            return false;
        }

        // Create a surface to hold the pixels (32-bit RGBA)
        SDL_Surface* surface = SDL_CreateRGBSurfaceWithFormat(
            0,
            width,
            height,
            32,
            SDL_PIXELFORMAT_ARGB8888
        );

        if (!surface) {
            std::cerr << "SDL_CreateRGBSurfaceWithFormat Error: " << SDL_GetError() << std::endl;
            return false;
        }

        // Read pixels from the current render target into the surface
        if (SDL_RenderReadPixels(
                renderer_,
                nullptr,                        // whole screen
                surface->format->format,
                surface->pixels,
                surface->pitch) != 0)
        {
            std::cerr << "SDL_RenderReadPixels Error: " << SDL_GetError() << std::endl;
            SDL_FreeSurface(surface);
            return false;
        }

        // Save as BMP (simple, no extra dependencies).
        // Use .bmp extension in the path you pass from Python.
        if (SDL_SaveBMP(surface, path) != 0) {
            std::cerr << "SDL_SaveBMP Error: " << SDL_GetError() << std::endl;
            SDL_FreeSurface(surface);
            return false;
        }

        SDL_FreeSurface(surface);
        return true;
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
