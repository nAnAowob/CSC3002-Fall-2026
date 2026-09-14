#ifndef POINT_FREE_H
#define POINT_FREE_H

#include <iostream>

// A namespace lets both versions coexist in the same program.
namespace free_function {

// Arithmetic is component-wise; results must fit in int.
struct point {
    int x;
    int y;

    point(int x = 0, int y = 0);
    point(const point&) = default;

    // C++ requires assignment and conversion operators to be members.
    point& operator=(const point& rhs);
    // Only (0, 0) is false.
    explicit operator bool() const;
};

point operator+(point lhs, const point& rhs);
point operator-(point lhs, const point& rhs);
point operator*(point lhs, const point& rhs);
// Division truncates toward zero; a zero divisor coordinate throws
// std::domain_error. Failed division leaves the left operand unchanged.
point operator/(point lhs, const point& rhs);

// Prefix modifies both coordinates and returns a reference.
// Postfix's dummy int distinguishes it; it returns the old value.
point& operator++(point& p);
point operator++(point& p, int);
point& operator--(point& p);
point operator--(point& p, int);

bool operator==(const point& lhs, const point& rhs);
bool operator!=(const point& lhs, const point& rhs);

point& operator+=(point& lhs, const point& rhs);
point& operator-=(point& lhs, const point& rhs);
point& operator*=(point& lhs, const point& rhs);
point& operator/=(point& lhs, const point& rhs);

std::ostream& operator<<(std::ostream& out, const point& p);

} // namespace free_function

#endif // POINT_FREE_H