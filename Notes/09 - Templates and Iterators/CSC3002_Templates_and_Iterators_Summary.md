# CSC3002 - Templates and Iterators: Detailed Summary

> Based on [Lecture 9: Template and Iterator](../../Lectures/9-CSC3002_Template%20and%20Iterator.pdf) (22 slides).
> Includes worked exercise answers and explicit corrections to iterator examples. `Vector`/`Stack` in the slides refer to teaching classes; standard containers use names such as `std::vector`.

## Quick Reference

| Feature | Pattern / key rule |
|---|---|
| One type parameter | `template <typename T>` |
| Several type parameters | `template <typename T, typename U>` |
| Generic class instance | `Stack<int> s;` |
| Out-of-class method | `template <typename T> void Stack<T>::push(T value) { ... }` |
| Template visibility | Definitions usually live in the header so instantiation can see them |
| First element | `container.begin()` |
| Past-the-end position | `container.end()`; never dereference it |
| Current element | `*it` |
| Move forward | `++it` |
| Standard traversal | `for (auto it = c.begin(); it != c.end(); ++it)` |
| Range loop with copies | `for (auto x : c)` |
| Range loop with mutation | `for (auto& x : c)` |
| Range loop without copies | `for (const auto& x : c)` |
| Reverse traversal | `rbegin()` to `rend()` where supported |

## 1. From Overloading to Templates (Slides 3-6)

Function overloading gives several functions one name but different parameter lists. The compiler selects a viable overload using argument types and conversion rules; return type alone cannot distinguish overloads.

```cpp
int operate(int a, int b) { return a / b; }
double operate(double a, double b) { return a / b; }

// operate(1, 2)     -> 0   (integer division)
// operate(1.0, 2.0) -> 0.5 (floating-point division)
```

When the algorithm is identical except for types, a template expresses the shared pattern:

```cpp
template <typename T>
T Max(T a, T b) {
    return (a > b) ? a : b;
}
```

`typename` and `class` are interchangeable when declaring a type template parameter. A template is a pattern from which the compiler instantiates functions or classes for the types used by the program.

```cpp
// Max(1, 2)     instantiates an int version.
// Max(1.0, 2.0) instantiates a double version.
// Max('A', 'Z') returns 'Z' in the lecture's character encoding.
```

Templates preserve type-specific semantics: replacing the two `operate` overloads with one template does not change integer division into floating-point division.

## 2. Type Requirements and Deduction (Slides 7-8)

The `Max` implementation requires `>` to be meaningful for its type, along with the copying/return operations it uses. Instantiating it for a class without an appropriate comparison produces a compile-time error.

- `std::string` has lexicographic comparison, so string objects work.
- A `Point` needs a defined `operator>`; C++ has no universal ordering for points.
- The outcome of comparing two points depends on that operator's implementation. Do not infer an ordering solely from their coordinates or the template.
- Raw C strings do not gain textual comparison from this template; use `std::string` objects.

For a single parameter `T`, `Max(1, 1.1)` fails ordinary deduction because the arguments suggest different types. One explicit solution is `Max<double>(1, 1.1)`, which converts the integer argument to `double`.

### Multiple types and the slide exercise

```cpp
template <typename T, typename U>
T MaxMixed(T a, U b) {
    return (a > b) ? a : b;
}
```

`MaxMixed(1, 1.1)` returns **`1`**:

1. `T` is `int` and `U` is `double`.
2. The comparison selects `1.1`.
3. The declared return type is `int`, so returning converts `1.1` to `1`.

The expression's type and the function's declared return type are separate issues. Choosing the right return type is part of generic interface design.

## 3. Generic Selection Sort (Slides 9-10)

Selection sort repeatedly finds the smallest remaining element and moves it to the next output position. The following adapts the slides and defines the helper before use:

```cpp
template <typename T>
void swapValues(T& x, T& y) {
    T temp = x;
    x = y;
    y = temp;
}

template <typename T>
void selectionSort(T* array, int n) {
    for (int i = 0; i < n; ++i) {
        int minIndex = i;
        for (int j = i + 1; j < n; ++j) {
            if (array[j] < array[minIndex]) minIndex = j;
        }
        swapValues(array[i], array[minIndex]);
    }
}
```

Requirements: `n` is nonnegative, storage contains at least `n` elements, and `T` supports `<`, copying, and assignment. Sorting does not require an arithmetic type: strings work because they support the necessary operations.

For `[3, 1, 2]`, the passes produce `[1, 3, 2]`, then `[1, 2, 3]`. After each pass, the prefix through index `i` is in its final position. The algorithm performs `n(n-1)/2` comparisons, so its running time is quadratic; it uses constant auxiliary space. Ordinary selection sort is not stable.

## 4. Class Templates and Implementation Placement (Slides 11-14)

To generalize a `CharStack`, replace element-specific uses of `char` with `ValueType`: the array becomes `ValueType*`, `push` accepts a `ValueType`, and `pop` returns one.

A syntax sketch, not a complete stack implementation:

```cpp
template <typename ValueType>
class Stack {
public:
    Stack();
    void push(ValueType value);
    ValueType pop();
private:
    ValueType* array;
    int capacity;
    int count;
};

template <typename ValueType>
Stack<ValueType>::Stack()
    : array(new ValueType[10]), capacity(10), count(0) {}
```

Every out-of-class method definition repeats the template declaration and qualifies its name with `Stack<ValueType>::`. A real owning stack also needs destruction, an ownership/copy policy, growth, and empty-pop handling; the sketch only shows template syntax.

Clients name the element type:

```cpp
// Stack<int> numbers;
// Stack<std::string> words;
```

`Stack<int>` and `Stack<std::string>` are different types. `new ValueType[capacity]` also imposes requirements on how elements can be default-initialized; generic code still has type constraints.

The compiler normally needs template definitions where it instantiates them. Put definitions in the header, or in an implementation file included by the header. Moving all definitions into an independently compiled `.cpp` often causes missing instantiations at link time. Explicit instantiation is a more advanced alternative; header-only definitions are the lecture's approach.

## 5. Why Iterators Exist (Slides 15-19)

Indexing works naturally for an array or vector, but not every collection has efficient numeric indexing. An iterator provides a common traversal interface while hiding storage details.

An iterator behaves like a position:

- `begin()` identifies the first element.
- `end()` identifies a position **one past** the final element.
- `*it` accesses the current element.
- `++it` advances.
- `it != end()` checks whether traversal should continue.

```cpp
#include <vector>
#include <iostream>

void print(const std::vector<int>& values) {
    for (auto it = values.begin(); it != values.end(); ++it) {
        std::cout << *it << ' ';
    }
}
```

The range is **half-open**, `[begin, end)`. For an empty container, `begin() == end()`, so the loop body never runs. Never dereference `end()`.

A container commonly exports a nested `iterator` type, such as `std::vector<int>::iterator`; const containers provide iterators that cannot modify their elements. In generic code, a dependent type may require `typename`, as in `typename Container::iterator`.

**Slide clarification:** standard container adaptors such as `std::stack` do not expose `begin()` and `end()`. A course `Stack` can supply iterators, but a loop over it does not automatically apply to `std::stack`.

## 6. Range-Based `for` (Slides 16-17)

Since C++11, range-based loops express ordinary traversal directly:

```cpp
std::vector<int> values{1, 2, 3};
for (auto x : values) x *= 2;        // changes only the local copies
for (auto& x : values) x *= 2;       // values becomes {2, 4, 6}
for (const auto& x : values) {
    // Read x without copying or modifying it.
}
```

Conceptually, the loop obtains begin/end positions, compares them, dereferences, and advances. A range loop hides iterator mechanics but does not remove the distinction between a value and a reference.

**Map clarification:** the slide's `for (string key : map)` may describe a teaching-library map. Iterating a standard `std::map` yields key-value pairs:

```cpp
// For a std::map<std::string, int> counts:
// for (const auto& entry : counts) {
//     std::cout << entry.first << ": " << entry.second << '\n';
// }
```

## 7. Iterator Capabilities and Reverse Traversal (Slides 20, 22)

Not every iterator supports pointer arithmetic.

| Category | Typical capability |
|---|---|
| Input | Read and advance with `++`; may be single-pass |
| Output | Write and advance |
| Forward | Multipass forward traversal |
| Bidirectional | Forward plus backward movement with `--` |
| Random access | Arithmetic such as `+= n`, differences, and ordering |

**Slide correction:** decrement (`--`) requires bidirectional capability; an input iterator need not support it. Vector iterators support random access, but that does not make `it += 2` or `it < end()` valid for all containers.

### Walk backward from the end

```cpp
// For a vector v:
// auto it = v.end();
// while (it != v.begin()) {
//     std::cout << *--it << ' ';
// }
```

Decrement occurs before dereferencing because `end()` itself is not an element. The guard also makes the loop safe for an empty vector.

### Reverse iterators

```cpp
// for (auto it = v.rbegin(); it != v.rend(); ++it) {
//     std::cout << *it << ' ';
// }
```

`rbegin()` starts at the final element, and `rend()` marks the reverse traversal's end. Incrementing a reverse iterator moves backward in the container's ordinary order. Neither end sentinel may be dereferenced.

**Stride caution:** slide 20 advances by two until `it < end()`. For odd-sized vectors, advancing beyond the one-past-end position is invalid. Use indices for this simple task:

```cpp
// for (std::size_t i = 0; i < v.size(); i += 2) {
//     std::cout << v[i] << ' ';
// }
```

Slide 22's displayed forward and backward sequences are inconsistent. For input `0 1 2 3 4 5 6 7 8 9`, reverse traversal must produce `9 8 7 6 5 4 3 2 1 0`.

## 8. Implementing a Vector-Like Iterator (Slides 19, 21)

For an array-backed teaching container, an iterator can store a pointer to its owning container and a current index. A nested class can access the enclosing class's private members, but still needs an object through which to access nonstatic state.

A simplified mutable iterator sketch:

```cpp
template <typename T>
class ArrayView {
public:
    ArrayView(T* data, int size) : data(data), size(size) {}

    class iterator {
    public:
        iterator(ArrayView* owner, int index) : owner(owner), index(index) {}
        T& operator*() const { return owner->data[index]; }
        iterator& operator++() { ++index; return *this; }
        bool operator!=(const iterator& other) const {
            return owner != other.owner || index != other.index;
        }
    private:
        ArrayView* owner;
        int index;
    };

    iterator begin() { return iterator(this, 0); }
    iterator end() { return iterator(this, size); }

private:
    T* data; // non-owning: underlying array must outlive the view and traversal
    int size;
};
```

```cpp
int data[] = {2, 4, 6};
ArrayView<int> view(data, 3);
for (int& x : view) ++x; // underlying array becomes {3, 5, 7}
```

This teaching sketch supplies the operations used by the range loop, not the full standard iterator requirements. A production iterator needs additional facilities, including suitable const support and iterator traits.

Array traversal has simple state; traversing a tree may require maintaining a path or other state to replace recursion. This is why iterators are easier for some representations than others.

Iterator validity depends on the container and operation. In particular, vector reallocation invalidates existing iterators; destroying a container leaves its iterators unusable. Do not assume an iterator remains valid after modifying the collection.

## 9. Revision Checklist

- Predict `operate(1, 2)` versus `operate(1.0, 2.0)`.
- Write one- and two-type function templates and identify required operations.
- Explain why mixed-type return conversion can turn `1.1` into `1`.
- Convert selection sort and its swap helper into templates.
- Write a class template and correctly qualify out-of-class methods.
- Explain why template implementations normally appear in headers.
- Trace `[begin, end)` for empty and nonempty containers.
- Distinguish copying, modifying references, and const references in range loops.
- Identify which iterator categories support `--` and random access.
- Explain reverse traversal and avoid dereferencing an end sentinel.
- Describe an iterator's owner/index state and distinguish teaching containers from standard adaptors.
