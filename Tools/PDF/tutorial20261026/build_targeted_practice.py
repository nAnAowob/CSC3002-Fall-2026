from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[3]
D=[]
def add(title, intro, parts, answer): D.append(dict(title=title,intro=intro,parts=parts,answer=answer))
add('Const pointers: what is protected?',
'Consider each statement independently, starting from the declarations below.',[
('code','int a = 12, b = 30;\nconst int* p = &a;\nint* const q = &a;'),
('task','(a) Mark each as valid or invalid and explain what is const: p = &b; *p = 7; q = &b; *q = 7; a = 7;',120),
('task','(b) Write a declaration of r that prevents both reseating r and changing a through r. Initialize r to point to a.',80),
('task','(c) Write int readValue(...) taking a pointer through which the int cannot be modified. Return the pointed-to value; assume the pointer is valid. Explain whether the caller may still modify a directly.',130)
], [('text','(a) Valid, invalid, invalid, valid, valid. p points to const int: modification through p is forbidden, but p can be reseated. q is a const pointer to mutable int: q cannot be reseated, but *q can be modified. a itself is not const.'),('code','const int* const r = &a;\n\nint readValue(const int* p) {\n    return *p;\n}'),('text','(b) Both pointer and pointed-to access are const. (c) The caller may still assign to a directly. const access through one pointer does not make the original non-const object immutable.')])
add('Constructor initialization and static state',
'Complete the class below. Do not change the member declarations.',[
('code','struct Ticket {\n    const int code;\n    static int created;\n    // Constructor and getCode go here.\n};'),
('task','(a) Write Ticket(int c) using a member initializer list. Increment created in the body. Write getCode(), callable on const Ticket, and define created outside the class with initial value zero.',190),
('task','(b) Explain why code(c) is not a function call here. Why does code = c inside the constructor body fail?',100),
('task','(c) For Ticket a(9); const Ticket b(14); write a.getCode(), b.getCode(), and Ticket::created. Is created stored separately in each object?',80)
], [('code','struct Ticket {\n    const int code;\n    static int created;\n    Ticket(int c) : code(c) { ++created; }\n    int getCode() const { return code; }\n};\nint Ticket::created = 0;'),('text','(b) code(c) initializes the data member code from parameter c before the constructor body runs. It does not call a function named code. Assignment in the body is too late for a const member; initialization and assignment are different operations.'),('text','(c) The values are 9, 14, and 2. created is one shared static member. getCode returns int, matching the type of code; trailing const qualifies the member function, not its return type.')])
add('Function pointers: pass a rule into a loop',
'Write complete definitions. Use the supplied predicate inside countIf, rather than hard-coding a particular test.',[
('task','(a) Write bool isPositive(long x). Declare an explicitly typed function-pointer variable test, initialized to isPositive. Explain the difference between isPositive and isPositive(5).',125),
('code','int countIf(const long* a, int n,\n            bool (*pred)(long));'),
('task','(b) Implement countIf. Assume n >= 0, pred is valid, and a refers to n valid elements when n > 0. It must return zero for n = 0.',180),
('task','(c) For {-3, 0, 4, 7}, call countIf using test and state the result. Then write isEven(long) and call the SAME countIf to count even values. State that result, too.',120)
], [('code','bool isPositive(long x) { return x > 0; }\nbool (*test)(long) = isPositive;\n\nint countIf(const long* a, int n,\n            bool (*pred)(long)) {\n    int count = 0;\n    for (int i = 0; i < n; ++i) {\n        if (pred(a[i])) ++count;\n    }\n    return count;\n}\n\nbool isEven(long x) { return x % 2 == 0; }\nlong data[] = {-3, 0, 4, 7};\n// countIf(data, 4, test)   returns 2\n// countIf(data, 4, isEven) returns 2'),('text','isPositive names the function and converts to a function pointer in this initialization. isPositive(5) calls the function and yields a bool. test and pred are pointer variables; count is the integer counter. pred(a[i]) calls the chosen function on one element. (*pred)(a[i]) is equivalent. Zero is even.')])
add('Object lifetime and dangling pointers',
'Classify behavior without inventing numerical memory addresses.',[
('code','int* makeBad() {\n    int value = 11;\n    return &value;\n}\nint* q = makeBad();\ncout << *q;'),
('task','(a) Explain when value begins and ends its lifetime, what q stores, and why reading *q has no guaranteed output. Is this necessarily a compilation error?',135),
('task','(b) Rewrite makeBad and the caller so the caller safely receives the number by value. Do not allocate dynamically.',100),
('task','(c) Write int* identity(int& x) returning a pointer to x. Use it with an int in main and print through the pointer while that int is alive. Explain why this differs from makeBad.',145)
], [('text','(a) value is an automatic local object. Its lifetime ends when makeBad exits. q receives a pointer to that expired object, not a copy of the int. q itself can still exist while its pointee is dead: that makes it dangling. Dereferencing it has undefined behavior. A compiler may warn; this need not be rejected as a compilation error.'),('code','int makeGood() {\n    int value = 11;\n    return value;\n}\n// In main:\nint answer = makeGood();\ncout << answer; // 11\n\nint* identity(int& x) { return &x; }\n// In main:\nint n = 11;\nint* p = identity(n);\ncout << *p; // 11'),('text','(c) x refers to the caller\'s n; it does not create a separate local int. Returning from identity does not end n\'s lifetime. The pointer remains usable while n remains alive. A pointer never extends the lifetime of its target by itself.')])
add('Money operators: types, const and *this',
'Use member operators. Assume integer sums do not overflow.',[
('code','struct Money {\n    int cents;\n    // Implement both operators here.\n};'),
('task','(a) Implement operator+ and operator+=. Both take a const-reference right operand. + must work on a const left operand and return a new Money without modifying inputs. += must modify the left operand and support chaining.',225),
('task','(b) Explain why return cents + rhs; and return cents + rhs.cents; do not work in this operator+. Explain what this and *this denote, and why += returns *this.',130),
('task','(c) Start with Money a{80}, b{15}, c{5}; then Money d = a + b; and (a += b) += c;. Give final cents for a, b, c, d. Does Money const operator+(...) replace trailing const?',80)
], [('code','struct Money {\n    int cents;\n    Money operator+(const Money& rhs) const {\n        return Money{cents + rhs.cents};\n    }\n    Money& operator+=(const Money& rhs) {\n        cents += rhs.cents;\n        return *this;\n    }\n};'),('text','(b) cents is int; rhs is a Money object accessed through a const reference. int + Money has no matching operator in this class. cents + rhs.cents is int, but this class has no implicit conversion from int to Money. Money{...} initializes a new Money with the sum.'),('text','In +=, this points to the left object and *this denotes that object. Returning *this with return type Money& returns a reference to the same object, allowing another += to modify it. It is not a reference to a newly created local result.'),('text','(c) a = 100, b = 15, c = 5, d = 95. Money const as a return type qualifies the returned value. Trailing const qualifies the member function and allows calls on const left operands. These are not interchangeable.')])
add('Abstract interfaces and exact overrides',
'Use this interface. tag is deliberately nonvirtual.',[
('code','struct Reporter {\n    virtual int report() const = 0;\n    int tag() const { return 1; }\n    virtual ~Reporter() = default;\n};'),
('task','(a) Write QuietReporter publicly derived from Reporter. report returns 0; tag returns 9. Use override where appropriate. Why can Reporter itself not be instantiated?',165),
('task','(b) Given QuietReporter s; Reporter& r = s;, write the results of r.report(), r.tag(), and s.tag(). Explain which calls depend on dynamic object type.',110),
('task','(c) Explain why const int report() does not override the required method. Explain the purpose of the virtual destructor when deleting a QuietReporter through Reporter*. Can derived code directly access private base members?',125)
], [('code','struct QuietReporter : public Reporter {\n    int report() const override { return 0; }\n    int tag() const { return 9; }\n};'),('text','(a) Reporter has a pure virtual report and is abstract. A shared interface lets callers use different derived implementations through the same base reference or pointer.'),('text','(b) The results are 0, 1, 9. report is virtual: r.report() chooses the final override for the dynamic object, QuietReporter. tag is nonvirtual: r.tag() uses Reporter::tag, while s.tag() uses QuietReporter::tag.'),('text','(c) const int report() places const on the return type and lacks the required trailing const. It does not provide the required override; adding override exposes the mismatch as an error. The virtual destructor supports correct destruction through the base pointer. Derived methods cannot directly access private base members merely because they inherit from the base.')])
add('Array parameters and one-past boundaries',
'Assume every pointer passed to sum refers to at least n elements when n > 0.',[
('code','int sum(const int a[], int n);'),
('task','(a) Implement sum using the explicit length. It must handle n = 0. Explain why sizeof(a) / sizeof(a[0]) inside this function cannot recover the caller\'s array length.',180),
('code','int values[] = {2, 4, 6, 8};\nint* end = values + 4;'),
('task','(b) Classify independently: forming values + 4; reading *end; reading *(end - 1). Give a value only where the read is valid.',100),
('task','(c) Rewrite the sum loop using a pointer p and the condition p != end. Use the four-element values array above. Never dereference the one-past pointer.',145)
], [('code','int sum(const int a[], int n) {\n    int total = 0;\n    for (int i = 0; i < n; ++i) total += a[i];\n    return total;\n}\n\nint values[] = {2, 4, 6, 8};\nint* end = values + 4;\nint total = 0;\nfor (const int* p = values; p != end; ++p) {\n    total += *p;\n} // total is 20'),('text','(a) An array parameter is adjusted to a pointer parameter. sizeof(a) is therefore the size of a pointer, not the original array. The explicit n gives the loop its bound.'),('text','(b) Forming the one-past pointer is valid. Reading *end has undefined behavior. Reading *(end - 1) is valid and yields 8. The loop in (c) tests before dereferencing, so it never reads through end.')])
add('C-strings: capacity, terminators and concatenation',
'Assume the standard string and C-string headers are available.',[
('code','char label[] = "Go";\nstring word = "Go";'),
('task','(a) State sizeof(label), strlen(label), and the minimum char-array capacity needed for "Blue". Explain why strcpy(label, "Blue") is unsafe.',110),
('task','(b) Write a safe fixed-size char array containing "Blue". Then write a std::string version initially containing "Go" and replace its contents with "Blue".',125),
('task','(c) Classify each independently and give the result when valid: "Hi" + "!"; string("Hi") + "!"; "Hi" + string("!"); strcmp("Go", "Go"). Explain why strcpy does not resize label.',145)
], [('text','(a) sizeof(label) = 3, strlen(label) = 2, and Blue needs capacity 5 including the null terminator. Copying it into label overflows the three-element array.'),('code','char safe[5] = "Blue";\n\nstring text = "Go";\ntext = "Blue";'),('text','(c) "Hi" + "!" is invalid: there is no operator+ joining two string literals this way. string("Hi") + "!" and "Hi" + string("!") are valid and yield "Hi!". strcmp("Go", "Go") returns zero, indicating equal contents. strcpy copies characters into existing storage; it does not allocate or resize the destination.')])
add('Ownership: raw aliases and smart pointers',
'Consider each subpart independently. All allocations succeed.',[
('code','int* p = new int(6);\nint* q = p;\ndelete p;\np = nullptr;'),
('task','(a) Describe p and q after these statements. May you read *q or delete q? Write a version that clears both local aliases after one deletion.',115),
('code','auto s = make_shared<int>(6);\nweak_ptr<int> w = s;'),
('task','(b) Give s.use_count(). Write code using w.lock() to print the value only if it is still alive. Then explain w.expired() after s.reset(), assuming no other shared_ptr survives.',135),
('task','(c) Write code that creates a unique_ptr<int>, transfers ownership to another unique_ptr, and checks that the source is empty. Also state the matching deletion for new int[1], and explain why copying an owning raw pointer is not a deep copy.',145)
], [('text','(a) p is null; q dangles. Reading *q or deleting q again has undefined behavior. Assigning nullptr to p does not change the separate pointer variable q.'),('code','int* p = new int(6);\nint* q = p;\ndelete p;\np = nullptr;\nq = nullptr;\n\nauto s = make_shared<int>(6);\nweak_ptr<int> w = s; // use_count is 1\nif (auto owner = w.lock()) {\n    cout << *owner;\n} // temporary strong owner ends here\ns.reset(); // w.expired() is now true\n\nauto first = make_unique<int>(6);\nauto second = std::move(first);\nif (!first) cout << "empty";'),('text','(b) weak_ptr does not add a strong owner. lock obtains a shared_ptr if the object is still alive. (c) unique_ptr ownership is moved, not copied. new int[1] requires delete[] even though there is only one element. Copying a raw pointer copies the pointer value; it does not allocate or copy the pointee.')])
add('Streams: exact output and persistent formatting',
'Write exact characters, including underscores and decimal zeros.',[
('code','istringstream in("18\\nLin Chen\\n");\nint id;\nstring first, name;\nin >> id;\ngetline(in, first);\ngetline(in, name);\nostringstream out;\nout << fixed << setprecision(2);\nout << setfill(\'_\') << setw(7) << 4.5;\nout << \'|\' << 8.0;\ncout << id << ":[" << first << "]\\n";\ncout << \'[\' << name << "]\\n";\ncout << out.str() << \'\\n\';'),
('task','(a) Write all three output lines. Explain the first getline result and count the padding characters.',125),
('task','(b) State which persist after printing 4.5: width, fill, fixed, precision. Does out.str() alone print or empty the stream?',85),
('task','(c) Rewrite the input section to read id and then the full name into name using ONE getline. Discard the rest of the id line with ignore and numeric_limits.',100)
], [('code','18:[]\n[Lin Chen]\n___4.50|8.00'),('text','(a) Formatted integer extraction leaves the newline unread. The first getline consumes that delimiter and returns an empty string. 4.50 has four characters, so width 7 adds three underscores.'),('text','(b) This numeric insertion resets width. Fill, fixed, and precision persist. out.str() returns the string contents; the getter alone neither prints nor clears the buffer.'),('code','in >> id;\nin.ignore(numeric_limits<streamsize>::max(), \'\\n\');\ngetline(in, name);'),('text','(c) Apply this replacement to a fresh stream with the original input. Include <limits> for numeric_limits. ignore consumes the rest of the id line including its newline; getline then reads the complete name.')])
add('Recover from failed numeric input',
'The input contains exactly one nonnumeric character between valid integers.',[
('code','istringstream numbers("5 15 x 25");\nint n, total = 0;\nwhile (numbers >> n) total += n;'),
('task','(a) State total after the loop and identify the unread character blocking the next integer extraction. Why does the loop body not process x?',100),
('task','(b) Write the recovery: reset the error flags, consume the one bad character, and add the remaining integer only if extraction succeeds. Give the new total.',180),
('task','(c) Explain why clear() alone is insufficient. Explain why sizeof(n) != 4 cannot identify bad input, and why casting n to int cannot repair a failed stream.',115)
], [('text','(a) total is 20. Extraction encounters x, fails, and the loop condition is false. x remains unread; the loop body is not entered for the failed extraction.'),('code','numbers.clear();\nchar bad;\nnumbers >> bad;\nif (numbers >> n) {\n    total += n;\n}\n// total is 45'),('text','(b) clear resets error flags, and extraction into char consumes x (skipping preceding whitespace). The guarded integer read then adds 25.'),('text','(c) clear does not remove unread input. Without consuming x, the next integer extraction fails again. sizeof(n) reports the storage size of type int, which is unrelated to the characters in the stream and is not universally four bytes. Casting an int to int does not reset stream state or remove x.')])
add('Templates and iterators: transfer check',
'Write code and explain types. Do not assume a double destination changes earlier arithmetic.',[
('task','(a) Write template<typename T> T third(T x) returning x / 3. For auto a = third(8); auto b = third(9.0); double c = third(8); auto d = third<double>(9); give each type and value.',160),
('code','template<typename T>\nT larger(T a, T b) { return a > b ? a : b; }\nvector<int> v{2, 5, 8};'),
('task','(b) Explain why larger(2, 2.5) fails deduction. Write a call with an explicit template argument that accepts both values and give its result.',85),
('task','(c) Write one range-for loop that adds 3 to each actual vector element. Contrast it with the same loop using a copied variable. Write an iterator loop that prints all elements without dereferencing end(). Give the modified vector.',155)
], [('code','template<typename T>\nT third(T x) { return x / 3; }'),('text','(a) a: int, 2. b: double, 3.0. c: double, 2.0. d: double, 3.0. For c, int division truncates before the result is converted to double. An explicit double template argument converts the integer argument before the function arithmetic.'),('code','larger<double>(2, 2.5); // returns 2.5\n\nfor (auto& x : v) x += 3;\n// v is now {5, 8, 11}\n\nfor (auto it = v.begin(); it != v.end(); ++it) {\n    cout << *it << \' \';\n}'),('text','(b) Deduction from the two arguments proposes conflicting types int and double for the same T. (c) auto& binds to each element; auto alone makes a copy, so modifying that copy leaves v unchanged. end() denotes the position past the last element, not the last element itself.')])

# Separate explicit TA-note priorities from supporting/broader practice.
original = D[:]
templates = dict(original[11])
templates['title'] = 'Function templates: write, deduce and trace'
templates['parts'] = [
 ('task', '(a) Write template<typename T> T third(T x) returning x / 3. For auto a = third(8); auto b = third(9.0); double c = third(8); auto d = third<double>(9); give each type and value.', 160),
 ('code', 'template<typename T>\nT larger(T a, T b) { return a > b ? a : b; }'),
 ('task', '(b) Explain why larger(2, 2.5) fails deduction. Write a call with an explicit template argument that accepts both values and give its result.', 100),
 ('task', '(c) Write template<typename T> T addOne(T x). Return x + 1. Give the type and value of addOne(4) and addOne(1.5). Explain why assigning third(8) to a double cannot recover the discarded fraction.', 145)]
templates['answer'] = original[11]['answer'][:2] + [
 ('code', 'larger<double>(2, 2.5); // returns 2.5\n\ntemplate<typename T>\nT addOne(T x) { return x + 1; }'),
 ('text', '(b) Deduction proposes conflicting types int and double for the same T. Explicitly choosing double permits conversion of the int argument. (c) addOne(4) returns int 5; addOne(1.5) returns double 2.5. third(8) performs int division first; converting its result to double produces 2.0, not the original fraction.')]
D = []
add('Optional standard-library vector and iteration',
    'Supplementary only. std::vector<int> is an exercise choice, not a confirmed TA exam clue. Lecture 9 uses capital-V Vector examples; do not assume the two APIs are identical.', [
 ('code', 'std::vector<int> v{2, 5, 8};'),
 ('task', '(a) Write a range-for loop adding 3 to each actual element. Give the resulting vector. Explain the difference between auto x and auto& x.', 160),
 ('task', '(b) Starting again from {2, 5, 8}, write an iterator loop printing each element. Explain why end() must not be dereferenced.', 150),
 ('task', '(c) Rewrite the traversal using int values[] = {2, 5, 8}; and a pointer. Use values + 3 as the stopping boundary and never read through it.', 140)], [
 ('code', 'for (auto& x : v) x += 3;\n// v becomes {5, 8, 11}\n\n// With a fresh v{2, 5, 8}:\nfor (auto it = v.begin(); it != v.end(); ++it) {\n    cout << *it << ' ';\n}\n\nint values[] = {2, 5, 8};\nfor (int* p = values; p != values + 3; ++p) {\n    cout << *p << ' ';\n}'),
 ('text', 'auto& refers to the element; auto alone makes a copy. end() and values + 3 denote one-past positions. Compare against them, but do not read through them. Both fresh traversals print 2 5 8. This exercise does not establish standard-library vector as an exam topic.')])
iterator = D[0]
core = [original[2], original[4], original[5], templates]
supplement = [original[j] for j in [0, 1, 3, 6, 7, 8, 9, 10]] + [iterator]
D = core + supplement
for j, d in enumerate(D):
 d['section'] = 'A' if j < len(core) else 'B'
 d['id'] = f"A{j+1}" if j < len(core) else f"B{j-len(core)+1}"

for name,file in [('Text','Times New Roman.ttf'),('Bold','Times New Roman Bold.ttf'),('Code','Courier New Bold.ttf'),('Sans','Arial.ttf'),('Heading','Arial Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
W,H=A4; L=54; width=W-2*L
style=ParagraphStyle('body',fontName='Text',fontSize=12,leading=15)
heading=ParagraphStyle('heading',fontName='Heading',fontSize=13,leading=17)
def build(solution=False):
 suffix='Solutions' if solution else 'Questions'
 path=R/f'output/pdf/2026_Targeted_CPP_Practice_{suffix}.pdf'
 c=canvas.Canvas(str(path),pagesize=A4);c.setTitle('CSC3002 Targeted C++ Practice - '+suffix)
 def para(t,head=False):
  nonlocal y
  p=Paragraph(escape(t),heading if head else style);_,h=p.wrap(width,1000)
  assert y-h>=51,(suffix,i,'text overflow',y,t)
  p.drawOn(c,L,y-h);y-=h+9
 def code(t):
  nonlocal y
  c.setFont('Code',11)
  for line in t.splitlines():
   assert pdfmetrics.stringWidth(line,'Code',11)<=width-14,(i,line)
   assert y-14>=51,(i,'code overflow')
   c.drawString(L+7,y-11,line);y-=14
  y-=9
 # A separate guide avoids shrinking the established handwriting spaces.
 i=0; y=H-72
 c.setFont('Sans',9);c.drawString(L,H-34,'The Chinese University of Hong Kong, Shenzhen');c.drawRightString(W-L,H-34,'CSC3002 | PRACTICE')
 c.setFont('Sans',10);c.drawCentredString(W/2,25,f'{suffix} - Page 1 of {len(D)+1}')
 para('Targeted C++ practice - study priorities', True)
 para('Revised to separate explicit TA-note priorities from supplementary revision. These are original practice exercises, not confirmed exam questions.')
 para('Part A: TA-emphasized topics - do these first', True)
 para('A1 Function pointers and callbacks (page 2). A2 Operator overloading, const and return types (page 3). A3 Abstract interfaces and virtual functions (page 4). A4 Writing and tracing function templates (page 5).')
 para('Evidence: your C++ Concept Review.md notes explicitly emphasize writing function pointers, understanding virtual/abstract interfaces, writing operators and explaining const, and writing/tracing function templates. The specific exercises and callback counting task were designed for practice.')
 para('Part B: supplementary - exam inclusion not confirmed', True)
 para('B1 Const pointers; B2 Constructor initialization/static state; B3 Lifetime; B4 Array bounds; B5 Strings; B6 Ownership; B7 Stream formatting; B8 Stream recovery; B9 Optional std::vector/iteration (pages 6-14).')
 para('These address your questions and earlier mistakes, or broader lecture material. Some support Part A and some appear in tutorial material, but that does not confirm their exam inclusion. This label does not mean the TA excluded them.')
 para('If time is short, finish A1-A4 first. Use B1-B2 when const or initialization blocks your understanding of A2. Treat B9 as optional: Lecture 9 uses capital-V Vector examples; std::vector<int> was my supplementary exercise choice.')
 para('How to use this booklet', True)
 para('Assume C++17, required standard headers, and using namespace std unless qualified. No numerical memory addresses are requested. Write complete code and explain requested reasoning. Questions and solutions use matching A/B identifiers. This is targeted practice, not a timed or scored mock exam.')
 para('Sources for the distinction: C++ Concept Review.md (your TA notes); tutorial review photographs as summarized in 2026-10-26_Tutorial_Review.md; Lectures/9-CSC3002_Template and Iterator.pdf (broader iteration coverage).')
 c.showPage()
 for i,d in enumerate(D,1):
  y=H-72
  c.setFont('Sans',9);c.drawString(L,H-34,'The Chinese University of Hong Kong, Shenzhen');c.drawRightString(W-L,H-34,'CSC3002 | PRACTICE')
  c.setFont('Sans',10);c.drawCentredString(W/2,25,f'{suffix} - Page {i+1} of {len(D)+1}')
  c.setFont('Sans',9)
  c.drawString(L,H-52, 'PART A | TA-EMPHASIZED TOPICS - PRIORITY PRACTICE' if d['section']=='A' else 'PART B | SUPPLEMENTARY - EXAM INCLUSION NOT CONFIRMED')
  para(f'{d["id"]}. {d["title"]}',True)
  if solution:
   for kind,t in d['answer']:(code if kind=='code' else para)(t)
  else:
   para(d['intro'])
   for part in d['parts']:
    if part[0]=='code':code(part[1])
    else:
     para(part[1]); h=part[2]
     assert y-h>=51,(i,'box overflow',y,h)
     c.setLineWidth(.65);c.rect(L,y-h,width,h);y-=h+15
  c.showPage()
 c.save();print(path)
build();build(True)
# Keep the editable question and solution content with the generator.
import json
(R/'Exam Prep/Midterm/2026_Targeted_CPP_Practice.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
