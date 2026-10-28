# A: Method for reading C++
1. Identify types: array, pointer, reference, object?
2. Locate the operation:
3. Track state changes: value of variable sometimes not change
4. Check the results: type -> same with the output of function, value & lifetime -> static or not?
## 3 questions
1. find some errors in the exam
2. what does evaluate to -> in/out of function
3. grammar of c++
# 2. Function parameters: Value, Reference, Pointer
## 2.5. Function Pointers
design something like this in the exam
```cpp
bool isEven(long value)

{

return value % 2 == 0;

}

  

int main()

{

bool (*test)(long) = isEven;

bool ok = test(12L);

cout << ok << endl;

return 0;

}
```

### examples
```cpp
int main()

{

int attemps = 0;

bool flag = false;

  

bool first = flag && (++attemps > 0); // left is false, right is skipped

bool second = !flag || (++attemps > 0); //left is false, rig is skipped

}
```
# 3. Raw Arrays and Pointer Variables
```cpp
int main()

{

int marks[4] = {5, 10, 15, 20};

int* cursor = marks;

++cursor;

int selected = *cursor; // selected = 10

}
```

# 4.4. Inheritance and Virtual Functions
Design some interfaces for the function -> same name to achieve different goals
# 4.5. 
concept of abstract and virtual, why we need to use in C++ (THE CONCEPT IS IMPORTANT)
# 4.6. Operator Overloading
** needs to know how to write, what is the meaning of ... here (const), 

# 5.1. Function Templates and Deduction
know how to write such a function template, and learn to judge the output from input
>> give you some different input and tell them the different output
>
# 5.2. 