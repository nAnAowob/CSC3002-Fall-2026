from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
R=Path(__file__).resolve().parents[3]
O=R/'output/pdf';O.mkdir(parents=True,exist_ok=True)
for n,f in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Mono','Courier New.ttf')]:
 pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
navy=colors.HexColor('#17324d');teal=colors.HexColor('#087e8b')
S={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.4,leading=13.2,spaceAfter=7,textColor=navy),
 'h1':ParagraphStyle('h1',fontName='Bold',fontSize=20,leading=24,spaceAfter=12,textColor=navy),
 'h2':ParagraphStyle('h2',fontName='Bold',fontSize=12,leading=16,spaceAfter=9,textColor=teal),
 'h3':ParagraphStyle('h3',fontName='Bold',fontSize=10.5,leading=14,spaceBefore=6,spaceAfter=6,textColor=teal,keepWithNext=True),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=8.5,leading=11.2,spaceAfter=9,backColor=colors.HexColor('#eef3f6'),borderPadding=6),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.5,leading=11.5,spaceAfter=0,textColor=navy),
}
def fmt(s):
 s=escape(s)
 s=re.sub(r'`([^`]+)`',lambda m:'<font name="Mono">'+m.group(1)+'</font>',s)
 return re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
def p(s,k='body'):return Paragraph(fmt(s),S[k])
def build(stem,label):
 lines=(R/'Exam Prep/Midterm'/f'{stem}.md').read_text().splitlines();story=[];i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line=='---PAGE---':story.append(PageBreak());i+=1;continue
  if line.startswith('```'):
   code=[];i+=1
   while not lines[i].startswith('```'):code.append(lines[i]);i+=1
   assert max(map(len,code),default=0)<=90,(stem,code)
   story.append(Preformatted('\n'.join(code),S['code']));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    row=[v.strip() for v in lines[i].strip('|').split('|')]
    if not all(re.fullmatch('[-: ]+',v) for v in row):rows.append(row)
    i+=1
   n=len(rows[0]);widths=({2:[94,413],3:[135,282,90],4:[110,110,100,187]}).get(n,[507/n]*n)
   if 'Quick key' in '\n'.join(lines[max(0,i-20):i]) and n==3:widths=[110,287,110]
   tb=Table([[p(v,'cell') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
   tb.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#deebef')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')]),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
   story.extend([tb,Spacer(1,9)]);continue
  if line.startswith('### '):story.append(p(line[4:],'h3'))
  elif line.startswith('## '):story.append(p(line[3:],'h2'))
  elif line.startswith('# '):story.append(p(line[2:],'h1'))
  elif line.startswith('___'):story.append(Spacer(1,8));story.append(p('_'*76))
  else:story.append(p(line))
  i+=1
 def footer(c,d):
  c.setStrokeColor(teal);c.line(44,38,A4[0]-44,38)
  c.setFont('Body',8);c.setFillColor(navy);c.drawString(44,25,'CSC3002 | '+label);c.drawRightString(A4[0]-44,25,str(d.page))
 doc=SimpleDocTemplate(str(O/f'{stem}.pdf'),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=38,bottomMargin=50,title=label,author='CSC3002 study materials')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 print(stem,doc.page,'pages')
build('2026-10-26_Tutorial_Review','Tutorial review | 26 October 2026')
# The question paper uses the past-exam typography and expanded writing areas.
import runpy
runpy.run_path(str(Path(__file__).with_name('build_exam_layout.py')), run_name='__main__')

# Readable solutions use the matching black-and-white exam style.
runpy.run_path(str(Path(__file__).with_name('build_solutions_layout.py')), run_name='__main__')
