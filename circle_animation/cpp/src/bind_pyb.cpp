#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using namespace pybind11::literals;

namespace circle_vertex_instanced {
    void circle_vis(py::array_t<float> pos, py::array_t<float> radii, py::array_t<float> dims, py::array_t<float> colors, py::array_t<float> background_color, const std::string vshader, const std::string fshader, bool time_it);
}

namespace circle_vertex {
    void circle_vis(py::array_t<float> pos, py::array_t<float> radii, py::array_t<float> dims, py::array_t<float> colors, py::array_t<float> background_color, const std::string vshader, const std::string fshader, bool time_it);
}

namespace circle_fragment_instanced {
    void circle_vis(py::array_t<float> pos, py::array_t<float> radii, py::array_t<float> dims, py::array_t<float> colors, py::array_t<float> background_color, const std::string vshader, const std::string fshader, bool time_it);
}

namespace circle_fragment {
    void circle_vis(py::array_t<float> pos, py::array_t<float> radii, py::array_t<float> dims, py::array_t<float> colors, py::array_t<float> background_color, const std::string vshader, const std::string fshader, bool time_it);
}

PYBIND11_MODULE(circle_vis, m) {
    m.def("circle_vertex_instanced", circle_vertex_instanced::circle_vis, "position"_a,  "radii"_a, "dims"_a, "colors"_a,  "background_color"_a,  "vshader"_a, "fshader"_a, "time_it"_a);

    m.def("circle_vertex", circle_vertex::circle_vis, "position"_a,  "radii"_a, "dims"_a, "colors"_a,  "background_color"_a,  "vshader"_a, "fshader"_a, "time_it"_a);

    m.def("circle_fragment_instanced", circle_fragment_instanced::circle_vis, "position"_a,  "radii"_a, "dims"_a, "colors"_a,  "background_color"_a,  "vshader"_a, "fshader"_a, "time_it"_a);

    m.def("circle_fragment", circle_fragment::circle_vis, "position"_a,  "radii"_a, "dims"_a, "colors"_a,  "background_color"_a,  "vshader"_a, "fshader"_a, "time_it"_a);
}
