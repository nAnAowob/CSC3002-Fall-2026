#include <iostream>
#include <type_traits>
using namespace std;
struct A {int a; A():a(1){} void display(){cout<<a<<endl;}};
struct B:A {int b; B():b(2){} void display(){cout<<a<<b<<endl;}};
struct C:B {int c; C(){b=1;c=3;} virtual void display(){cout<<a<<b<<c<<endl;}};
int main(){
cout << 9*(8-7)/6 + 5*4%3*(2+1.0) << '\n';
C obj; B* pb=&obj;pb->display();
int arr[]={2,0,2,1};int* p=arr;
int a=*++p,b=*p++,c=++*p,d=(*p)++;
cout<<arr[0]<<arr[1]<<arr[2]<<arr[3]<<'\n'<<a<<b<<c<<d<<'\n';
cout<<((0xFF202104u>>8)&0xFFu)<<'\n';
static_assert(!is_copy_constructible<ostream>::value);
static_assert(is_lvalue_reference<decltype((p))>::value);
static_assert(is_lvalue_reference<decltype(*p)>::value);
static_assert(!is_lvalue_reference<decltype(&p)>::value);
static_assert(!is_lvalue_reference<decltype(p+1)>::value);
}
