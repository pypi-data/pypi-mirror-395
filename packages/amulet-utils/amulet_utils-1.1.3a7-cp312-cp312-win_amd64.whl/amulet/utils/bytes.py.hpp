#pragma once

#include <pybind11/pybind11.h>

#include "bytes.hpp"

namespace pybind11 {
namespace detail {

    template <>
    struct type_caster<Amulet::Bytes> {
        PYBIND11_TYPE_CASTER(Amulet::Bytes, io_name("bytes", "bytes"));

        static handle
        cast(const Amulet::Bytes& bytes, return_value_policy, handle)
        {
            auto* ptr = PyBytes_FromStringAndSize(bytes.data(), bytes.size());
            if (!ptr) {
                throw std::runtime_error("Could not allocate bytes object");
            }
            return ptr;
        }

        bool load(handle src, bool)
        {
            if (!PyBytes_Check(src.ptr())) {
                return false;
            }
            char* buffer = nullptr;
            Py_ssize_t length = 0;
            if (PyBytes_AsStringAndSize(src.ptr(), &buffer, &length) != 0) {
                throw error_already_set();
            }
            value = Amulet::Bytes(buffer, length);
            return true;
        }
    };

} // namespace detail
} // namespace pybind11
