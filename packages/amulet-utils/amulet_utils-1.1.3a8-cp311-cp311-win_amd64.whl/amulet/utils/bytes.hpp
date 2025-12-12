#pragma once

#include <string>

namespace Amulet {

// A subclass of std::string to simplify casting to Python.
class Bytes : public std::string {
public:
    template <typename... Args>
        requires std::constructible_from<std::string, Args...>
    Bytes(Args&&... args)
        : std::string(std::forward<Args>(args)...)
    {
    }

    template <typename Arg>
        requires std::assignable_from<std::string&, Arg>
    Bytes& operator=(Arg&& arg)
    {
        std::string::operator=(std::forward<Arg>(arg));
        return *this;
    }
};

} // namespace Amulet
