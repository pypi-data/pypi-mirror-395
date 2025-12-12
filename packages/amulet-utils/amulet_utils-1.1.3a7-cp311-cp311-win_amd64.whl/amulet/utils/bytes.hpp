#pragma once

#include <string>

namespace Amulet {

// A subclass of std::string to simplify casting to Python.
class Bytes : public std::string {
public:
    template <typename... Args>
    Bytes(Args&&... args)
        : std::string(std::forward<Args>(args)...)
    {
    }

    template <typename... Args>
    Bytes& operator=(Args&&... args)
    {
        std::string::operator=(std::forward<Args>(args)...);
        return *this;
    }
};

} // namespace Amulet
