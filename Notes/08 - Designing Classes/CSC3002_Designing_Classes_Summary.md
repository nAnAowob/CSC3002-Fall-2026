# CSC3002 - Designing Classes: Detailed Summary

> Based on [Lecture 8: Designing Classes](../../Lectures/8-CSC3002_Designing%20Classes%281%29.pdf) (58 slides).
> Examples are condensed and corrected for study. Differences from the slides are identified where they affect behavior.

## Quick Reference

| Feature | Pattern / meaning |
|---|---|
| Class / object | Type definition / instance of that type |
| `public` | Accessible to clients |
| `private` | Accessible to class members and friends |
| `protected` | Also accessible to derived-class members, subject to protected-access rules |
| Constructor | `Point(int x, int y);` - same name as class, no return type |
| Initializer list | `Point(int a, int b) : x(a), y(b) {}` |
| Const member function | `int getX() const;` - cannot normally modify object state |
| Copy constructor | `Point(const Point& src);` |
| Copy assignment | `Point& operator=(const Point& src);` |
| Destructor | `~Point();` - cleanup at end of lifetime |
| `this` / `*this` | Pointer to current object / current object itself |
| Friend | Nonmember or other class explicitly granted private access |
| Pure virtual function | `virtual double calcArea() const = 0;` |
| Public inheritance | `class Rectangle : public BaseShape { ... };` |

## 1. Types, Structures, Classes, and Objects (Slides 3-16)

Primitive types include `int`, `double`, `bool`, and `char`. Compound types combine or organize values: enums name alternatives; structures/classes combine fields and operations.

```cpp
enum Direction { NORTH, EAST, SOUTH, WEST }; // 0, 1, 2, 3
enum Coin { PENNY = 1, NICKEL = 5, DIME = 10, QUARTER = 25 };

struct PointData {
    int x;
    int y;
};
PointData pt{3, 4}; // defines an object; the struct above defines a type
```

In C++, both `struct` and `class` support methods, constructors, destructors, inheritance, and access control. Their key language differences are defaults: `struct` has public member access and public inheritance; `class` has private member access and private inheritance. A C structure does not have these C++ object-oriented facilities.

A class combines **representation** (fields) and **behavior** (methods). Creating an object is instantiation. Encapsulation restricts access to the representation so the class can enforce its rules.

## 2. Interfaces, Methods, Getters, and Setters (Slides 15-19)

Class declarations commonly go in a header; ordinary method definitions go in a `.cpp` file. The scope-resolution operator connects a definition to its class:

```cpp
// Inside the class: int getX() const;
// Outside the class:
// int Point::getX() const { return x; }
```

An accessor/getter reads state; a mutator/setter changes it. Making fields private and then exposing unrestricted setters may lose much of the benefit. Supply only operations clients need, and validate changes when the class has invariants.

An immutable design exposes no operations that change its logical value after construction. Private fields alone do not make an object immutable.

### A compact `Point` example

```cpp
#include <cmath>
#include <ostream>

class Point {
public:
    Point(int xx = 0, int yy = 0) : x(xx), y(yy) {}
    int getX() const { return x; }
    int getY() const { return y; }
    double length() const {
        return std::hypot(double(x), double(y));
    }
    double length(const Point& p) const {
        return std::hypot(double(p.x) - x, double(p.y) - y);
    }
    Point operator+(const Point& p) const {
        return Point(x + p.x, y + p.y);
    }
    bool operator==(const Point& p) const {
        return x == p.x && y == p.y;
    }
    friend std::ostream& operator<<(std::ostream& os, const Point& p) {
        return os << '[' << p.x << ',' << p.y << ']';
    }
private:
    int x;
    int y;
};
```

`Point p(3, 4);` has distance `5` from the origin. An overloaded `length(q)` computes the distance to another point. `std::hypot` expresses the slides' square-root formula directly.

**Slide behavior versus conventional behavior:** slides 9 and 32 define `operator+` to modify the left operand and return it by reference. Trace that exact behavior if given that code. The example above uses the usual arithmetic convention: `a + b` produces a new point; a mutating addition would normally be named `operator+=`.

## 3. Constructors and Initializer Lists (Slides 20, 29-31)

Constructors establish valid initial state. They can be overloaded by parameter list and have no return type, not even `void`.

```cpp
Point a;        // default arguments initialize (0, 0)
Point b(3, 4);  // initialize (3, 4)
Point c = b;   // copy construction
```

A default constructor is callable with no arguments. If no constructor is user-declared, the compiler may implicitly declare one; it can be deleted if members cannot be initialized. Declaring a parameterized constructor does not automatically provide a separate no-argument constructor.

An initializer list initializes members before the constructor body. It is required for reference members and for const members without another initializer, and it selects base-class constructors. Members initialize in **declaration order**, regardless of list order.

```cpp
class LabelledPoint {
public:
    LabelledPoint(int idValue, int xx) : id(idValue), x(xx) {}
private:
    const int id;
    int x;
};
```

**Clarification:** an initializer list initializes a constant; it does not reinitialize it later. Uninitialized built-in members do not automatically receive zero merely because the constructor has a body.

## 4. Copy Construction versus Assignment (Slides 21-25)

```cpp
Point a(3, 4);
Point b = a; // new object: copy constructor
Point c;
c = a;      // existing object: copy assignment
```

Passing by value can copy an object; passing by `const T&` avoids that parameter copy and prevents ordinary mutation through the reference. Returning by value may use copying, moving, or copy elision.

The conventional signatures are:

```cpp
// Declarations inside class T:
// T(const T& src);
// T& operator=(const T& src);
```

Assignment returns `*this` by reference so expressions such as `a = b = c` work naturally.

### Shallow and deep copying

For a raw owning pointer, compiler-generated copying copies the address, not the allocation:

```text
Shallow: original.array ----> [10, 20, 30] <---- copy.array
Deep:    original.array ----> [10, 20, 30]
         copy.array     ----> [10, 20, 30]  (separate allocation)
```

If both objects delete the same allocation, destruction causes a double deletion; modifying one object's array may unexpectedly affect the other.

**Important qualification:** default copying is memberwise. Members such as `std::string` and `std::vector` already implement appropriate value copying. A class containing only integers, like `Point`, normally needs no custom copying. The slide warning concerns raw resource ownership, not all classes or `std::vector` itself.

## 5. Stack Ownership and Safe Deep Copying (Slides 26-28)

A stack is **LIFO**: last in, first out. `push` adds the top element; `pop` removes it. An array-based implementation stores an allocation, a capacity, and an element count.

For a raw-memory owner, consider the **Rule of Three**: destructor, copy constructor, and copy assignment usually need coordinated implementations. This compact ownership example deliberately omits the stack operations to focus on copying:

```cpp
class CharStorage {
public:
    CharStorage() : array(new char[10]), capacity(10), count(0) {}

    CharStorage(const CharStorage& src)
        : array(new char[src.capacity]),
          capacity(src.capacity), count(src.count) {
        for (int i = 0; i < count; ++i) array[i] = src.array[i];
    }

    CharStorage& operator=(const CharStorage& src) {
        if (this != &src) {
            // Allocate before deleting: allocation failure preserves this object.
            char* replacement = new char[src.capacity];
            for (int i = 0; i < src.count; ++i)
                replacement[i] = src.array[i];
            delete[] array;
            array = replacement;
            capacity = src.capacity;
            count = src.count;
        }
        return *this;
    }

    ~CharStorage() { delete[] array; }

private:
    char* array;
    int capacity;
    int count;
};
```

**Slide correction:** slide 28 calls `clear()` inside `deepCopy()`, including from a copy constructor that has not initialized `array`. Reading or deleting that uninitialized pointer is invalid. Initialize members first or allocate directly as above. Copy construction starts with a new object; assignment must also account for existing storage and self-assignment.

If copying is forbidden, modern C++ can state this explicitly:

```cpp
// Inside the owning class:
// CharStorage(const CharStorage&) = delete;
// CharStorage& operator=(const CharStorage&) = delete;
```

The slides show the older approach of declaring copy operations private. Using a standard container for ownership often removes the need to implement these operations manually.

## 6. Operator Overloading and Friends (Slides 31-39)

Operators are functions whose names begin with `operator`. Overloading gives existing operators meanings for user-defined types; it does not change their precedence or number of operands.

| Style | Binary operation `a == b` | Private access |
|---|---|---|
| Member | `a.operator==(b)`; `a` is `*this` | Member can access private fields |
| Free function | `operator==(a, b)` | Use public methods or declare it a friend |

A friend remains a nonmember; friendship grants access but does not make the function a method. A free function using only getters does not need friendship.

### Stream insertion

```cpp
// Typical signature:
// std::ostream& operator<<(std::ostream& os, const Point& p);
```

The left operand is a stream, so insertion is normally a nonmember. Streams cannot be copied; take the stream by reference and return the same stream by reference for chaining. Taking the point by const reference avoids a copy and accepts const objects. In the slides, friendship permits calling the private `toString()` helper, which constructs text using `std::ostringstream`.

### Prefix, postfix, and Boolean conversion

Conventional member declarations are:

```cpp
// Point& operator++();   // ++p: update and return this object
// Point operator++(int); // p++: save old value, update, return old value
```

The slides return prefix results by value; the reference return above is conventional. Prefix/postfix decrement follows the same distinction. The dummy `int` distinguishes postfix syntax.

Slide 31 defines:

```cpp
// explicit operator bool() const { return x != 0 && y != 0; }
```

Under that definition, both coordinates must be nonzero: `(1, 0)` is false. `explicit` permits contextual Boolean use such as `if (p)` without allowing arbitrary implicit conversions through `bool`.

## 7. Inheritance, Virtual Functions, and Abstract Classes (Slides 41-47, 55-57)

The slides organize shapes as:

```text
BaseShape
├── Ellipse
│   └── Circle
└── Rectangle
    └── Square
```

Public inheritance models an "is-a" relationship. A derived constructor can initialize its base using an initializer list, such as a square passing equal width and height to `Rectangle`.

A virtual method supports runtime dispatch through a base pointer or reference. A pure virtual method uses `= 0`; a class with an unimplemented pure virtual function is abstract and cannot be instantiated directly.

```cpp
class BaseShape {
public:
    virtual double calcArea() const = 0;
    virtual ~BaseShape() = default;
};

class Rectangle : public BaseShape {
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    double calcArea() const override { return width * height; }
private:
    double width, height;
};

// Rectangle rect(3, 4);
// BaseShape& shape = rect;
// shape.calcArea() returns 12 using Rectangle's implementation.
```

`override` asks the compiler to verify that the signature overrides a base virtual method. Virtual dispatch remains virtual in subclasses even if they omit the `virtual` keyword. Use a virtual destructor when deleting derived objects through a base pointer. The slides declare a pure virtual destructor; such a destructor still requires a definition because base destruction occurs during derived-object cleanup.

### Inheritance access

| Inheritance mode | Base public members become | Base protected members become |
|---|---|---|
| `public` | Public | Protected |
| `protected` | Protected | Protected |
| `private` | Private | Private |

Base private members remain inaccessible directly to the derived class; they still exist in its base subobject. Access them through permitted base operations.

The lecture names single inheritance (one base), multilevel inheritance (a chain), multiple inheritance (several bases), hierarchical inheritance (several children), and hybrid inheritance (combinations).

**Polymorphism:** overloading chooses among signatures at compile time. Virtual overriding chooses the implementation at runtime according to the object's dynamic type. A nonvirtual method does not gain runtime dispatch merely because a derived class uses the same name.

## 8. Rational Numbers and Invariants (Slides 48-49)

A rational number represents `numerator / denominator` using integers. This can preserve exact fractions such as `1/3` that floating-point values approximate, subject to the integer representation's finite range.

Constructors support zero arguments (`0/1`), one integer (`n/1`), or two integers (`n/d`). A valid representation should ensure:

- The denominator is nonzero and positive.
- Numerator and denominator are reduced by their greatest common divisor.
- Zero is represented as `0/1`.

For example, `6/-8` normalizes to `-3/4`. These conditions are **invariants**: rules maintained by constructors and every operation.

| Operation | Formula |
|---|---|
| `a/b + c/d` | `(ad + bc) / bd` |
| `a/b - c/d` | `(ad - bc) / bd` |
| `a/b * c/d` | `ac / bd` |
| `(a/b) / (c/d)` | `ad / bc`, requiring `c != 0` |

Arithmetic operators return normalized results. Intermediate integer products can overflow, so exact rational arithmetic does not mean unlimited precision.

## 9. TokenScanner Interface (Slides 50-52)

A token is a meaningful unit of input, such as a word, operator, number, or quoted string. Token boundaries depend on the application. The lecture's `TokenScanner` is from the Stanford library, not the C++ Standard Library.

| Method | Purpose |
|---|---|
| `setInput(str)` / `setInput(stream)` | Choose the input source |
| `hasMoreTokens()` | Test whether another token exists |
| `nextToken()` | Return next token, or an empty string at the end |
| `saveToken(token)` | Put a token back for the next read |
| `ignoreWhitespace()` | Skip whitespace tokens |
| `scanNumbers()` | Group numbers into single tokens |
| `scanStrings()` | Group quoted strings into single tokens |

```cpp
// With the course library available:
// TokenScanner scanner;
// scanner.setInput(source);
// scanner.ignoreWhitespace();
// while (scanner.hasMoreTokens()) {
//     std::string token = scanner.nextToken();
//     // Process token.
// }
```

The interface hides scanning details while exposing configuration that different clients need.

## 10. Designing and Encapsulating a Program (Slides 40, 53-54)

Start with client use cases, choose private state, define constructors that establish invariants, and provide public operations that maintain them. Add friends only when the design needs their access. Implement the class and exercise it as a client would.

Encapsulating related program functions as methods lets them share private instance state without global variables or long parameter lists. This is useful when the data and behavior form a coherent object.

## 11. Revision Checklist

- Explain C structures versus C++ structs and classes, including access defaults.
- Distinguish a type, an object, and an object's private state.
- Write constructor initializer lists and identify actual initialization order.
- Decide whether code uses copy construction or assignment.
- Draw shallow/deep copy diagrams and identify double-deletion risks.
- Explain why the slide's uninitialized-pointer copy helper needs correction.
- Trace member/free operators, `this`, stream chaining, and prefix/postfix values.
- Distinguish overloading, overriding, and virtual dispatch.
- Apply the inheritance access table and identify abstract classes.
- Normalize rational values and explain the TokenScanner client loop.
