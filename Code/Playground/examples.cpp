#include<iostream>
#include<cstring>
using namespace std;

double add(int c, int d) {
	cout << "double add\n";
	return c+d;
}
int main() {
	// int a = 1,b = 2;
	// double c = 1.0, d = 3.0;
	// int r1 = add(a,b);
	// int r2 = add(c,d);
	// cout << r1 << " " << r2;
	// A
	int a = 2;
	int b = 9;
	int c = 7;
	int& r = a;

	r = b;
	b = 100;    
	cout << &a << " " << &b << " " << &r << endl;
	cout << a << " " << b << " " << r << endl;

	int DIGITS[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
	cout << sizeof(DIGITS) << " " <<sizeof(DIGITS[0]);
}