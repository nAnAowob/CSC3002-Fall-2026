#include "point_free.h"

#include <cassert>
#include <iostream>
#include <sstream>
#include <stdexcept>

int main() {
    using free_function::point;

    // Operators are found through argument-dependent lookup (ADL).
    const point a(12, 18);
    const point b(3, 6);

    std::cout << "a = " << a << ", b = " << b << '\n'
              << "a + b = " << a + b << '\n'
              << "a - b = " << a - b << '\n'
              << "a * b = " << a * b << '\n'
              << "a / b = " << a / b << '\n';
    // Free operators can also be called explicitly as ordinary functions.
    assert(free_function::operator+(a, b) == point(15, 24));
    assert(a + b == point(15, 24));
    assert(a - b == point(9, 12));
    assert(a * b == point(36, 108));
    assert(a / b == point(4, 3));
    assert(point(-7, 7) / point(2, 2) == point(-3, 3));

    std::cout << std::boolalpha
              << "bool(a) = " << static_cast<bool>(a) << '\n'
              << "bool(point()) = " << static_cast<bool>(point()) << '\n'
              << "a != b = " << (a != b) << '\n';
    assert(!point());
    assert(point(0, 5));
    assert(point(5, 0));
    assert(a != b);
    assert(!(a != a));
    if (a) {
        std::cout << "a has at least one nonzero coordinate\n";
    }

    point p;
    p = a;
    assert(p == a);
    std::cout << "p = a: " << p << '\n';

    point old = p++;
    assert(old == a && p == point(13, 19));
    std::cout << "p++ returned " << old << ", p is now " << p << '\n';
    point& incremented = ++p;
    assert(&incremented == &p);
    assert(p == point(14, 20));
    std::cout << "After ++p: " << p << '\n';
    old = p--;
    assert(old == point(14, 20) && p == point(13, 19));
    std::cout << "p-- returned " << old << ", p is now " << p << '\n';
    --p;
    assert(p == a);
    std::cout << "After --p: " << p << '\n';

    p += b;
    assert(p == point(15, 24));
    std::cout << "After p += b: " << p << '\n';
    p -= b;
    assert(p == a);
    std::cout << "After p -= b: " << p << '\n';
    p *= b;
    assert(p == point(36, 108));
    std::cout << "After p *= b: " << p << '\n';
    p /= b;
    assert(p == a);
    std::cout << "After p /= b: " << p << '\n';

    // Check that failed division leaves p unchanged.
    for (const point divisor : {point(0, 1), point(1, 0)}) {
        bool threw = false;
        try {
            p /= divisor;
        } catch (const std::domain_error& error) {
            threw = true;
            std::cout << "Caught: " << error.what() << '\n';
        }
        assert(threw && p == a);
    }

    std::ostringstream output;
    output << a << ' ' << b;
    assert(output.str() == "(12, 18) (3, 6)");
    std::cout << "All checks passed.\n";
}