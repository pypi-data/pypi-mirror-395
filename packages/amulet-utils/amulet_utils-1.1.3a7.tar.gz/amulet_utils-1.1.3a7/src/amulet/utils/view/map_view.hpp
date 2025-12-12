#pragma once

namespace Amulet {

// There are some cases where I want to expose a const view to a map of smart pointers.
// Const does not carry to the pointed object so this is a workaround.

template <typename MapT, typename VT>
class MapViewIterator {
    static_assert(
        std::is_convertible_v<typename MapT::mapped_type, VT>,
        "MapView: VT must be convertible from MapT::mapped_type");

public:
    using value_type = std::pair<typename MapT::key_type, VT>;

private:
    typename MapT::const_iterator _it;
    mutable value_type _value;

public:
    MapViewIterator(typename MapT::const_iterator it)
        : _it(it)
    {
    }

    value_type operator*() const
    {
        return { _it->first, _it->second };
    }

    const value_type* operator->() const
    {
        _value = operator*();
        return &_value;
    }

    MapViewIterator& operator++()
    {
        ++_it;
        return *this;
    }

    MapViewIterator operator++(int)
    {
        MapViewIterator tmp = *this;
        ++_it;
        return tmp;
    }

    bool operator==(const MapViewIterator& other) const
    {
        return _it == other._it;
    }

    bool operator!=(const MapViewIterator& other) const
    {
        return !(*this == other);
    }
};

template <typename MapT, typename VT>
class MapView {
    static_assert(
        std::is_convertible_v<typename MapT::mapped_type, VT>,
        "MapView: VT must be convertible from MapT::mapped_type");

private:
    const MapT& _map;

public:
    using iterator = MapViewIterator<MapT, VT>;
    using const_iterator = MapViewIterator<MapT, VT>;

    MapView(const MapT& map)
        : _map(map)
    {
    }

    template <typename... Args>
    VT at(Args&&... args) const
    {
        return _map.at(std::forward<Args>(args)...);
    }

    MapViewIterator<MapT, VT> begin() const
    {
        return _map.begin();
    }

    MapViewIterator<MapT, VT> end() const
    {
        return _map.end();
    }

    bool empty() const
    {
        return _map.empty();
    }

    typename MapT::size_type size() const
    {
        return _map.size();
    }

    typename MapT::size_type max_size() const
    {
        return _map.max_size();
    }

    template <typename... Args>
    typename MapT::size_type count(Args&&... args) const
    {
        return _map.count(std::forward<Args>(args)...);
    }

    template <typename... Args>
    MapViewIterator<MapT, VT> find(Args&&... args) const
    {
        return _map.find(std::forward<Args>(args)...);
    }

    template <typename... Args>
    bool contains(Args&&... args) const
    {
        return _map.contains(std::forward<Args>(args)...);
    }
};

} // namespace Amulet
