#include <cassert>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <cstring>
using namespace std;
bool isMultipleOf3(long x){return x%3==0;} bool isNegative(long x){return x<0;}
int countMatches(const long*a,int n,bool(*pred)(long)){int count=0;for(int i=0;i<n;++i)if(pred(a[i]))++count;return count;}
struct Money{int cents;Money operator+(const Money&rhs)const{return Money{cents+rhs.cents};}Money&operator+=(const Money&rhs){cents+=rhs.cents;return *this;}};
struct Reader{virtual int read()const=0;int label()const{return 4;}virtual ~Reader(){cout<<"R";}};
struct FixedReader:public Reader{int read()const override{return 6;}int label()const{return 9;}~FixedReader()override{cout<<"F";}};
template<typename T>T quarter(T x){return x/4;}template<typename T>T twice(T x){return x+x;}
int main(){long data[]={-6,1,3,10,12};bool(*rule)(long)=isMultipleOf3;assert(countMatches(data,5,rule)==3);rule=isNegative;assert(countMatches(data,5,rule)==1&&countMatches(nullptr,0,rule)==0);Money a{45},b{12},c{8};const Money fee{5};Money d=fee+b;(a+=b)+=c;assert(a.cents==65&&d.cents==17);Reader*p=new FixedReader;assert(p->read()==6&&p->label()==4);ostringstream destruct;auto*old=cout.rdbuf(destruct.rdbuf());delete p;cout.rdbuf(old);assert(destruct.str()=="FR");assert(quarter(11)==2&&quarter<double>(11)==2.75&&twice(1.25)==2.5);int values[]={5,0,-2,9};int total=0;for(int*p=values;*p!=0;++p)total+=*p;assert(total==5);total=0;for(int*p=values;p!=values+4;++p)total+=*p;assert(total==12);char text[]="Sun";assert(sizeof(text)==4&&strlen(text)==3);string word="Moon";assert(word.substr(1,2)=="oo");ostringstream out;out<<fixed<<setprecision(2)<<setfill('_')<<setw(6)<<7.5<<'|'<<1.0;assert(out.str()=="__7.50|1.00");istringstream nums("4 6 x 8");int n;total=0;while(nums>>n)total+=n;assert(total==10);nums.clear();char bad;nums>>bad;if(nums>>n)total+=n;assert(total==18);}
