#include "temp.hpp"

#include <chrono>
#include <cstdlib>
#include <filesystem>
#include <mutex>

#include "lock_file.hpp"

namespace Amulet {

std::filesystem::path& _get_temp_dir()
{
    static std::filesystem::path _temp_dir = "";
    return _temp_dir;
}

std::mutex& _get_temp_dir_mutex()
{
    static std::mutex _temp_dir_mutex;
    return _temp_dir_mutex;
}

static void clean_temp_dir(const std::filesystem::path& temp_dir)
{
    for (const auto& group : std::filesystem::directory_iterator(temp_dir)) {
        if (!group.is_directory()) {
            continue;
        }
        for (const auto& dir : std::filesystem::directory_iterator(group.path())) {
            if (!dir.path().filename().string().starts_with("amulettmp-")) {
                continue;
            }
            try {
                Amulet::LockFile lock(dir.path() / "lock");
            } catch (const std::runtime_error&) {
                continue;
            }
            std::filesystem::remove_all(dir.path());
        }
    }
};

std::filesystem::path get_temp_dir()
{
    std::lock_guard lock(_get_temp_dir_mutex());
    auto& temp_dir = _get_temp_dir();
    if (temp_dir.empty()) {
        throw std::runtime_error("Temporary directory has not been set.");
    }
    return temp_dir;
}

void set_temp_dir(std::filesystem::path path)
{
    if (!std::filesystem::is_directory(path)) {
        throw std::runtime_error("Temporary path is not a directory.");
    }
    std::lock_guard lock(_get_temp_dir_mutex());
    auto& temp_dir = _get_temp_dir();
    if (!temp_dir.empty()) {
        clean_temp_dir(temp_dir);
    }
    temp_dir = std::move(path);
    clean_temp_dir(temp_dir);
}

TempDir::TempDir(const std::string& group)
{
    auto time = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::system_clock::now().time_since_epoch())
                    .count();
    for (size_t i = 0; i < 100; i++) {
        auto path = get_temp_dir() / group / ("amulettmp-" + std::to_string(time) + "-" + std::to_string(i));
        std::filesystem::create_directories(path);
        try {
            _lock = std::make_unique<Amulet::LockFile>(path / "lock");
        } catch (const std::runtime_error&) {
            continue;
        }
        _path = path;
        return;
    }
    throw std::runtime_error("Could not create temporary directory.");
}

TempDir::TempDir(TempDir&&) = default;
TempDir& TempDir::operator=(TempDir&&) = default;

TempDir::~TempDir()
{
    _lock.reset();
    std::filesystem::remove_all(_path);
}

const std::filesystem::path& TempDir::get_path() const
{
    return _path;
}

} // namespace Amulet
