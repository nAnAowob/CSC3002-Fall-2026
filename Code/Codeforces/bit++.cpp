#include<iostream>
#include<cstring>
using namespace std;

int main() {
    int _x = 2;
    cout << _x << endl;

    int cat;
    cat=13;
    cout << cat << endl;

    int dog;
    dog = (cat = 15,14);
    cout << dog << endl;
}