from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[3]
for n,f in [('ExamText','Times New Roman.ttf'),('ExamBold','Times New Roman Bold.ttf'),('ExamCode','Courier New Bold.ttf'),('ExamSans','Arial.ttf'),('ExamHeading','Arial Bold.ttf')]:
 pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
pdfmetrics.registerFontFamily('ExamText',normal='ExamText',bold='ExamBold',italic='ExamText',boldItalic='ExamBold')
W,H=A4;L=54;WIDTH=W-108
styles={
 'body':ParagraphStyle('body',fontName='ExamText',fontSize=12,leading=15),
 'option':ParagraphStyle('option',fontName='ExamText',fontSize=12,leading=15,leftIndent=18,firstLineIndent=-18),
 'heading':ParagraphStyle('heading',fontName='ExamHeading',fontSize=12,leading=16),
 'small':ParagraphStyle('small',fontName='ExamSans',fontSize=10,leading=14),
}
source=(R/'Exam Prep/Midterm/2026_TA_Mock_Midterm_Questions.md').read_text()
# Preserve all question text; remove only the old layout and scratch lines.
sections={}
for n in range(1,15):
 pat=rf'(?m)^### Q{n}\. ' if n<=11 else rf'(?m)^## Q{n}\. ' if n==12 else rf'(?m)^# Q{n} \| '
 m=re.search(pat,source);assert m,n
 end=re.search(r'(?m)^(?:### Q\d+\.|## Q12\.|# Q1[34] \|)',source[m.end():])
 text=source[m.start():m.end()+end.start() if end else len(source)]
 text=re.split(r'(?m)^### Part I answer record',text)[0]
 lines=text.splitlines();title=lines.pop(0)
 cleaned=[]
 for line in lines:
  if line=='---PAGE---' or line.startswith('___') or line.startswith('Answer:') or line.startswith('### Scratch work') or line.startswith('**End of paper.'):continue
  if line.startswith('#') and not line.startswith('### ('):continue
  cleaned.append(line)
 sections[n]=(title,'\n'.join(cleaned).strip())
# Written-response subparts are placed separately with large blank answer boxes.
subs={}
for n in [12,13,14]:
 parts=re.split(r'(?m)^### ',sections[n][1])[1:]
 subs[n]={p[1]:p for p in parts}
 assert len(subs[n])==({12:3,13:4,14:3}[n])
output=R/'output/pdf/2026_TA_Mock_Midterm_Questions.pdf'
c=canvas.Canvas(str(output),pagesize=A4);c.setTitle('CSC3002 Mock Midterm - Past-exam layout');c.setAuthor('CSC3002 practice materials')
page=0;TOTAL=14;y=0

def para(text,kind='body',gap=7):
 global y
 text=escape(text);text=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',text)
 text=re.sub(r'`([^`]+)`',r'<font name="ExamCode">\1</font>',text)
 p=Paragraph(text,styles[kind]);_,h=p.wrap(WIDTH,1000)
 assert y-h>=50,(page,'overflow',text,y,h)
 p.drawOn(c,L,y-h);y-=h+gap

def new(title=None,instruction=None):
 global page,y
 if page:c.showPage()
 page+=1;y=H-76
 c.setFont('ExamSans',9);c.drawString(L,H-34,'The Chinese University of Hong Kong, Shenzhen');c.drawRightString(W-L,H-34,'CSC3002 | MOCK')
 c.setFont('ExamSans',10);c.drawCentredString(W/2,25,f'Page {page} of {TOTAL}')
 if title:para(title,'heading',8)
 if instruction:para(instruction,'body',13)

def code(s):
 global y
 # Wrap long code only at token boundaries; no characters are discarded.
 lines=[]
 for line in s.splitlines():
  if pdfmetrics.stringWidth(line,'ExamCode',11)<=WIDTH-24:lines.append(line);continue
  # C++ insertion chains can continue on a new line before <<.
  while pdfmetrics.stringWidth(line,'ExamCode',11)>WIDTH-24:
   candidates=[m.start() for m in re.finditer(r' << |; ',line)]
   valid=[i for i in candidates if pdfmetrics.stringWidth(line[:i],'ExamCode',11)<=WIDTH-24]
   assert valid,('long code',line)
   cut=valid[-1]
   if line[cut:cut+2]=='; ':cut+=1
   lines.append(line[:cut]);line='    '+line[cut:].lstrip()
  lines.append(line)
 h=len(lines)*14
 assert y-h>=50,(page,'code overflow')
 c.setFont('ExamCode',11)
 for line in lines:c.drawString(L+12,y-11,line);y-=14
 y-=10

def content(text):
 lines=text.splitlines();i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('```'):
   i+=1;ls=[]
   while i<len(lines) and not lines[i].startswith('```'):ls.append(lines[i]);i+=1
   code('\n'.join(ls))
  elif re.match(r'^\([a-d]\)',line):para(line,'heading',9)
  elif re.match(r'^[A-F]\. ',line):para(line,'option',7)
  else:para(line)
  i+=1

def question(n):
 global y
 title=sections[n][0];title=re.sub(r'^#+ ','',title)
 title=re.sub(r'^Q(\d+)\.',r'\1.',title)
 para(title,'heading',10);content(sections[n][1]);y-=4
 para('Answer: ____________________',gap=17)

def box(h,label='Answer'):
 global y
 assert h>=55 and y-h-21>=50,(page,'box',y,h)
 c.setFont('ExamText',11);c.drawString(L,y-10,label);y-=20
 c.setLineWidth(.65);c.rect(L,y-h,WIDTH,h);y-=h+13

def fillbox(label='Answer',minheight=100):
 h=y-83
 assert h>=minheight,(page,'small box',h)
 box(h,label)

new()
c.setFont('ExamSans',11);c.drawString(L+14,y-12,'Student Number');c.line(L+133,y-15,W-L-80,y-15)
c.drawString(L+14,y-42,'Student Name');c.line(L+133,y-45,W-L-80,y-45)
y-=125
for text,size in [('MOCK MIDTERM EXAMINATION',18),('Fall 2026',12),('CSC3002 C/C++ Programming',16)]:
 c.setFont('ExamHeading',size);c.drawCentredString(W/2,y,text);y-=31
y-=12
para('Practice paper based on the 26 October tutorial.','small')
para('This is a mock examination, not an official university paper.','small',19)
para('Suggested practice duration: 100 minutes. Total: 100 points.')
para('This paper has 14 questions divided into 3 parts.',gap=17)
for text in ['Part I: Single-choice questions (Q1-Q4), 20 points.','Part II: Multiple-choice questions (Q5-Q11), 40 points.','Part III: Written-response questions (Q12-Q14), 40 points.']:para(text,'heading',8)
y-=9
para('Instructions','heading')
for s in ['Choose one answer for each question in Part I. Select all true options in Part II. Record your choices on page 8 or beside each question.','Write Part III answers in the boxes provided. Use additional paper if necessary and label the question number.','Assume C++17, all required standard headers, and using namespace std. Snippets and options are independent unless stated otherwise. Assume allocations succeed and the small arithmetic values do not overflow.','No numerical memory addresses are requested.','Practice marking: Part II uses exact-set marking (all correct choices and no incorrect ones). The actual exam marking policy and duration were not supplied.']:para(s,'body',8)
new('Part I: Single-choice questions (Q1-Q4). 20 points.','Select ONE answer for each question. Each question carries 5 points.')
question(1);question(2)
new('Part I: Single-choice questions (continued)')
question(3);question(4)
new('Part II: Multiple-choice questions (Q5-Q11). 40 points.','Select ALL true options. Q5-Q9 carry 6 points each; Q10-Q11 carry 5 points each.')
question(5);question(6)
new('Part II: Multiple-choice questions (continued)');question(7)
new('Part II: Multiple-choice questions (continued)');question(8)
new('Part II: Multiple-choice questions (continued)');question(9);question(10)
new('Part II: Multiple-choice questions (continued)');question(11)
para('Answer record - Parts I and II','heading',13)
c.setFont('ExamText',12)
for row in range(3):
 for col in range(4):
  n=row*4+col+1
  if n>11:continue
  x=L+col*121;c.drawString(x,y-12,f'Q{n}');c.rect(x+28,y-24,78,30)
 y-=47
new('Part III: Written-response questions (Q12-Q14). 40 points.','Write your answers in the boxes. Show reasoning where requested.')
para('12. Trace, write and diagnose. (12 points)','heading',12)
content(subs[12]['a']);fillbox('Answer to Q12(a): output, final array and pointer movement',220)
new('12. Trace, write and diagnose (continued)')
content(subs[12]['b']);box(230,'Answer to Q12(b): function definitions, pointer declaration and result')
content(subs[12]['c']);fillbox('Answer to Q12(c)',90)
new('13. Operators and abstract interfaces. (14 points)')
content(subs[13]['a']);box(265,'Answer to Q13(a): operator implementations')
content(subs[13]['b']);fillbox('Answer to Q13(b)',90)
new('13. Operators and abstract interfaces (continued)')
content(subs[13]['c']);box(245,'Answer to Q13(c): derived class and explanation')
content(subs[13]['d']);fillbox('Answer to Q13(d): output and reason',110)
new('14. Templates and stream reasoning. (14 points)')
content(subs[14]['a']);box(205,'Answer to Q14(a): function template')
para('Types and values (4 points)','heading',8)
c.setFont('ExamText',12)
rowh=36;colw=[80,190,WIDTH-270]
for row,vals in enumerate([['Variable','Type','Value'],['a','',''],['b','',''],['c','',''],['d','','']]):
 x=L
 for val,w in zip(vals,colw):c.rect(x,y-rowh,w,rowh);c.drawString(x+9,y-23,val);x+=w
 y-=rowh
new('14. Templates and stream reasoning (continued)')
content(subs[14]['b']);box(125,'Answer to Q14(b): three output lines and explanation')
content(subs[14]['c']);fillbox('Answer to Q14(c): total, recovery code and explanation',95)
assert page==TOTAL
c.save();print(output, page,'pages')
