#include<iostream>
#include<string.h>
using namespace std;

// int main() {
//     //don't convert pointers from double into integer
//     int i = 1;
//     int * pi = &i;
//     double d = 2.1;
//     double * pd = &d;
//     cout << *pi << endl;
//     cout << *pd << endl;
//     int * pi1 = (int *) pd;
//     cout << *pi1 << endl;
//     double * pd1 = (double *) pi;
//     cout << *pd1 << endl;
// }

// int main(){
//     int *p,x;
//     x = 3;
//     p = &x;
//     int d = *p;
//     cout << d << endl << p << endl << &x << endl  << x;

//     string str1 = "hello,world";
//     string str2 = "hello" + "," + string("world");
// }
int main() 
{
	// int n = 42;
	// int *p = &n;
	// int** pp = &p;
	
	// cout << "n: " << n << " " << &n << endl;
	// cout << "p: " << &p << " " << p << " " << *p << endl;
	// cout << "pp: " << &pp << " " << pp << " " << *pp << " " << **pp << endl;
	
	// **pp = 7;

	// cout << "n: " << n << " " << &n << endl;
	// cout << "p: " << &p << " " << p << " " << *p << endl;
	// cout << "pp: " << &pp << " " << pp << " " << *pp << " " << **pp << endl;
	
	int a[4] = {2,4,6,8};
	int* p = a;
	
	cout << *p+2 << " " << *(p+2) << " " << p+4;
}