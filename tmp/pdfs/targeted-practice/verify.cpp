#include <cassert>
#include <sstream>
#include <iomanip>
#include <string>
#include <memory>
#include <vector>
#include <limits>
using namespace std;
struct Ticket { const int code; static int created; Ticket(int c):code(c){++created;} int getCode() const{return code;} }; int Ticket::created=0;
bool isPositive(long x){return x>0;} bool isEven(long x){return x%2==0;}
int countIf(const long* a,int n,bool(*pred)(long)){int count=0;for(int i=0;i<n;++i)if(pred(a[i]))++count;return count;}
struct Money { int cents; Money operator+(const Money& rhs)const{return Money{cents+rhs.cents};} Money& operator+=(const Money& rhs){cents+=rhs.cents;return *this;} };
struct Reporter {virtual int report()const=0;int tag()const{return 1;}virtual ~Reporter()=default;};
struct QuietReporter:public Reporter{int report()const override{return 0;}int tag()const{return 9;}};
template<typename T>T third(T x){return x/3;}
int main(){Ticket t(9);const Ticket u(14);assert(t.getCode()==9&&u.getCode()==14&&Ticket::created==2);long data[]={-3,0,4,7};bool(*test)(long)=isPositive;assert(countIf(data,4,test)==2&&countIf(data,4,isEven)==2&&countIf(nullptr,0,test)==0);Money a{80},b{15},c{5};Money d=a+b;(a+=b)+=c;assert(a.cents==100&&b.cents==15&&c.cents==5&&d.cents==95);const Money e{3};assert((e+b).cents==18);QuietReporter s;Reporter& r=s;assert(r.report()==0&&r.tag()==1&&s.tag()==9);
istringstream in("18\nLin Chen\n");int id;string first,name;in>>id;getline(in,first);getline(in,name);assert(id==18&&first.empty()&&name=="Lin Chen");ostringstream out;out<<fixed<<setprecision(2)<<setfill('_')<<setw(7)<<4.5<<'|'<<8.0;assert(out.str()=="___4.50|8.00");istringstream numbers("5 15 x 25");int n,total=0;while(numbers>>n)total+=n;assert(total==20);numbers.clear();char bad;numbers>>bad;if(numbers>>n)total+=n;assert(bad=='x'&&total==45);auto owner=make_shared<int>(6);weak_ptr<int>w=owner;assert(owner.use_count()==1);owner.reset();assert(w.expired());assert(third(8)==2&&third(9.0)==3.0&&third<double>(9)==3.0);vector<int>v{2,5,8};for(auto&x:v)x+=3;assert((v==vector<int>{5,8,11}));}
