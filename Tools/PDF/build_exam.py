from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit
from pathlib import Path
out=Path(__file__).resolve().parents[2]/'Exam Prep/Midterm/CSC3002_Mock_Midterm.pdf'
c=canvas.Canvas(str(out),pagesize=A4)
c.setTitle('CSC3002 Mock Midterm - Questions Only')
c.setAuthor('Practice paper prepared from course materials')
W,H=A4; margin=48; y=0; page=0
navy=HexColor('#16324a'); gray=HexColor('#526171')
def text(s,size=10.5,font='Helvetica',gap=5):
 global y
 c.setFont(font,size); c.setFillColor(navy)
 for line in simpleSplit(s,font,size,W-2*margin):
  c.drawString(margin,y,line); y-=size*1.4
 y-=gap
 assert y>42,(page,s,y)
def code(s):
 global y
 lines=s.split('\n'); h=len(lines)*13+16
 c.setFillColor(HexColor('#f1f4f7')); c.roundRect(margin-3,y-h+12,W-2*margin+6,h,4,fill=1,stroke=0)
 c.setFillColor(navy);c.setFont('Courier',9.3)
 for line in lines:
  assert c.stringWidth(line,'Courier',9.3)<W-2*margin
  c.drawString(margin+8,y-2,line);y-=13
 y-=14
 assert y>42

def start(title,sub):
 global y,page
 if page:c.showPage()
 page+=1;y=H-49
 c.setFillColor(gray);c.setFont('Helvetica',9);c.drawString(margin,y,'CSC3002  /  FALL 2026  /  PRACTICE PAPER')
 c.drawRightString(W-margin,28,f'{page} / 8')
 c.setStrokeColor(HexColor('#cbd4dd'));c.line(margin,40,W-margin,40)
 y-=36;text(title,20,'Helvetica-Bold',6);text(sub,10,'Helvetica',14)
def q(n,s,opts=None,src=None):
 text(f'{n}.  {s}',10.5,'Helvetica-Bold',3)
 if src:code(src)
 if opts:
  for a,b in zip('ABCD',opts):text(f'{a}.  {b}',9.5,'Helvetica',0)
  text('Answer: __________',9,'Helvetica',5)
def box(h):
 global y
 c.setStrokeColor(HexColor('#b8c3ce'));c.rect(margin,y-h,W-2*margin,h);y-=h+15
start('Mock midterm examination','Questions only  |  90 minutes  |  100 marks  |  32 questions')
text('Name: _______________________     Student ID: _______________________',11,gap=24)
text('Practice conditions',13,'Helvetica-Bold')
for s in ['Allow one double-sided A4 sheet of notes. Use no calculator, compiler, internet, or AI assistance during the timed attempt. These are suggested practice conditions, not official midterm rules.', 'Answer all questions. Write T/F for Section I, one letter for Section II, and all selected letters for Section III. Write working and answers in Section IV.', 'Assume standard C++17, required headers, and using namespace std; unless stated otherwise. Each code fragment is independent. Assume allocations succeed. No unspecified machine sizes should be assumed.', 'For output questions, preserve spaces and line breaks. Never invent an output for undefined behavior.']:
 text(s,gap=10)
text('Marks and suggested timing',13,'Helvetica-Bold')
for s in ['I. True / false: Q1-10 | 10 marks | 8 minutes','II. Single choice: Q11-20 | 20 marks | 17 minutes','III. Multiple selection: Q21-30 | 40 marks | 30 minutes','IV. Tracing and addresses: Q31-32 | 30 marks | 30 minutes','Reserve the final 5 minutes to check your answers.']:text(s)
text('Scope and design',13,'Helvetica-Bold')
text('Scope is inferred from your saved Functions and Libraries, Strings, Streams, Pointers and Arrays, and Lecture 7 Dynamic Memory Management materials, plus Assignment 1 and Tutorial 4. This is an original practice paper, not a prediction of the official midterm.')
text('The four-section format and emphasis on pointer tracing follow the 2020-2021 Term 2 final in Exam Prep/Past Papers/csc3002 final(2).pdf. Advanced final-exam topics beyond this inferred scope are omitted. No solutions are included.',9.5)
start('Section I. True / false','10 questions x 1 mark = 10 marks. Write T or F in each blank.')
tf=[
'A function with return type int may contain more than one return statement.',
'Changing an int parameter passed by value always changes the caller\'s corresponding int variable.',
'Two ordinary functions in the same scope can be overloaded solely by changing their return types.',
'For char s[] = "quiz";, sizeof(s) is 5 and strlen(s) is 4.',
'The expression "mid" + "term" performs valid C++ string concatenation.',
'After successful formatted integer extraction, a following getline can read an empty line if the next character is a newline.',
'In a parameter declaration, int a[10] is adjusted to int* a; it does not enforce an argument length of 10.',
'For int a[5];, the expression a + 5 may be formed, but dereferencing that one-past-the-end pointer is invalid.',
'After delete p;, assigning nullptr to p automatically sets every other pointer to the deleted object to nullptr.',
'Copying a shared_ptr shares ownership of its managed object rather than making a deep copy of that object.'
]
for i,s in enumerate(tf,1):text(f'{i}.  ____   {s}',11,gap=19)
start('Section II. Single choice','Q11-15. Choose exactly one option. Each question is worth 2 marks.')
q(11,'What is the value of this expression?',['4.0','4.5','5.0','5.5'],'7 / 2 + 5 % 3 * 0.5')
q(12,'What does this fragment print?',['3 5','4 5','3 9','4 9'],'''void update(int x, int& y) { ++x; y += x; }
// In main:
int a = 3, b = 5;
update(a, b);
cout << a << ' ' << b;''')
q(13,'Which parameter avoids copying a string and prevents modification through that parameter?',['string s','string& s','const string& s','string* s'])
q(14,'Which declaration correctly gives only the second parameter a default argument?',['int f(int x = 1, int y);','int f(int x, int y = 1);','int f(int x, int = y);','int f(int x = 1, int y = x);'])
q(15,'What is printed?',['6 6','7 6','12 6','12 7'],'char word[12] = "stream";\ncout << sizeof(word) << \' \' << strlen(word);')
start('Section II. Single choice','Q16-20. Choose exactly one option. Each question is worth 2 marks.')
q(16,'What is printed?',['inter','term','term!','midterm'],'''string s = "midterm";
s.erase(0, 3);
s += "!";
cout << s.substr(0, 4);''')
q(17,'What is printed?',['27','12','15','The loop never terminates'],'''istringstream in("12 15 x 8");
int value = 0, total = 0;
while (in >> value) total += value;
cout << total;''')
q(18,'Given int n = 42; int* p = &n; int** pp = &p;, the address of n is 0x3100 and the address of p is 0x4200. What are pp and **pp?',['0x3100 and 42','0x4200 and 42','0x4200 and 0x3100','0x3100 and 0x4200'])
q(19,'Which single statement correctly releases this allocation?',['delete a;','delete[] a;','delete *a;','No release is needed when a leaves scope.'],'int* a = new int[6];')
q(20,'What does int (*p)[4]; declare?',['An array of four pointers to int','A pointer to an array of four int','A pointer to a function returning int','An array of four int'])
start('Section III. Multiple selection','Q21-25. Each question is worth 4 marks.')
text('Select all correct options. Exact set: 4 marks. Nonempty proper subset with no incorrect option: 2 marks. Any incorrect selection, or no selection: 0 marks.',10,gap=12)
q(21,'Which declarations can overload int f(int x); in the same scope?',['double f(int x);','int f(double x);','int f(int y);','int f(int x, int y);'])
q(22,'Which initializations compile?',['string a = string("C") + "++";','string b = "C" + string("++");','string c = "C" + "++";','char d[] = "C++";'])
q(23,'Which statements about C++ streams are correct?',['while (in >> x) processes x only after a successful extraction.','getline(in, s) stores the newline delimiter at the end of s.','in.clear() resets error-state flags but does not discard the offending input.','An output operator for a custom type can return ostream& to support chaining.'])
q(24,'For int a[4] = {2, 4, 6, 8}; and int* p = a;, which are correct?',['*(p + 2) is 6.','p + 4 is a valid one-past-the-end pointer.','*(p + 4) is a valid array element.','a = p; is valid array assignment.'])
q(25,'Given the following declarations, which statements compile when considered independently?',['*p = 7;','p = &y;','*q = 7;','q = &y;'],'int x = 1, y = 2;\nconst int* p = &x;\nint* const q = &x;')
start('Section III. Multiple selection','Q26-30. Use the same marking rule as on the preceding page.')
q(26,'For int a[3] = {1, 2, 3}; int* p = a;, which expressions are modifiable lvalues?',['p','*p','&p','p + 1'])
q(27,'Which statements about lifetime and allocation are correct?',['A local pointer variable can point to dynamically allocated storage.','delete p; also destroys the local pointer variable p itself.','Returning the address of a local int gives the caller a pointer to an object whose lifetime has ended.','Every separately allocated row of an int** matrix must be released before its row-pointer array is released.'])
q(28,'Which statements are correct after the fragment below?',['The first allocation has leaked.','The second allocation has been freed.','q is a dangling pointer.','delete q; would safely free a remaining live object.'],'''int* p = new int(4);
int* q = new int(9);
p = q;
delete p;
p = nullptr;''')
q(29,'Which statements about smart pointers are correct?',['A unique_ptr can be freely copied to create another owner.','A shared_ptr copy can increase the shared ownership count.','A weak_ptr alone keeps its observed object alive.','weak_ptr::lock() returns an empty shared_ptr if its observed object no longer exists.'])
q(30,'A character buffer has capacity 8 bytes and must always hold a valid null-terminated C string. Which statements are correct?',['It can hold at most 7 content characters.','The null terminator contributes 1 to strlen(buffer).','Copying 7 content characters requires writing a terminator at index 7.','A stream insertion overload should normally return the original stream by reference.'])
start('Section IV. Code tracing','Q31. 12 marks total. Write the exact output for each independent fragment.')
text('31(a). Pointer operators (4 marks: 2 per output line).',11,'Helvetica-Bold')
code('''int arr[] = {3, 1, 4, 2};
int* p = arr;
int a = *++p;
int b = *p++;
int c = ++*p;
int d = (*p)++;
cout << arr[0] << ' ' << arr[1] << ' '
     << arr[2] << ' ' << arr[3] << '\\n';
cout << a << ' ' << b << ' ' << c << ' ' << d << '\\n';''')
box(49)
text('31(b). Mixing formatted input and lines (4 marks: 2 per output line).',11,'Helvetica-Bold')
code('''istringstream in("24\\nAda Lovelace\\n");
int id;
string line;
in >> id;
getline(in, line);
cout << id << ":[" << line << "]\\n";
getline(in, line);
cout << '[' << line << "]\\n";''')
box(49)
text('31(c). Shared ownership (4 marks: 2 per output line).',11,'Helvetica-Bold')
code('''auto p = make_shared<int>(7);
weak_ptr<int> w = p;
{
    auto q = p;
    *q += 2;
    cout << *p << ' ' << p.use_count() << '\\n';
}
p.reset();
cout << boolalpha << w.expired() << '\\n';''')
box(49)
start('Section IV. Addresses and values','Q32. 18 marks total. Each row is worth 1.5 marks.')
text('Assume sizeof(int) == 4, sizeof(int*) == 8, and byte-addressed memory. The first element of a starts at hexadecimal address 0x2000. Evaluate each expression independently.',11)
code('int a[6] = {2, 5, 8, 11, 14, 17};\nint* p = a + 2;')
text('Write addresses in hexadecimal with prefix 0x. Write element values, byte sizes, and pointer differences in decimal. Write INVALID only if evaluation requires an invalid operation. Do not treat an integer value as an address.',10.5,gap=17)
rows=['a (after conversion to int*)','&a','a + 1','&a + 1','&a[5]','*a + 5','*(a + 5)','p - a','sizeof(a)','sizeof(p)','a + 6','*(a + 6)']
c.setFillColor(navy);c.rect(margin,y-29,W-2*margin,29,fill=1,stroke=0)
c.setFillColor(HexColor('#ffffff'));c.setFont('Helvetica-Bold',10);c.drawString(margin+10,y-19,'Expression');c.drawString(330,y-19,'Value / address / INVALID');y-=29
for i,s in enumerate(rows):
 c.setFillColor(HexColor('#f1f4f7') if i%2==0 else HexColor('#ffffff'));c.rect(margin,y-31,W-2*margin,31,fill=1,stroke=0)
 c.setFillColor(navy);c.setFont('Courier',10);c.drawString(margin+10,y-20,s);c.setStrokeColor(HexColor('#cbd4dd'));c.line(330,y-24,W-margin-12,y-24);y-=31
y-=23;text('Working space',10,'Helvetica-Bold');box(30)
text('END OF MOCK EXAMINATION',11,'Helvetica-Bold')
c.save()
print(out.resolve())
