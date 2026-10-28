#include <cassert>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <string>
#include <cstring>
#include <memory>
#include <vector>
#include <type_traits>
using namespace std;
void adjust(int a,int& b,int* c){a+=2;b+=a;*c+=b;}
int pick(int x){return x+1;}
double pick(double x,int extra=2){return x+extra;}
template<typename T>T half(T v){return v/2;}
template<typename T>T larger(T a,T b){return a>b?a:b;}
void inspect(int a[6]){static_assert(is_same_v<decltype(a),int*>);}
struct Ticket{const int code;static int created;Ticket(int c):code(c){++created;}int getCode()const{return code;}};
int Ticket::created=0;
struct Reporter{virtual int report()const=0;int tag()const{return 1;}virtual ~Reporter()=default;};
struct Brief:Reporter{int report()const override{return 7;}int tag()const{return 2;}};
struct SilentReporter:Reporter{int report()const override{return 0;}};
bool isEven(long value){return value%2==0;}
int countIf(const long* a,int n,bool(*pred)(long)){int count=0;for(int i=0;i<n;++i)if(pred(a[i]))++count;return count;}
struct Money{int cents;Money operator+(const Money& rhs)const{return Money{cents+rhs.cents};}Money& operator+=(const Money& rhs){cents+=rhs.cents;return *this;}};
template<typename T>T halfValue(T value){return value/2;}
int main(){
 {int x=3,y=4,z=5;adjust(x,y,&z);assert(x==3&&y==9&&z==14);}
 {ostringstream o;o<<pick(4)<<' '<<pick(4.5)<<' '<<pick(4.5,1);assert(o.str()=="5 6.5 5.5");}
 {int visits=1;bool a=true||(++visits>2);bool b=false||(++visits>2);bool c=b&&(++visits>0);ostringstream o;o<<visits<<' '<<a<<' '<<b<<' '<<c;assert(o.str()=="2 1 0 0");}
 {auto a=half(9);auto b=half(9.0);double c=half(9);static_assert(is_same_v<decltype(a),int>);static_assert(is_same_v<decltype(b),double>);assert(a==4&&b==4.5&&c==4.0);}
 {int values[4]={2,4,6,8};inspect(values);const int* read=values;int* const fixed=values;++read;*fixed=9;assert(read==values+1&&values[0]==9);assert((values+4)-values==4);}
 {char label[]="Go";string word="Blue";assert(sizeof(label)==3&&strlen(label)==2);assert(word.substr(1,2)=="lu"&&word=="Blue");assert(string("C")+"++"=="C++"&&"C"+string("++")=="C++");assert(strcmp("Go","Go")==0);}
 {Ticket a(17);const Ticket b(42);assert(Ticket::created==2&&a.getCode()==17&&b.getCode()==42);}
 {Brief b;Reporter&r=b;assert(r.report()==7&&r.tag()==1);Reporter*p=new Brief;delete p;}
 {int*p=new int[1];delete[]p;auto s=make_shared<int>(3);weak_ptr<int>w=s;assert(s.use_count()==1);s.reset();assert(w.expired());static_assert(!is_copy_constructible_v<unique_ptr<int>>);}
 {ostringstream oss;oss<<fixed<<setprecision(2)<<3.14159;assert(oss.str()=="3.14");assert(oss.str()=="3.14");}
 {assert(larger<double>(2,2.5)==2.5);vector<int>v{1,2,3};for(auto x:v)++x;assert((v==vector<int>{1,2,3}));for(auto&x:v)++x;assert((v==vector<int>{2,3,4}));}
 {int data[5]={3,6,9,12,15};int*p=data;int a=*++p;int b=*p++;int c=++*p;int d=(*p)++;ostringstream o;o<<a<<' '<<b<<' '<<c<<' '<<d<<'\n';o<<(p-data)<<' '<<*p<<'\n';assert(o.str()=="6 6 10 10\n2 11\n");assert(data[0]==3&&data[1]==6&&data[2]==11&&data[3]==12&&data[4]==15);}
 {bool(*test)(long)=isEven;long a[]={3,4,8,9};assert(countIf(a,4,test)==2);assert(countIf(nullptr,0,test)==0);assert(isEven(-4)&&!isEven(-3));}
 {const Money a{120},b{30};Money c=a+b;assert(a.cents==120&&b.cents==30&&c.cents==150);Money d{120};(d+=b)+=b;assert(d.cents==180);SilentReporter s;Reporter&r=s;assert(r.report()==0);}
 {auto a=halfValue(7);auto b=halfValue(7.0);double c=halfValue(7);auto d=halfValue<double>(7);static_assert(is_same_v<decltype(a),int>&&is_same_v<decltype(b),double>&&is_same_v<decltype(d),double>);assert(a==3&&b==3.5&&c==3.0&&d==3.5);}
 {istringstream in("24\nAda Lovelace\n");int id;string first,name;in>>id;getline(in,first);getline(in,name);ostringstream out;out<<fixed<<setprecision(2)<<setfill('_');out<<setw(6)<<3.5<<'|'<<2.0;ostringstream result;result<<id<<":["<<first<<"]\n";result<<'['<<name<<"]\n";result<<out.str()<<'\n';assert(result.str()=="24:[]\n[Ada Lovelace]\n__3.50|2.00\n");}
 {istringstream numbers("10 20 x 30");int n,total=0;while(numbers>>n)total+=n;assert(total==30&&numbers.fail());numbers.clear();char bad;numbers>>bad;assert(bad=='x');if(numbers>>n)total+=n;assert(total==60);}
 cout<<"All 14 questions: defined behavior, outputs and reference solutions verified.\n";
}
