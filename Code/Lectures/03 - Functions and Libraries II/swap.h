#include<iostream>
using namespace std;

void swap1(int x,int y) {
    int temp = x;
    x = y;
    y = temp;
}

void swap2(int &x, int &y){
    int temp = x;
    x = y;
    y = temp;
}