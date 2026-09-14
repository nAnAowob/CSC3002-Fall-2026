#include<iostream>
using namespace std;

int main() {
    int a = 5;
    int b = a++; //post increment
    cout << "a = " << a << ", b = " << b << "\n";
    /*Output:
    a = 6, b = 5
    Post increment returns the value before incrementing, so b is assigned the value of a before it was incremented.
    */

    int c = 5;
    int d = ++c; //pre increment
    cout << "c = " << c << ", d = " << d << "\n";
    /*Output:
    c = 6, d = 6
    Pre increment increments the value before returning it, so d is assigned the value of c after it was incremented.
    */

    int i = 0;
    int arr[5] = {0, 1, 2, 3, 4};
    cout << "arr[i++] = " << arr[i++] << ", i = " << i << "\n";
    i = 0; //reset i to 0
    cout << "arr[++i] = " << arr[++i] << ", i = " << i << "\n"; 


    /* i = 0
        a[i++] = a[0], then i = 1
        i = 0
        a[++i] = a[1], and i = 1
    */

    int x = 10, y = 11;

    if (x<y) {
        cout << "x is less than y\n";
    } else if (x<=y) {
        cout << "x is less than OR EQUAL TO y\n";
    }
    cout << "finished if-else statement\n";
}