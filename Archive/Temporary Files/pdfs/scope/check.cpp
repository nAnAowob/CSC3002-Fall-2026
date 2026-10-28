#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
using namespace std;
int main(){
int arr[]={2,0,2,1}; int* p=arr;
int a=*++p; int b=*p++; int c=++*p; int d=(*p)++;
cout<<arr[0]<<arr[1]<<arr[2]<<arr[3]<<'\n'<<a<<b<<c<<d<<'\n';
cout<<fixed<<setprecision(2)<<setfill('_')<<setw(6)<<3.5<<'|'<<2.0<<'\n';
istringstream in("42\nAlice Bob\n");int n;string s,t;in>>n;getline(in,s);getline(in,t);cout<<n<<'|'<<s<<'|'<<t<<'\n';
istringstream input("10 20 x 30");int x,total=0;while(input>>x)total+=x;cout<<total<<'|'<<boolalpha<<input.fail()<<'\n';
}
