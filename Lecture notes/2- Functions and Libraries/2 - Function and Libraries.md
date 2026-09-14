# Parameter vs Argument

## parameter

```cpp
double f(double x) {
   return x * x + 1;
}
```
## argument

```cpp
double y = 1.0;
double z = f(y);
```
# Defining functions in C++
```
type name (parameter list) {

   statements in the function body

}
```
- type indicates what type the function returns
- name is the name of the function
- parameter list is a list of variable declarations used to hold the values of each argument
- statements in the function body implement the function (e.g., the algorithm), at least including a return statement
1. predicate functions.
```cpp
bool isEven(int n) {
   return n % 2 == 0;
}
. . .
if (isEven(i)) . . .
```

2. procedure: function that has no return value [ void() ]
**All functions need to be declared before they are called by specifying a prototype consisting of the header line followed by a semicolon.**
## function prototype
1. low-level function: define the function before calling main()
```cpp
double squeeze(double x) { ... }
double f(double x) {
	double F = 10.0;
		double y = squeeze(F);
		double z = f(y)
}
int main(){
	double F = 10.0;
	double E = f(F)
}
```
2. intermediate-level function:

# C++ Enhancement
## overloaded function
```cpp
#include <iostream>

int add1(int x);
	double add1(double x);
int main() {
   double x;
   std::cin >> x;
   std::cout << add1(x)/4;
   return 0;

}

int add1(int y) {
   return y + 1;

}

double add1(double x) {
   return x + 1;

}
```