#include <iostream>
#include <type_traits>
using namespace std;

// Templates: the compiler generates a function for the argument types.
template <typename ValueType1, typename ValueType2>
typename common_type<ValueType1, ValueType2>::type Max(ValueType1 v1, ValueType2 v2) {
    // A common return type preserves a double when comparing int and double.
    return (v1 > v2) ? v1 : v2;
}

// Overloading: same name, different parameter lists (chosen at compile time).
// Changing only the return type does not create a valid overload.
int function(int x, int y) {
    return x + y;
}

double function(double x, double y) {
    return x + y;
}

// Overriding: a derived class replaces an inherited virtual function.
class Animal {
public:
    virtual void speak() const {
        cout << "Animal makes a sound" << endl;
    }

    virtual ~Animal() = default;
};

class Dog : public Animal {
public:
    void speak() const override {
        cout << "Dog barks" << endl;
    }
};

int main() {
    /*
    1. Compile-time polymorphism: function overloading and templates.
    2. Runtime polymorphism: overriding virtual functions, called through
       a base-class pointer or reference. The term is "override", not "overwrite".
    */
    cout << "Max(3, 7): " << Max(3, 7) << endl;
    cout << "Max(3, 7.5): " << Max(3, 7.5) << endl;

    cout << "function(2, 3): " << function(2, 3) << endl;
    cout << "function(2.5, 3.5): " << function(2.5, 3.5) << endl;

    Animal animal;
    Dog dog;
    Animal* ptr = &animal;
    ptr->speak(); // Calls Animal::speak().
    ptr = &dog;
    ptr->speak(); // Calls Dog::speak(), even though ptr has type Animal*.

    return 0;
}
