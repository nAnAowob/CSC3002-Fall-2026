#include <iostream>
#include "swap.h"
using namespace std;

int main() {
    int a = 10, b = 20;

    cout << "Before swap1: a = " << a << ", b = " << b << endl;
    swap1(a, b);
    cout << "After swap1: a = " << a << ", b = " << b << endl;

    cout << "Before swap2: a = " << a << ", b = " << b << endl;
    swap2(a, b);
    cout << "After swap2: a = " << a << ", b = " << b << endl;

    return 0;
}