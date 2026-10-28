from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[3]
for n,f in [('SolText','Times New Roman.ttf'),('SolBold','Times New Roman Bold.ttf'),('SolCode','Courier New Bold.ttf'),('SolSans','Arial.ttf'),('SolHead','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
pdfmetrics.registerFontFamily('SolText',normal='SolText',bold='SolBold',italic='SolText',boldItalic='SolBold')
S={
 'body':ParagraphStyle('body',fontName='SolText',fontSize=12,leading=15.5,spaceAfter=9),
 'h1':ParagraphStyle('h1',fontName='SolHead',fontSize=17,leading=21,spaceAfter=14,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='SolHead',fontSize=12,leading=16,spaceAfter=10,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='SolHead',fontSize=12,leading=16,spaceBefore=8,spaceAfter=9,keepWithNext=True),
 'code':ParagraphStyle('code',fontName='SolCode',fontSize=11,leading=14,spaceBefore=3,spaceAfter=12),
 'cell':ParagraphStyle('cell',fontName='SolText',fontSize=11,leading=14),
}
WIDTH=A4[0]-108
source=(R/'Exam Prep/Midterm/2026_TA_Mock_Midterm_Solutions.md').read_text()
chunks=source.split('---PAGE---')
# Put the answer table and the detailed explanations on separate pages.
first=chunks[0]
front,reason=first.split('### Part I reasoning',1)
reason,score=reason.split('### Score record',1)
policy=chunks[1].split('### Mock marking policy',1)[1]
q5=chunks[1].split('### Q5.',1)[1].split('### Q7.',1)[0]
q7=chunks[1].split('### Q7.',1)[1].split('### Mock marking policy',1)[0]
q9=chunks[2].split('### Q9.',1)[1].split('### What the mock sampled',1)[0]
coverage=chunks[2].split('### What the mock sampled',1)[1]
# Explicit breaks at complete subparts avoid splitting code from its rubric.
q12a,q12bc=chunks[3].split('### (b) Callback',1)
q13ab,q13cd=chunks[4].split('### (c) Abstract interface',1)
q14ab,q14c=chunks[5].split('### (c) Recovery',1)
pages=[
 front+'\n### Score record\n'+score,
 '# Part I | Single-choice explanations\n'+reason+'\n### Mock marking policy\n'+policy,
 '# Part II | Arrays and strings\n### Q5.'+q5,
 '# Part II | Classes and dispatch\n### Q7.'+q7,
 '# Part II | Ownership, streams and iteration\n### Q9.'+q9,
 q12a,
 '# Q12 | Callback and lifetime\n### (b) Callback'+q12bc,
 q13ab,
 '# Q13 | Abstract interfaces and dispatch\n### (c) Abstract interface'+q13cd,
 q14ab,
 '# Q14 | Input recovery and revision\n### (c) Recovery'+q14c,
 '# Coverage and source map\n### What the mock sampled'+coverage,
]
def fmt(s):
 s=escape(s)
 s=re.sub(r'`([^`]+)`',r'<font name="SolCode">\1</font>',s)
 return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
def p(s,k='body'):return Paragraph(fmt(s),S[k])
story=[]
for pi,chunk in enumerate(pages):
 if pi:story.append(PageBreak())
 lines=chunk.strip().splitlines();i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('```'):
   code=[];i+=1
   while not lines[i].startswith('```'):
    value=lines[i]
    if pdfmetrics.stringWidth(value,'SolCode',11)>WIDTH:
     if '//' in value:
      a,b=value.split('//',1);code.extend([a.rstrip(),'//'+b])
     else:raise ValueError(value)
    else:code.append(value)
    i+=1
   story.append(KeepTogether([Preformatted('\n'.join(code),S['code'])]));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    row=[x.strip() for x in lines[i].strip('|').split('|')]
    if not all(re.fullmatch('[-: ]+',x) for x in row):rows.append(row)
    i+=1
   n=len(rows[0]);widths=[100,WIDTH-170,70] if n==3 else [100,120,90,WIDTH-310]
   if rows[0][0]=='Variable':widths=[65,80,65,WIDTH-210]
   t=Table([[p(x,'cell') for x in row] for row in rows],colWidths=widths,repeatRows=1)
   t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,'black'),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
   story.extend([t,Spacer(1,12)]);continue
  if line.startswith('# '):story.append(p(line[2:],'h1'))
  elif line.startswith('## '):story.append(p(line[3:],'h2'))
  elif line.startswith('### '):story.append(p(line[4:],'h3'))
  elif re.match(r'^\*\*[A-F] (?:true|false):',line):
   # Each option gets its own paragraph instead of a dense block.
   for item in re.split(r' (?=\*\*[A-F] (?:true|false):)',line):story.append(p(item))
  else:story.append(p(line))
  i+=1
class NumberedCanvas(canvas.Canvas):
 def __init__(self,*args,**kw):super().__init__(*args,**kw);self.saved=[]
 def showPage(self):self.saved.append(dict(self.__dict__));self._startPage()
 def save(self):
  total=len(self.saved)
  for state in self.saved:
   self.__dict__.update(state)
   self.setFont('SolSans',9);self.drawString(54,A4[1]-34,'CSC3002 | MOCK MIDTERM');self.drawRightString(A4[0]-54,A4[1]-34,'SOLUTIONS')
   self.setFont('SolSans',10);self.drawCentredString(A4[0]/2,25,f'Page {self._pageNumber} of {total}')
   canvas.Canvas.showPage(self)
  canvas.Canvas.save(self)
out=R/'output/pdf/2026_TA_Mock_Midterm_Solutions.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=54,rightMargin=54,topMargin=67,bottomMargin=55,title='CSC3002 Mock Midterm - Solutions and marking guide',author='CSC3002 practice materials')
doc.build(story,canvasmaker=NumberedCanvas)
print(out,doc.page,'pages')
