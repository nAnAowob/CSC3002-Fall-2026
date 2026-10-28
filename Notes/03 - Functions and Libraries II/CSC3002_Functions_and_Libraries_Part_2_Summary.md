# CSC3002 - Functions and Libraries II: Detailed Summary

> Based on [Lecture 3: Functions and Libraries Part 2](../../Lectures/3-CSC3002_Lecture%20Notes%20Functions%20and%20Libraries%20Part%202.pdf) (34 slides).
> Quick reference first, followed by explanations, examples, and a revision checklist. Examples clarify minor errors in the slides.

## Quick Reference

| Concept | Meaning / pattern |
|---|---|
| Client | Code that uses a library |
| Interface | Public contract: types, declarations, and documented behavior |
| Implementation | Code that fulfills the interface |
| Header guard | `#ifndef NAME_H`, `#define NAME_H`, `#endif` |
| Compile without linking | `g++ -c file.cpp -o file.o` |
| Create a static archive | `ar rcs libname.a file.o` |
| Export a constant | Header: `extern const double PI;`; one source definition with initializer |
| Private file-level helper | `static void helper();` |
| Persistent local state | `static bool initialized = false;` |
| `rand()` | Integer in `[0, RAND_MAX]` |
| `srand(seed)` | Set the pseudorandom generator's seed |
| Inclusive integer range | `[low, high]`, containing `high - low + 1` integers |
| Half-open real range | `[low, high)`, includes `low` but excludes `high` mathematically |

## 1. Libraries, Clients, and Abstraction (Slides 4-5, 11)

A library collects reusable functionality behind a well-defined interface. The **client** calls the library; the **implementer** supplies its behavior. The interface is both a communication channel and a boundary that hides implementation details.

For example, a client should be able to call `randomInteger(1, 6)` without understanding the generator's internal state. Reuse avoids implementing the same operations repeatedly; abstraction lets clients work with meaningful operations instead of low-level mechanisms.

## 2. Compilation and Linking (Slides 6-7)

The conceptual pipeline is:

```text
.cpp source + included headers -> compiler -> .o object file
object files + library files   -> linker   -> executable
object files                  -> archiver -> static library
```

Preprocessing handles `#include` and conditional directives before compilation. A header supplies declarations; it does not automatically supply separately compiled function definitions to the linker.

```sh
# Compile the implementation without linking.
g++ -c direction.cpp -o direction.o
# Bundle object code into a static archive.
ar rcs libdirection.a direction.o
# Link a client against the archive.
g++ DirDemo.cpp -L. -ldirection -o main
```

Here `-L.` adds the current directory to the library search path, and `-ldirection` selects a library named `libdirection`. Alternatively, name the archive directly. The slides use `dir.lib`; `.a` is the usual Unix static-library convention. For `ar rcs`, `r` replaces/adds members, `c` creates the archive, and `s` writes its symbol index.

A missing declaration commonly causes a compiler error. A declared function whose definition was not linked commonly causes an undefined-symbol linker error.

## 3. Standard Libraries and `<cmath>` (Slides 8-10)

C++ supports much C code and exposes adapted C libraries, but it is not a perfectly compatible superset of C. Standard-library names generally live in `std`.

| Category | Examples |
|---|---|
| Containers | `<vector>`, `<queue>`, `<stack>`, `<map>`, `<set>` |
| General utilities | `<algorithm>`, `<functional>`, `<iterator>`, `<memory>` |
| Text and I/O | `<string>`, `<iostream>`, `<fstream>`, `<sstream>` |
| Adapted C libraries | `<cmath>`, `<cctype>`, `<cstring>`, `<cstdio>`, `<cstdlib>` |
| Other facilities | Numerics, localization, language support, threads |

| `<cmath>` function | Meaning |
|---|---|
| `std::abs(x)` | Absolute value |
| `std::sqrt(x)` | Square root |
| `std::floor(x)` | Largest integer value no greater than `x` |
| `std::ceil(x)` | Smallest integer value no less than `x` |
| `std::exp(x)` | `e` raised to `x` |
| `std::log(x)`, `std::log10(x)` | Natural and base-10 logarithms |
| `std::pow(x, y)` | `x` raised to `y` |
| `std::sin(t)`, `std::cos(t)`, `std::tan(t)` | Trigonometric functions; angle in radians |
| `std::atan(x)` | Principal arctangent |
| `std::atan2(y, x)` | Angle using both coordinates, preserving quadrant information |

`floor(-2.3)` is `-3`, whereas converting `-2.3` to `int` gives `-2` (truncation toward zero).

## 4. Header and Implementation Design (Slides 12-13)

A small error-reporting library illustrates the separation.

**`error.h`:**

```cpp
#ifndef CSC3002_ERROR_H
#define CSC3002_ERROR_H
#include <string>

// Print a message to standard error and terminate with failure.
void error(std::string msg);
#endif
```

**`error.cpp`:**

```cpp
#include "error.h"
#include <cstdlib>
#include <iostream>

void error(std::string msg) {
    std::cerr << msg << '\n';
    std::exit(EXIT_FAILURE);
}
```

- Guards prevent repeated inclusion within one translation unit; they do not solve multiple definitions across separate source files.
- Include the library's own header in its implementation so declaration/definition mismatches are detected.
- A header should include what its declarations require. `error.h` needs `<string>` even if one client happens to include it first.
- Avoid `using namespace std;` in headers because it affects every including client. Use `std::string`, `std::ostream`, etc.
- Put ordinary non-inline function definitions in a `.cpp` file. Templates are an important exception covered in Lecture 9.

## 5. Exporting Types: `Direction` (Slides 14-19)

```cpp
enum Direction { NORTH, EAST, SOUTH, WEST };
```

The enumerators have values `0`, `1`, `2`, and `3`. An interface can export this type together with operations:

```cpp
Direction leftFrom(Direction dir) {
    return static_cast<Direction>((dir + 3) % 4);
}
Direction rightFrom(Direction dir) {
    return static_cast<Direction>((dir + 1) % 4);
}
```

Adding `3` makes a left turn without a negative remainder: `leftFrom(NORTH)` becomes `WEST`; `rightFrom(WEST)` becomes `NORTH`.

```cpp
#include <ostream>
#include <string>

std::string directionToString(Direction dir) {
    switch (dir) {
        case NORTH: return "NORTH";
        case EAST:  return "EAST";
        case SOUTH: return "SOUTH";
        case WEST:  return "WEST";
        default:    return "???";
    }
}

std::ostream& operator<<(std::ostream& os, Direction dir) {
    return os << directionToString(dir);
}
```

Returning the same stream by reference supports chaining: `std::cout << dir << '\n';`.

### Prefix versus postfix increment

Prefix `++dir` yields the updated value; postfix `dir++` yields the old value. The extra `int` parameter marks the postfix overload; it is not an ordinary client-supplied argument.

A **cyclic** version is:

```cpp
Direction& operator++(Direction& dir) {
    dir = rightFrom(dir);
    return dir;
}
Direction operator++(Direction& dir, int) {
    Direction old = dir;
    ++dir;
    return old;
}
```

**Slide caution:** slide 19 increments without wrapping so a loop can pass `WEST`. Converting `4` to the shown unfixed enum is outside its valid representable range and should not be relied on. Conversely, making increment cyclic means `dir <= WEST` never becomes false. Use an integer counter for exactly four directions:

```cpp
for (int i = 0; i < 4; ++i) {
    Direction dir = static_cast<Direction>(i);
    // Process dir.
}
```

## 6. Exporting Constants and Degree-Based Math (Slides 20-22)

An ordinary namespace-scope `const` variable generally has internal linkage. To share one constant across source files, declare it in a header and define it once:

```cpp
// gmath.h
extern const double PI;
double toRadians(double degrees);
double toDegrees(double radians);
```

```cpp
// gmath.cpp (also includes gmath.h)
extern const double PI = 3.14159265358979323846;

double toRadians(double degrees) { return degrees * PI / 180; }
double toDegrees(double radians) { return radians * 180 / PI; }
```

Degree-based wrappers call `std::sin(toRadians(angle))` or `std::cos(toRadians(angle))`. The declaration without an initializer announces the object; the definition allocates it and supplies its value. Do not put that initialized `extern` definition in a header included by multiple source files.

## 7. Five Principles of Interface Design (Slide 23)

| Principle | Design question |
|---|---|
| Unified | Do the operations belong to one coherent abstraction? |
| Simple | Does the interface hide unnecessary complexity? |
| Sufficient | Can clients perform the operations they need? |
| General | Is it useful to several clients and situations? |
| Stable | Can implementation changes preserve existing client behavior? |

## 8. Designing a Random Number Library (Slides 24-28)

A pseudorandom generator uses a deterministic process whose results appear random. The same seed reproduces the same sequence for a given implementation, which is useful for debugging. Time-based seeding allows different runs to begin differently, though runs started at the same clock resolution may share a seed.

| Public function | Contract |
|---|---|
| `randomInteger(low, high)` | Integer from `low` through `high`, inclusive |
| `randomReal(low, high)` | Real value intended to lie in `[low, high)` |
| `randomChance(p)` | Boolean event with probability `p`; require `0 <= p <= 1` |
| `randomBool()` | Boolean event with probability `0.5` |
| `setRandomSeed(seed)` | Choose a reproducible starting state |

These functions are a course library interface, not standard C++ functions. Assume valid ordered bounds for the examples below.

## 9. Random Library Implementation (Slides 29-34)

### Normalize, scale, translate

```cpp
// Requires <cstdlib>, <cmath>, and an initRandomSeed declaration.
int randomInteger(int low, int high) {
    initRandomSeed();
    double d = std::rand() / (double(RAND_MAX) + 1);
    double s = d * (double(high) - low + 1);
    return int(std::floor(low + s));
}

double randomReal(double low, double high) {
    initRandomSeed();
    double d = std::rand() / (double(RAND_MAX) + 1);
    return low + d * (high - low);
}

bool randomChance(double p) { return randomReal(0, 1) < p; }
bool randomBool() { return randomChance(0.5); }
```

For a die, the integer mapping is `floor(1 + d * 6)`, giving `1` through `6` mathematically.

1. Floating-point division avoids integer truncation to zero.
2. Dividing by `RAND_MAX + 1.0` makes the normalized result less than one mathematically.
3. Integer bounds require a width of `high - low + 1`; real bounds use `high - low`.
4. Convert before addition/subtraction to avoid overflowing those intermediate integer expressions.
5. `floor` handles negative ranges correctly; a direct integer cast truncates toward zero.

These are the lecture's teaching formulas. Finite generator resolution can make integer outcomes slightly biased or unreachable for very large ranges, and floating-point rounding can affect endpoints. They are not a general guarantee of perfectly uniform sampling over arbitrary bounds.

### Initialize once; allow explicit reseeding

```cpp
#include <cstdlib>
#include <ctime>

static void initRandomSeed() {
    static bool initialized = false;
    if (!initialized) {
        std::srand(static_cast<unsigned int>(std::time(nullptr)));
        initialized = true;
    }
}

void setRandomSeed(int seed) {
    initRandomSeed();
    std::srand(static_cast<unsigned int>(seed));
}
```

The function-level `static` gives the helper internal linkage. The local `static` variable retains its value across calls. `setRandomSeed` first marks initialization complete, then installs the requested seed; later random calls therefore do not overwrite it with a time-based seed. Repeatedly reseeding before each draw can restart the sequence and undermine the intended behavior.

## 10. Revision Checklist

- Explain client, interface, implementation, compiler, linker, and archiver.
- Write a guarded header that includes its own dependencies.
- Distinguish declarations from definitions and compile errors from link errors.
- Trace compass turns and explain prefix/postfix return values.
- Export a constant with one definition and use radians correctly.
- State the five interface-design principles.
- Derive the integer and real range mappings, including endpoint differences.
- Explain both uses of `static` and why explicit seeding remains effective.
- Know that repeated seeds reproduce sequences, not that every platform produces the same sequence.
