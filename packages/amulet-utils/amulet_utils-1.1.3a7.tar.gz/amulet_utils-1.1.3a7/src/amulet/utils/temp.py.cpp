#include <pybind11/pybind11.h>
#include <pybind11/stl/filesystem.h>

#include "temp.hpp"

namespace py = pybind11;

void init_temp(py::module m_parent)
{
    auto m = m_parent.def_submodule("temp");

    m.def(
        "get_temp_dir",
        Amulet::get_temp_dir,
        py::doc("Get the directory in which temporary directories will be created.\n"
                "This is configurable by setting the \"CACHE_DIR\" environment variable.\n"
                "Thread safe."));

    m.def(
        "set_temp_dir",
        Amulet::set_temp_dir,
        py::arg("path"),
        py::doc("Set the temporary directory path.\n"
                "It must be a path to an existing directory.\n"
                "Anything using the previous path will continue using that path."));
}
