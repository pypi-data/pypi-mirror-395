#pragma once

#include <SDL.h>
#include <vector>

// A minimal 2D graphics engine binding for Python using SDL.
namespace mini {

    // We define our own event types so Python doesn't need to know about SDL constants.
    enum class EventType {
        Unknown = 0,
        Quit,
        KeyDown,
        KeyUp
    };

    // A simple event structure to pass events to Python.
    struct Event {
        EventType type;
        int key;  // SDL key code (e.g., 27 for ESC). 0 if not applicable.
    };

    // The main engine class that wraps SDL functionality.
    class Engine {
    public:
        Engine();
        ~Engine();

        // Initialize the engine with a window of given width, height, and title.
        void init(int width, int height, const char* title);

        // Clear the screen to a default color (black) and get ready to draw.
        void begin_frame();

        // Present what has been drawn.
        void end_frame();

        // Draw a simple filled rectangle (we'll use a fixed color for now).
        void draw_rect(int x, int y, int w, int h);

        // Sprite drawing stub for later.
        void draw_sprite(int texture_id, int x, int y, int w, int h);

        // Poll all pending events and return them.
        std::vector<Event> poll_events();

    private:
        SDL_Window* window_;
        SDL_Renderer* renderer_;
        bool initialized_;
    };

} // namespace mini
