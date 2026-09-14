#include<iostream>
using namespace std;

double f1(double x) {
    x = x + 10.0;
    return x+1;
}

double f2(double x) {
    x = x + 10.0;
    return x++;
}

void swap1(int x, int y) {
   int tmp = x;
   x = y;
   y = tmp;
}
void swap2(int & x, int & y) {
   int tmp = x;
   x = y;
   y = tmp;
}


int main() {
    double xx = 10.0;
    double y1 = f1(xx);
    double y2 = f2(xx);
    cout << xx << "\ny1: " << y1 << "\ny2: " << y2 << endl;

    int a = 1, b = 2;
    int x = 3, y = 4;
    swap1(a,b);
    swap2(x,y);
    cout << a << ' ' << b << endl;
    cout << x << ' ' << y;
}

