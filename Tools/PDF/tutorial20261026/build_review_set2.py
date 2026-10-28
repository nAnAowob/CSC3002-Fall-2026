from pathlib import Path
from xml.sax.saxutils import escape
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[3]
D=[]
def add(id,title,parts,answers):D.append(dict(id=id,title=title,parts=parts,answers=answers))
add('A1','Callback repair: a function is not its result',[
('code','bool isMultipleOf3(long x) { return x % 3 == 0; }\nint countMatches(const long* a, int n,\n                 bool (*pred)(long)) {\n    int count = 0;\n    for (int i = 0; i < n; ++i) {\n        if (pred) ++count;\n    }\n    return count;\n}'),
('task','(a) Repair the function with the smallest change. Explain what if(pred) tests and why the original returns n when pred is valid. Assume n >= 0 and a valid range for n > 0.',110),
('task','(b) Declare a long array {-6, 1, 3, 10, 12}. Declare an explicitly typed function pointer named rule, bound to isMultipleOf3. Call the repaired function and state its result.',130),
('task','(c) Write isNegative(long). Reassign rule without redeclaring it, call countMatches again, and give the result. Explain whether rule = isNegative(-6); is valid.',130)
],[('code','// Repair inside the loop:\nif (pred(a[i])) ++count;\n\nlong data[] = {-6, 1, 3, 10, 12};\nbool (*rule)(long) = isMultipleOf3;\nint first = countMatches(data, 5, rule); // 3\n\nbool isNegative(long x) { return x < 0; }\n// Back in the calling function:\nrule = isNegative;\nint second = countMatches(data, 5, rule); // 1'),('text','(a) if(pred) tests whether the function pointer is non-null. It does not call the predicate. Calling pred(a[i]) tests one array element. For n = 0 the loop does not run and count remains zero.'),('text','(b) -6, 3 and 12 match. (c) Only -6 is negative. rule = isNegative(-6) is invalid: the call produces bool, not a compatible function pointer. isNegative names the function; isNegative(-6) calls it. Put the isNegative definition outside the calling function.')])
add('A2','Money: return an object or return its identity',[
('code','struct Money {\n    int cents;\n    // Write the member operators here.\n};'),
('task','(a) Implement + and += inside the struct. Both receive a const-reference right operand. + returns a new Money and accepts a const left operand. += changes the left operand and supports chaining.',210),
('task','(b) Start with Money a{45}, b{12}, c{8}; const Money fee{5}; then Money d = fee + b; and (a += b) += c;. Give final cents for a, b, c, fee and d. Explain why += must return Money& for this contract.',110),
('task','(c) Inside +=, classify this, *this and cents as pointer, object or integer member. Explain why return cents; fails. Is Money const operator+(...) equivalent to a trailing const?',110)
],[('code','struct Money {\n    int cents;\n    Money operator+(const Money& rhs) const {\n        return Money{cents + rhs.cents};\n    }\n    Money& operator+=(const Money& rhs) {\n        cents += rhs.cents;\n        return *this;\n    }\n};'),('text','(b) a = 65, b = 12, c = 8, fee = 5, d = 17. += returns a reference to the same left object so the next += modifies that object again. Returning a new copy would not preserve that identity.'),('text','(c) In +=, this is Money*, *this denotes the current Money object, and cents is its int member. Returning cents cannot satisfy Money&. In +, cents + rhs.cents is int; Money{...} constructs the required result object. const on the return type does not replace trailing const: trailing const qualifies the member function and allows calling it on fee.'),('text','Syntax check: omit Money:: inside the struct. Use Money:: for an out-of-class definition only after declaring the member inside the class. Keep the two const positions separate: rhs is the right operand; trailing const concerns the left object.')])
add('A3','Abstract classes, dispatch and destruction',[
('code','struct Reader {\n    virtual int read() const = 0;\n    int label() const { return 4; }\n    virtual ~Reader() { cout << "R"; }\n};'),
('task','(a) Write FixedReader publicly derived from Reader. Override read to return 6, define label to return 9, and write a destructor that prints F. Use override only where valid.',180),
('task','(b) Explain why Reader x; is invalid. Given FixedReader s; Reader& r = s;, state r.read(), r.label(), s.label(). Do these method calls destroy s?',110),
('task','(c) In a separate run: Reader* p = new FixedReader; delete p;. Give the destructor output. If the base destructor is made nonvirtual (and override removed from the derived destructor), is delete p valid? Should you delete twice?',125)
],[('code','struct FixedReader : public Reader {\n    int read() const override { return 6; }\n    int label() const { return 9; }\n    ~FixedReader() override { cout << "F"; }\n};'),('text','(a) label is nonvirtual, so it cannot use override. read must retain the trailing const to match the pure virtual base method. The derived destructor may use override because the base destructor is virtual.'),('text','(b) Reader is abstract because read is pure virtual (= 0), not because a destructor exists. Results: 6, 4, 9. The calls do not destroy s. A local s is destroyed when its lifetime ends, normally at scope exit.'),('text','(c) Output is FR. One delete invokes the derived destructor, then the base destructor, and releases the allocation. With a nonvirtual base destructor, deleting a FixedReader through Reader* has undefined behavior. Deleting twice never repairs this. Deleting through a FixedReader* would correctly run both destructors even with a nonvirtual base destructor.')])
add('A4','Templates: distinguish deduction from conversion',[
('task','(a) Write template<typename T> T quarter(T x) returning x / 4. For auto a = quarter(11); auto b = quarter(11.0); double c = quarter(11); auto d = quarter<double>(11); state BOTH type and value.',180),
('code','template<typename T>\nT smaller(T a, T b) { return a < b ? a : b; }'),
('task','(b) Classify smaller(3, 2.5) and smaller<double>(3, 2.5). Explain the deduction issue; give the result type and value for the valid call.',115),
('task','(c) Write template<typename T> T twice(T x) returning x + x. Give type and value for twice(4) and twice(1.25). Explain why a double destination cannot restore the fraction lost in quarter(11).',140)
],[('code','template<typename T>\nT quarter(T x) { return x / 4; }\n\ntemplate<typename T>\nT twice(T x) { return x + x; }'),('text','(a) a: int 2; b: double 2.75; c: double 2.0; d: double 2.75. For d the explicit type converts 11 to double before division. For c the int division has already produced 2 before the assignment conversion.'),('text','(b) smaller(3, 2.5) fails deduction: the arguments propose int and double for one T. smaller<double>(3, 2.5) is valid and returns double 2.5. An explicit T permits argument conversion; deduction does not simply select a common floating-point type here.'),('text','(c) twice(4) returns int 8; twice(1.25) returns double 2.5. Integer division discards the fractional part during evaluation. Converting the resulting integer later cannot recover it. On the exam, write the type explicitly rather than using decimal notation alone.')])
add('B1','Const access, references and the arrow operator',[
('code','struct Box { int value; };\nBox a{21}, b{34};\nconst Box* p = &a;\nBox* const q = &a;'),
('task','(a) Independently classify: p = &b; p->value = 7; q = &b; q->value = 7; a.value = 7;. Explain whether a itself is const.',130),
('task','(b) Declare r so neither reseating r nor changing a through r is allowed. Write int readValue(...) taking a pointer with read-only access to a Box. Call it on a and store the returned int.',170),
('task','(c) Rewrite q->value using * and . . Explain how this differs from *q. After a.value = 99;, what does readValue(&a) return? Does reading through a const pointer freeze a?',130)
],[('text','(a) Valid, invalid, invalid, valid, valid. p can be reseated but cannot modify the Box through p. q always points to a, but may modify a. The original a is not const.'),('code','const Box* const r = &a;\n\nint readValue(const Box* p) {\n    return p->value;\n}\n// In the caller:\nint result = readValue(&a);\n// q->value is equivalent to (*q).value'),('text','(b) r has both const protections. readValue is a free function, so do not add trailing const. Return the int member, not the pointer. Pass &a, not the Box object itself.'),('text','(c) *q denotes the entire Box; (*q).value denotes its int member. After a.value = 99, readValue(&a) returns 99. Read-only access through one pointer does not prevent direct modification of the original non-const object.')])
add('B2','A zero is data, not an array terminator',[
('code','int values[] = {5, 0, -2, 9};\nint* end = values + 4;\nint total = 0;\nfor (int* p = values; *p != 0; ++p) {\n    total += *p;\n}'),
('task','(a) Give total for this exact code. Repair the loop to process all four elements using p != end. Give the corrected total and explain why zero must not stop it.',150),
('task','(b) Write int sum(const int a[], int n) using n. Handle n = 0 without reading a. Assume n >= 0 and a valid range for n > 0. For this part assume sizeof(int) = 4 and sizeof(const int*) = 8: give sizeof(a), sizeof(a[0]), and their quotient INSIDE sum.',180),
('task','(c) Classify forming end, reading *end, and reading *(end - 1). Explain why an int array does not automatically acquire a null terminator.',100)
],[('code','int total = 0;\nfor (int* p = values; p != end; ++p) {\n    total += *p;\n} // total is 12\n\nint sum(const int a[], int n) {\n    int total = 0;\n    for (int i = 0; i < n; ++i) total += a[i];\n    return total;\n}'),('text','(a) The original loop stops at values[1] and gives 5. The repaired loop includes the zero and negative value and gives 12. With an array containing no zero, the original stopping rule could instead read past the array; it has no general valid bound.'),('text','(b) The adjusted parameter type is const int*. With the stated assumptions, sizeof(a) = 8, sizeof(a[0]) = 4, quotient = 2, not the caller\'s array length 4. Use n. For n = 0 no elements are read.'),('text','(c) Forming end is valid. Reading *end has undefined behavior. *(end - 1) is valid and yields 9. Ordinary int arrays have no automatic sentinel element; a zero among the elements is simply a data value.')])
add('B3','Constructor initialization versus assignment',[
('code','struct Pass {\n    const int code;\n    static int created;\n    // Add constructor and getCode.\n};'),
('task','(a) Write Pass(int c), initializing code and incrementing created. Add getCode() callable on a const Pass. Define created outside the class, initially zero.',190),
('task','(b) Explain code(c) in the initializer list. Why is Pass(int c) { code = c; ++created; } invalid? Does getCode need to return a Pass object?',110),
('task','(c) Starting from created = 0, construct Pass a(31); const Pass b(42);. Give a.getCode(), b.getCode(), Pass::created. Explain why one shared static member is not a separate counter in each object.',130)
],[('code','struct Pass {\n    const int code;\n    static int created;\n    Pass(int c) : code(c) { ++created; }\n    int getCode() const { return code; }\n};\nint Pass::created = 0;'),('text','(b) code(c) initializes the int member code from parameter c before the constructor body. It is not a call to a function named code. A const member must be initialized; assigning it in the body is not permitted.'),('text','getCode returns int because code is an int. A member function does not automatically return the class type merely because it belongs to that class.'),('text','(c) The values are 31, 42 and 2. Both constructors increment the same static member. Trailing const allows getCode on b and constrains ordinary modification of the current object through this.')])
add('B4','Lifetime: an existing pointer can have a dead target',[
('code','int* makePointer() {\n    int x = 23;\n    return &x;\n}'),
('task','(a) For int* p = makePointer(); cout << *p;, explain exactly which object dies and when. Is the output guaranteed to be 23? Does assigning the pointer to p extend that object\'s lifetime?',150),
('task','(b) Rewrite the function and caller to safely return 23 by value. Then write int* alias(int& x) returning a pointer to a caller-owned int. Show one safe call and explain its lifetime.',190),
('task','(c) Independently: int* p = new int(23); int* q = p; delete p; p = nullptr;. Describe p and q. May you read *q or delete q? State the minimal local cleanup for q.',115)
],[('text','(a) The local automatic int x dies as makePointer exits. p receives a pointer to that expired object; keeping the pointer does not keep x alive. Reading *p is undefined behavior, not a guaranteed 23. A warning is possible; this need not be a compilation error.'),('code','int makeValue() { return 23; }\nint* alias(int& x) { return &x; }\n\n// In the caller:\nint value = makeValue();\nint n = 23;\nint* observed = alias(n);\ncout << *observed; // valid while n is alive'),('text','(b) alias refers to the caller\'s int; it does not create a new local int target. That target survives the return. (c) p is null and q dangles. Neither reading *q nor deleting it again is valid. Assign q = nullptr; to clear that alias. Clearing q does not recreate the destroyed allocation.')])
add('B5','Strings: bytes, characters and safe replacement',[
('code','char text[] = "Sun";\nstring word = "Sun";'),
('task','(a) Give sizeof(text), strlen(text), and the minimum char-array capacity needed for "Moon". Explain why strcpy(text, "Moon") is unsafe.',110),
('task','(b) Write a safe fixed-size char array containing "Moon". Replace word with "Moon" using std::string. Give word.substr(1, 2) and say whether substr changes word.',150),
('task','(c) Classify "Good" + "!", string("Good") + "!", and "Good" + string("!"). Give strcmp("Sun", "Sun"). Explain why a null-terminated C-string loop is different from a bounded int-array loop.',160)
],[('text','(a) sizeof(text) = 4, strlen(text) = 3. Moon needs five char slots, including the null terminator. strcpy cannot resize the four-element destination; that copy would overflow.'),('code','char safe[5] = "Moon";\nword = "Moon";\nstring middle = word.substr(1, 2); // "oo"'),('text','(b) substr returns a separate string and does not change word. Its second argument is a count, not an ending index.'),('text','(c) Two string literals cannot be joined with operator+ directly. The two expressions with a std::string operand are valid and produce "Good!". strcmp of equal strings returns 0. A valid C-string supplies a null terminator within accessible storage; an arbitrary int array supplies no such guarantee and may contain zero as ordinary data.')])
add('B6','Streams: remaining input and formatting state',[
('code','istringstream in("32\\nMai Wong\\n");\nint id;\nstring first, name;\nin >> id;\ngetline(in, first);\ngetline(in, name);\nostringstream out;\nout << fixed << setprecision(2) << setfill(\'_\');\nout << setw(6) << 7.5 << \'|\' << 1.0;'),
('task','(a) State id, first, name and out.str(). Explain the first getline result. Which of width, fill, fixed and precision persist after inserting 7.5?',120),
('task','(b) With fresh input "32\\nMai Wong\\n", write code reading id and then the complete name using one getline. Discard the remaining id line explicitly.',110),
('task','(c) For istringstream nums("4 6 x 8"); int n, total=0; while(nums >> n) total += n;, give total at failure. Write code to clear the failure, consume the single x and conditionally add the remaining integer. Explain why clear alone is insufficient.',160)
],[('text','(a) id = 32; first is empty; name is "Mai Wong"; out.str() is "__7.50|1.00". Integer extraction leaves a newline, which the first getline consumes as its delimiter. 7.50 has four characters, so width 6 adds two underscores. This insertion resets width; fill, fixed and precision persist.'),('code','// Fresh input stream:\nin >> id;\nin.ignore(numeric_limits<streamsize>::max(), \'\\n\');\ngetline(in, name);\n\n// After the failed numeric loop:\nnums.clear();\nchar bad;\nnums >> bad;\nif (nums >> n) total += n;'),('text','(b) Include <limits> for numeric_limits. ignore consumes through the newline; the one getline reads the full name.'),('text','(c) total is 10 at failure, then 18 after successful recovery. clear resets flags but does not consume x. Attempting another integer read without removing x would fail again. sizeof(n) measures its type\'s storage, not whether the next input character is numeric.')])

for name,file in [('Text','Times New Roman.ttf'),('Code','Courier New Bold.ttf'),('Sans','Arial.ttf'),('Heading','Arial Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
W,H=A4;L=54;width=W-108
body=ParagraphStyle('body',fontName='Text',fontSize=12,leading=15)
head=ParagraphStyle('head',fontName='Heading',fontSize=13,leading=17)
output=R/'output/pdf/2026_CPP_Midterm_Review_Set_2.pdf'
c=canvas.Canvas(str(output),pagesize=A4);c.setTitle('CSC3002 Midterm Review - Set 2');c.setAuthor('Personalized C++ practice')
page=0;y=0;TOTAL=1+2*len(D)
def para(t,heading=False):
 global y
 p=Paragraph(escape(t),head if heading else body);_,h=p.wrap(width,1000)
 assert y-h>=50,(page,t,y)
 p.drawOn(c,L,y-h);y-=h+9

def code(t):
 global y
 c.setFont('Code',11)
 for line in t.splitlines():
  assert pdfmetrics.stringWidth(line,'Code',11)<=width-14,(page,line)
  assert y-14>=50
  c.drawString(L+7,y-11,line);y-=14
 y-=9

def new(label):
 global page,y
 if page:c.showPage()
 page+=1;y=H-76
 c.setFont('Sans',9);c.drawString(L,H-34,'The Chinese University of Hong Kong, Shenzhen');c.drawRightString(W-L,H-34,'CSC3002 | REVIEW SET 2')
 c.drawString(L,H-52,label)
 c.setFont('Sans',10);c.drawCentredString(W/2,25,f'Page {page} of {TOTAL}')

new('PERSONALIZED PRACTICE | QUESTIONS FIRST, SOLUTIONS LAST')
para('Midterm review - fresh practice, Set 2',True)
para('Built around your recent written answers: function calls versus pointers, Money return types, abstract classes versus destructors, const access, and bounded array traversal.')
para('Part A: explicit TA-note priorities',True)
para('A1 Callback repair (p. 2); A2 Money operators (p. 3); A3 Abstract interfaces and destruction (p. 4); A4 Function templates (p. 5). The topics follow your TA notes; these particular exercises are newly written practice, not confirmed exam questions.')
para('Part B: supporting practice - exam inclusion not confirmed',True)
para('B1 Const pointers and -> (p. 6); B2 Array bounds and sizeof (p. 7); B3 Constructors/static members (p. 8); B4 Lifetime (p. 9); B5 Strings (p. 10); B6 Streams (p. 11). These address observed mistakes and broader revision. Supporting classification does not mean the TA excluded a topic.')
para('How to practise',True)
para('Use C++17, required standard headers and using namespace std. Assume small arithmetic does not overflow and allocations succeed. No numerical memory addresses are requested. This is a targeted review, not a 100-point mock examination.')
para('Attempt pages 2-11 without the solutions. Write full function definitions where requested. For every output question, state both type and value when asked. Mark invalid code as a compilation error or undefined behavior as appropriate.')
para('Solutions begin on page 12',True)
para('Each solution uses the same question ID. Compare your explanation as well as your final value. For partial self-checking, distinguish: wrong concept, invalid declaration, missing answer, or incorrect trace.')
para('Evidence for priorities: your C++ Concept Review.md TA notes and the marked mock/interactive submissions in this conversation. Supplementary topics are retained for learning, not presented as new TA predictions.')
for d in D:
 new('PART A | TA-EMPHASIZED TOPICS' if d['id'].startswith('A') else 'PART B | SUPPLEMENTARY - EXAM INCLUSION NOT CONFIRMED')
 para(d['id']+'. '+d['title'],True)
 for part in d['parts']:
  if part[0]=='code':code(part[1])
  else:
   para(part[1]);h=part[2];assert y-h>=50,(page,'box',y,h)
   c.setLineWidth(.65);c.rect(L,y-h,width,h);y-=h+15
for d in D:
 new('SOLUTIONS | '+('TA-EMPHASIZED TOPIC' if d['id'].startswith('A') else 'SUPPLEMENTARY - EXAM INCLUSION NOT CONFIRMED'))
 para(d['id']+'. '+d['title'],True)
 for kind,t in d['answers']:(code if kind=='code' else para)(t)
assert page==TOTAL
c.save()
(R/'Exam Prep/Midterm/2026_CPP_Midterm_Review_Set_2.json').write_text(json.dumps(D,indent=2))
print(output, TOTAL,'pages')
