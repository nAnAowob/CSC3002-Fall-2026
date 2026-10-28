from pathlib import Path
from PIL import Image as PI
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parents[3]; T=R/'Archive/Temporary Files/pdfs/scope'; O=R/'Exam Prep/Midterm'; O.mkdir(exist_ok=True,parents=True)
for n,f in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Mono','Courier New.ttf')]: pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
navy=colors.HexColor('#17324d');teal=colors.HexColor('#087e8b');gray=colors.HexColor('#526273')
W,H=A4
styles={
'b':ParagraphStyle('b',fontName='Body',fontSize=10,leading=14,spaceAfter=9,textColor=navy),
'h':ParagraphStyle('h',fontName='Bold',fontSize=21,leading=25,spaceAfter=15,textColor=navy),
's':ParagraphStyle('s',fontName='Bold',fontSize=12,leading=16,spaceBefore=8,spaceAfter=7,textColor=teal),
'c':ParagraphStyle('c',fontName='Body',fontSize=9,leading=12,spaceAfter=5,textColor=navy),
'code':ParagraphStyle('code',fontName='Mono',fontSize=9,leading=12,spaceAfter=9,backColor=colors.HexColor('#eef3f6'),borderPadding=7)}
def p(t,k='b'):return Paragraph(t,styles[k])
def footer(c,d=None):
 c.setStrokeColor(teal);c.line(44,38,W-44,38);c.setFont('Body',8);c.setFillColor(gray);c.drawString(44,25,'CSC3002 | Midterm practice from the 2021 Spring final');c.drawRightString(W-44,25,str(c.getPageNumber()))
# Faithful image crops of original question content, including split questions.
crops={1:[(2,127,191)],2:[(2,191,255)],3:[(2,255,343)],4:[(2,343,432)],5:[(2,432,483)],6:[(2,483,572)],7:[(2,572,637)],9:[(2,715,777)],10:[(3,77,165)],11:[(3,229,345)],12:[(3,345,434)],14:[(3,562,688)],15:[(3,688,777),(4,77,142)],17:[(4,454,632)],20:[(5,314,430)],21:[(5,504,605)],22:[(5,605,719)],23:[(5,719,758),(6,77,142)],24:[(6,144,236)],25:[(6,236,325)],26:[(6,325,439)],27:[(6,439,555)],30:[(7,209,635)],31:[(7,700,775),(8,77,298)],32:[(8,302,744)]}
for q,parts in crops.items():
 out=[]
 for page,y1,y2 in parts:
  im=PI.open(T/f'source-{page}.png');s=im.height/842.04
  out.append(im.crop((round(49*s),round(y1*s),round(552*s),round(y2*s))))
 target=PI.new('RGB',(max(i.width for i in out),sum(i.height for i in out)), 'white');y=0
 for im in out:target.paste(im,(0,y));y+=im.height
 target.save(T/f'q{q}.png')
c=canvas.Canvas(str(O/'CSC3002_2021_Final_Midterm_Questions.pdf'),pagesize=A4)
c.setTitle('CSC3002 - 2021 final questions matching Lectures 1-9')
def title(t,sub):
 c.setFillColor(navy);c.setFont('Bold',18);c.drawString(44,H-54,t)
 ob=p(sub,'c');_,h=ob.wrap(W-88,100);ob.drawOn(c,44,H-70-h);return H-82-h
def question(q,y):
 im=PI.open(T/f'q{q}.png');w=W-88;h=im.height/im.width*w
 assert y-h>48,(q,y,h)
 c.drawImage(str(T/f'q{q}.png'),44,y-h,width=w,height=h);return y-h-5
pages=[('Core practice | True / false','Scope: Lectures 1-9 in your Midterm folder, consistent with your existing revision guide. No separate official midterm notice was found. Original question numbers and wording are preserved. Choose a = True or b = False. Historical exam rules and marks are not current midterm instructions.',[1,2,3,4,5,6,7]),('Core practice | Short questions','Q9: true / false. Q11, Q12, Q14 and Q15: choose ONE option. Q15 has been joined across its original page break.',[9,11,12,14,15]),('Core practice | Concepts','Q20: choose ONE option. Q21, Q22, Q24 and Q25: choose one or more options.',[20,21,22,24,25]),('Core practice | Memory and classes','Q26, Q27 and Q30: choose one or more options. Q30 tests which function a base-class pointer calls.',[26,27,30]),('Core practice | Pointer tracing','Q31 has been joined across its original page break. Preserve the exact printed output, including line breaks. Use the remaining space for a trace table.',[31]),('Core practice | Array addresses','Q32: the first entry is already supplied in the original, leaving 12 blanks. Distinguish pointer addresses from numeric element values. Workings can go below.',[32]),('Optional | Confirm coverage first','These are related to the lectures but not firmly supported as core scope: Q10 (functional programming), Q17 (bit masks; operators appear in precedence tables), Q23 (Stanford-library-specific range-for support). Q10 is true/false; Q17 single choice; Q23 multiple choice.',[10,17,23])]
for ti,su,qs in pages:
 y=title(ti,su)
 for q in qs:y=question(q,y)
 footer(c);c.showPage()
c.save()
# Companion guide with fixed page divisions.
st=[]
def add(t,k='b'):st.append(p(t,k))
def code(t):st.append(Preformatted(t,styles['code']))
def table(rows,widths):
 data=[[p(escape(str(x)),'c') for x in row] for row in rows]
 tb=Table(data,colWidths=widths,hAlign='LEFT');tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e1edf0')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f4f7f9')]),('LINEBELOW',(0,0),(-1,0),.7,teal),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));st.append(tb);st.append(Spacer(1,9))
def new():st.append(PageBreak())
add('What to practise from this final','h')
add('<b>Working scope: Lectures 1-9.</b> These are the decks in your Midterm folder; your existing revision guide also records Lectures 1-9 as confirmed coverage. I did not find a separate official midterm notice. This is a content comparison, not a prediction of this year\'s questions.')
add('22 clear matches','s')
table([['Questions','Why they fit / lecture evidence'],['1, 11, 24','Variables, expressions and identifiers - L1, pp.25-51.'],['2, 20, 22','Functions, const-reference arguments, overloading - L2 pp.3-9,16-30; L8 p.22.'],['3, 4','String concatenation - L4 pp.24-26; stream operator/reference return - L8 pp.36-39.'],['5, 6, 7, 14, 15, 26, 27, 31, 32','Array size, pointers, addressing and expression tracing - L6 pp.9-11,18-29,35-46. Q26 mentions linked structures only as a use of pointers.'],['25','Static storage, stack and heap - L6 p.14; L7 p.4.'],['9','begin()/end() iterator meaning - L9 pp.16-22.'],['12, 21, 30','Encapsulation, OOP and virtual/nonvirtual dispatch - L8 pp.15-18,41-47,54-57.']],[115,392])
add('Three optional questions','s')
add('<b>Q10:</b> C++ paradigms; functional programming is not developed in these decks. <b>Q17:</b> bitwise shifts and masks; the operators appear in L1 p.42 and L6 p.32, but pixel masking is not a developed example. <b>Q23:</b> range-for is covered, but the exact Stanford container support is library-specific. Keep these for a second pass.','c')
add('Seven questions to set aside for now','s')
add('<b>Q8</b> hashing and collision complexity; <b>Q13</b> merge-sort complexity; <b>Q16</b> minimax; <b>Q18</b> BST traversals; <b>Q19</b> heap priority queues; <b>Q28</b> recursive problem decomposition; <b>Q29</b> circular queue implementation. These are not developed in Lectures 1-9. L1 p.13 lists data structures and algorithms as later course parts. Selection sort as a template example and CharStack as a class-design example <b>are</b> still in scope.','c')
new()
add('What this paper leaves out','h')
add('“Missing” means not directly assessed in this paper; a passing mention is not meaningful practice. Do not use this final as your complete midterm checklist.')
table([['Lecture','Coverage gap to revise'],['L1 | Foundations','Scope/lifetime, namespace and compilation/linking, control-flow tracing, short-circuit evaluation, casts, assertions. Q1/11/24 cover only a small slice.'],['L2 | Functions','Default parameters, pass-by-value vs reference mutation, writing/tracing swap, prototypes and algorithm implementation. Q2/20/22 are conceptual.'],['L3 | Libraries','Headers vs implementation, include guards, exported types/constants, enum operators, library design, rand/srand and seed behavior. Almost no direct coverage.'],['L4 | Strings','C-string terminators and storage, strlen/strcpy/strcmp, character classification, indexing, substr/find/erase/insert/replace and string-processing loops. Q3 tests only concatenation.'],['L5 | Streams','setw, fill/alignment, fixed/scientific and precision; whitespace handling; get/getline; file open/read/write/close; success/failure-controlled loops; stringstream conversion. Q4 and cout in Q31 do not cover these skills.'],['L6 | Pointers / arrays','Pointer-based swap, object pointers and ->/this, function pointers, writing C-string traversal/copy routines. Basic addressing is well represented.'],['L7 | Dynamic memory','new/delete and new[]/delete[], dynamic 2D arrays, leaks/dangling pointers, lifetime/destructors, malloc/free, const/static variations, unique/shared/weak pointers. Q25/26 only skim the concepts.'],['L8 | Classes','Constructors/initializer lists/destructors, shallow vs deep copy, copy constructor vs assignment, implementing operators, abstract classes/pure virtual functions, CharStack ownership, Rational/TokenScanner Archive/Build Outputs/Playground/examples. Q30 is only one dispatch trace.'],['L9 | Templates / iterators','Writing function/class templates, multiple type parameters and return conversion, template definitions in headers, generic selection sort, forward/reverse iterator loops and implementation. Q9 tests only endpoint meaning.']],[113,394])
add('Highest-priority gaps: L5 streams, L7 ownership/lifetime, L8 copying, and L9 templates. The final contains no substantial template-writing or file/string-stream exercise.','c')
new()
add('Pointers and arrays | Start here','h')
add('Practise Q6, 7, 15 and 27, then Q31 and Q32. Draw a box for each variable and an arrow for each pointer. After every statement, update both the pointer position and the array contents. L6 pp.22-29 and 35-46 are the closest lecture Archive/Build Outputs/Playground/examples.')
add('Q31 worked trace - cover this until you try it','s')
table([['Statement','Value assigned','Pointer / array after statement'],['int* p = arr','-','p -> arr[0]; arr = {2,0,2,1}'],['int a = *++p','a = 0','p -> arr[1]; array unchanged'],['int b = *p++','b = 0','p -> arr[2]; array unchanged'],['int c = ++*p','c = 3','p -> arr[2]; arr = {2,0,3,1}'],['int d = (*p)++','d = 3','p -> arr[2]; arr = {2,0,4,1}']],[145,100,262])
code('2041\n0033')
add('<b>*p++</b> is <b>*(p++)</b>: use the old pointed-to value, then advance p. <b>*++p</b> advances p before dereferencing. <b>++*p</b> and <b>(*p)++</b> change the element, not p.','c')
add('Q32: type determines the step size','s')
add('In most expressions doubleArray becomes a double*; adding 1 advances 8 bytes. &amp;doubleArray has type double (*)[10]; adding 1 advances 80 bytes (0x50). Same starting address, different types.','c')
table([['Expression(s)','Requested hexadecimal value'],['doubleArray; &doubleArray; &doubleArray[0]','ACE0 (addresses)'],['*doubleArray; doubleArray[0]','0000 (numeric value 0)'],['doubleArray+1; &doubleArray[1]','ACE8 (address)'],['&doubleArray+1','AD30 (one past the whole array)'],['doubleArray+9; &doubleArray[9]','AD28 (address: ACE0 + 9 x 8)'],['*doubleArray+9','0009 (numeric value: 0 + 9)'],['*(doubleArray+9); doubleArray[9]','0022 (numeric value: decimal 34)']],[320,187])
add('The paper asks you to express numeric values in hex; this does not ask for the IEEE-754 bit representation of a double. One-past pointers may be formed, but not dereferenced.','c')
new()
add('Streams | A manageable checklist','h')
add('Streams deserve deliberate practice because this final barely tests them. Work through L5 pp.11-17 (formatting/input), pp.20-31 (files/reading), and pp.34-38 (string streams).')
add('1. Know what is consumed','s')
add('<b>&gt;&gt;</b> normally skips leading whitespace; extraction into a string stops at whitespace. <b>get(ch)</b> reads the next character, including whitespace. <b>getline</b> reads through the delimiter and discards it. After number extraction, a newline can remain for the next getline. <b>ws</b> consumes leading whitespace; use it only when leading whitespace and blank lines should be ignored.','c')
add('2. Track formatting state','s')
add('<b>setw(n)</b> sets a minimum field width for the next formatted value. <b>setfill</b>, alignment, fixed/scientific and precision persist until changed. With <b>fixed</b>, precision counts decimal places; in the default format, it counts significant digits. A width never truncates a value.','c')
add('3. Let the read operation control the loop','s')
code('while (in >> value) { /* process value */ }\nwhile (getline(in, line)) { /* process line */ }\nwhile (in.get(ch)) { /* process character */ }')
add('Check that opening a file succeeded. Do not use while (!in.eof()) as a general read loop: EOF is detected by a read attempt. L5 p.24 shows that pattern; p.30 provides the safer getline-controlled loop. clear() resets error flags; it does not itself remove invalid input.','c')
add('4. Treat a string as an input/output source','s')
add('Use istringstream to parse existing text; ostringstream to build formatted text; str() to obtain the stored string. Be able to trace a failed conversion and explain when a loop stops.','c')
add('5. Try these three short drills','s')
add('Assume the standard headers and using namespace std. Answers are on page 6. These are new practice exercises, not questions from the final.','c')
code('// A: write the exact output\ncout << fixed << setprecision(2) << setfill(\'_\')\n     << setw(6) << 3.5 << \'|\' << 2.0;\n\n// B: what do s and t contain?\nistringstream in("42\\nAlice Bob\\n");\nint n; string s, t;\nin >> n; getline(in, s); getline(in, t);\n\n// C: what are total and in.fail() at the end?\nistringstream in("10 20 x 30");\nint x, total = 0;\nwhile (in >> x) total += x;')
new()
add('Your revision priorities','h')
add('These priorities combine the lecture coverage, this paper\'s practice value, and your concerns. They are study recommendations, not estimated exam probabilities.')
table([['Priority','What you should be able to do without notes'],['1 | Pointers + arrays','Trace Q31/32 accurately; distinguish p, *p, &p, arr and &arr; scale pointer arithmetic; explain array decay and bounds.'],['2 | Streams','Trace whitespace and newlines; predict exact padding/precision; write read-controlled loops; parse a string stream and detect failure.'],['3 | Dynamic memory + copying','Pair allocation/deallocation; draw stack/heap lifetime; identify leaks/dangling pointers; explain deep copy and object ownership.'],['4 | Classes + templates','Trace constructor/copy/assignment behavior and virtual dispatch; implement basic operators; write a small generic function/class and iterator loop.'],['5 | Strings + foundations','Practise C-string vs std::string operations, references/default arguments, integer division/control flow, library interfaces and random seeds.']],[158,349])
add('A focused four-hour practice session','s')
table([['Time','Task'],['0:00-0:55','Attempt Q6/7/15/27/31/32. Check the trace on page 3 only after finishing. Redo errors with a memory diagram.'],['0:55-1:45','Do the stream drills; then write one line-reading loop and one numeric string-stream parser. Revisit L5 Archive/Build Outputs/Playground/examples.'],['1:45-2:25','Practise new[]/delete[], a dynamic matrix cleanup, const pointer forms, and a deep-copy class.'],['2:25-3:00','Do Q12/20/21/22/30; trace a virtual vs nonvirtual call and distinguish copy construction from assignment.'],['3:00-3:30','Write a function template, trace a mixed-type return, and practise begin/end and reverse traversal.'],['3:30-4:00','Review strings, default arguments and library gaps; redo your three most frequent errors without notes.']],[95,412])
add('Readiness check','s')
add('You are ready to move on when you can explain <b>why</b> each pointer moves, which input characters remain unread, and who owns each allocated object. For every snippet, first decide: valid execution, compile error, or undefined behavior.','c')
add('A note about old-paper wording','s')
add('Q4 has misleading wording: std::ostream is noncopyable, so returning a normal output stream by value does not simply produce a copy. Learn ostream&amp; and chaining. Q21 uses a broad “distinguishing features” formulation; abstraction also appears in other paradigms. Treat these as concept prompts rather than rely on an unverified old answer key.','c')
new()
add('Drill answers and source map','h')
add('Streams: check your reasoning','s')
add('<b>A:</b> <font name="Mono">__3.50|2.00</font>. The first number occupies four characters, so width 6 adds two underscores. setw applies to that value; fixed and precision remain for the second number.','c')
add('<b>B:</b> n = 42, s is empty, and t = "Alice Bob". The number extraction leaves the newline. The first getline consumes it and returns an empty string.','c')
add('<b>C:</b> total = 30 and in.fail() is true. Extraction fails at x, so the loop ends before the final 30 is processed. Clearing the error alone would leave the offending character to handle.','c')
add('Sources used for this comparison','s')
add('Page references in this guide use PDF page numbers, including title slides. All lecture files below are in Midterm/Lecture notes. The source final is in Past papers.','c')
for s in [
'2021 Spring final: 2_CSC3002_Final_2021_Spring.pdf.pdf, pp.2-8. Original questions reproduced in the companion question PDF.',
'L1: 1-Overview/1-CSC3002_Lecture Notes Overview of C++.pdf. Course outline p.13; foundations pp.16-64.',
'L2: 2-Functions and Libraries 1/Week 1/2 - CSC3002_Lecture Notes Functions and Libraries Part 1.pdf. Functions, references and operators pp.3-35.',
'L3: 3 - Function and Library 2/3-CSC3002_Lecture Notes Functions and Libraries Part 2.pdf. Interfaces pp.4-23; random library pp.24-34.',
'L4: 4 - Strings/4-CSC3002_Lecture Notes_Strings.pdf. C strings pp.10-15; C++ strings pp.22-38.',
'L5: 5 - Stream/5-CSC3002_Lecture Notes Streams.pdf. Formatting pp.11-17; files pp.20-31; string streams pp.34-38.',
'L6: 6 - Array/6-CSC3002_Pointers and Arrays(2).pdf. Memory pp.3-19; pointers pp.20-34; arrays pp.35-46.',
'L7: 7- Dynamic memory management/7-CSC3002 Dynamic memory management.pdf. Allocation pp.5-20; const/static pp.22-26; smart pointers pp.27-30.',
'L8: 8 - Designing Classes/lecture/8-CSC3002_Designing Classes(1).pdf. Copying pp.21-28; operators pp.31-39; virtual classes pp.41-47; OOP pp.54-57.',
'L9: 9 - Template and Iterator/9-CSC3002_Template and Iterator.pdf. Templates pp.3-14; iteration pp.16-22.',
'Existing scope context: Exam Prep/Midterm/CSC3002_Lectures_1-9_Revision_Guide.md, opening scope statement. This is a previously prepared study guide, not an official syllabus notice.'
]:add(s,'c')
add('The extracted paper preserves its historical wording and answer choices. The practice guide provides explanations for Q31-32 and the new stream drills; it is not an official marking scheme.','c')
SimpleDocTemplate(str(O/'CSC3002_Midterm_Coverage_and_Focus.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=44,bottomMargin=52,title='CSC3002 - Midterm coverage gaps and study priorities',author='Study guide').build(st,onFirstPage=footer,onLaterPages=footer)
print('Created both PDFs')
