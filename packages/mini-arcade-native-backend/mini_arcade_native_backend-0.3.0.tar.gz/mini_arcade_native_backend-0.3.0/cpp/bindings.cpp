#include <pybind11/pybind11.h>
#include <pybind11/stl.h>   // so std::vector<Event> becomes a Python list

#include "engine.h"

namespace py = pybind11;

PYBIND11_MODULE(_native, m) {
    m.doc() = "Mini arcade native SDL2 backend";

    // Bind the EventType enum
    py::enum_<mini::EventType>(m, "EventType")
        .value("Unknown", mini::EventType::Unknown)
        .value("Quit", mini::EventType::Quit)
        .value("KeyDown", mini::EventType::KeyDown)
        .value("KeyUp", mini::EventType::KeyUp)
        .export_values();

    // Bind the Event struct
    py::class_<mini::Event>(m, "Event")
        .def_readonly("type", &mini::Event::type)
        .def_readonly("key", &mini::Event::key);

    // Bind the Engine class
    py::class_<mini::Engine>(m, "Engine")
        .def(py::init<>())
        .def("init", &mini::Engine::init,
                py::arg("width"), py::arg("height"), py::arg("title"))

        .def("begin_frame", &mini::Engine::begin_frame)
        .def("end_frame", &mini::Engine::end_frame)

        .def("draw_rect", &mini::Engine::draw_rect,
                py::arg("x"), py::arg("y"), py::arg("w"), py::arg("h"))
        .def("draw_sprite", &mini::Engine::draw_sprite,
                py::arg("texture_id"), py::arg("x"), py::arg("y"),
                py::arg("w"), py::arg("h"))

        .def("load_font", &mini::Engine::load_font,
                py::arg("path"), py::arg("pt_size"))

        .def(
            "draw_text",
            &mini::Engine::draw_text,
                py::arg("text"),
                py::arg("x"),
                py::arg("y"),
                py::arg("r"),
                py::arg("g"),
                py::arg("b")
        )
        .def("poll_events", &mini::Engine::poll_events);
}
