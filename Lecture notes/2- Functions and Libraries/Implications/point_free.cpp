#include "point_free.h"

#include <ostream>
#include <stdexcept>

namespace free_function {

point::point(int x, int y) : x(x), y(y) {}

point& point::operator=(const point& rhs) {
    x = rhs.x;
    y = rhs.y;
    return *this;
}

point::operator bool() const {
    return x != 0 || y != 0;
}

// lhs is a copy, so binary arithmetic leaves its operands unchanged.
point operator+(point lhs, const point& rhs) {
    return lhs += rhs;
}

point operator-(point lhs, const point& rhs) {
    return lhs -= rhs;
}

point operator*(point lhs, const point& rhs) {
    return lhs *= rhs;
}

point operator/(point lhs, const point& rhs) {
    return lhs /= rhs;
}

point& operator++(point& p) {
    ++p.x;
    ++p.y;
    return p;
}

point operator++(point& p, int) {
    point previous(p);
    ++p;
    return previous;
}

point& operator--(point& p) {
    --p.x;
    --p.y;
    return p;
}

point operator--(point& p, int) {
    point previous(p);
    --p;
    return previous;
}

bool operator==(const point& lhs, const point& rhs) {
    return lhs.x == rhs.x && lhs.y == rhs.y;
}

bool operator!=(const point& lhs, const point& rhs) {
    return !(lhs == rhs);
}

point& operator+=(point& lhs, const point& rhs) {
    lhs.x += rhs.x;
    lhs.y += rhs.y;
    return lhs;
}

point& operator-=(point& lhs, const point& rhs) {
    lhs.x -= rhs.x;
    lhs.y -= rhs.y;
    return lhs;
}

point& operator*=(point& lhs, const point& rhs) {
    lhs.x *= rhs.x;
    lhs.y *= rhs.y;
    return lhs;
}

point& operator/=(point& lhs, const point& rhs) {
    if (rhs.x == 0 || rhs.y == 0) {
        throw std::domain_error("point division requires nonzero divisor coordinates");
    }
    lhs.x /= rhs.x;
    lhs.y /= rhs.y;
    return lhs;
}

std::ostream& operator<<(std::ostream& out, const point& p) {
    return out << '(' << p.x << ", " << p.y << ')';
}

} // namespace free_function