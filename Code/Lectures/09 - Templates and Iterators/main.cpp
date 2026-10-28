#include <iostream>
#include <string>
#include "Vector.h"
using namespace std;

void print(const Vector<int>& v, bool bForward = true)
{
     if(bForward) {
//          for (auto x:v) cout <<" "<<x;
     for (auto it = v.begin(); it!=v.end(); it++) cout <<" "<<*it;
     } else {
     for (auto it = v.rbegin(); it!=v.rend(); it++) cout <<" "<<*it;
     }
     cout <<endl;
}

int main()
{
     Vector<int> vec;
     for(int i = 0; i<11; i++) vec.push_back(i);
     print(vec);
     print(vec,false);
     return 0;
}