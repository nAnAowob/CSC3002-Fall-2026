# Part 1: Select 1 Choice
1. Which
# Part 2: Multiple Choice

1. getX()
```
void swap1(int x, int y) {int t=x; x=y; y=t;} //(A) incorrect (not swap)
void swap2(int &x, int &y) {int t=x; x=y; y=t;} //(B) correct (swap)
void swap3(int *x, int *y) {int* t=x; x=y; y=t;} //(C) incorrect (not swap)
void swap4(int *x, int *y) {int t=*x; *x=*y; *y=t;} // (D) correct
void swap5(int *x, int *y) {int t=*x; *x=*y; y=t;}  // (E) incorrect (not compile)
void swap6(int *x, int *y) {int t=*x; x=*y; *y=t;}  // (F) incorrect (not compile)
```

# Part 3: Short Answer
## 3.1. Write 1-2 sentences explaining the definitions (2pt each)
1. Compile-time (Static) Polymorphism
2. Runtime  (Dynamic) Polymorphism
3. Encapsulation
4. Inheritance
5. Abstract Class
6. Virtual Function
7. Overloading
8. Override
9. Iteration
10. Pointer
## 3.2. Explain
### 1. Determine the output

Given the following code, what are the values of `p2.x` and `p2.y` after execution?

```
class Point {
public:
    int x, y;
};

int main() {
    Point p1, p2;
    p1.x = 100;
    p1.y = 100;
    p2 = p1;
}
```

### 2. Complete the copy assignment operator

Complete the following copy assignment operator for the `Point` class. Write **one line of code in each blank**.

```
Point& operator=(const Point& src) {
    x = src.x;
    // Write your code here.
    // Write your code here.
}
```
### 3. Consider the following C++ function template:
```
template <typename valueType1, typename valueType2>
valueType1 Max(valueType1 v1, valueType2 v2) {
    return v1 > v2 ? v1 : v2;
}
```

For each of the following function calls, determine the return value and return type. Briefly explain your answer.

3.1 `Max(1, 1.1)`

3.2 `Max(1, 2.9)`