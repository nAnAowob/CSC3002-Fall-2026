from pathlib import Path
import re,html,json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
root=Path(__file__).resolve().parents[2]
source=root/'Exam Prep/Midterm/CSC3002_Lectures_1-9_Revision_Guide.md'
output=source.with_suffix('.pdf')
# System fonts: embed Unicode text, keeping code monospaced.
fonts=Path('/System/Library/Fonts/Supplemental')
for name,file in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf'),('Mono','Courier New.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
navy=colors.HexColor('#18324B');teal=colors.HexColor('#087F8C');gray=colors.HexColor('#516174')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=9.05,leading=11.7,spaceAfter=5.0,textColor=navy),
 'h1':ParagraphStyle('h1',fontName='Bold',fontSize=20,leading=24,spaceAfter=13,textColor=navy),
 'h2':ParagraphStyle('h2',fontName='Bold',fontSize=11.2,leading=14,spaceBefore=7,spaceAfter=6,textColor=teal,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.0,leading=10.0,textColor=navy),
 'headcell':ParagraphStyle('headcell',fontName='Bold',fontSize=8.0,leading=10.0,textColor=colors.white),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=7.8,leading=9.4,textColor=navy,backColor=colors.HexColor('#F0F4F7'),borderPadding=6,spaceBefore=3,spaceAfter=9),
}
def inline(s):
 s=html.escape(s)
 return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
def par(s,style='body'):return Paragraph(inline(s),styles[style])
page_chunks=source.read_text().split('---PAGE---')
story=[]
for pn,chunk in enumerate(page_chunks,1):
 lines=chunk.strip().splitlines();i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip():i+=1;continue
  if line.startswith('```'):
   code=[];i+=1
   while i<len(lines) and not lines[i].startswith('```'):
    code.append(lines[i]);i+=1
   # XML-safe Preformatted text, preserving literal < and &.
   block=Preformatted('\n'.join(code),styles['code'])
   story.append(block);i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    cells=[x.strip() for x in lines[i].strip('|').split('|')]
    if not all(re.fullmatch(r'[:\- ]+',x) for x in cells):rows.append(cells)
    i+=1
   count=len(rows[0]);w=A4[0]-84
   if count==3:
    ratios=[.28,.45,.27] if pn!=1 else [.12,.71,.17]
   else:ratios=[.35,.65]
   widths=[w*r for r in ratios]
   data=[[par(c,'headcell' if r==0 else 'cell') for c in row] for r,row in enumerate(rows)]
   table=Table(data,colWidths=widths,hAlign='LEFT')
   table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),navy),('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
    ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#F0F4F7'),colors.white]),
    ('LINEBELOW',(0,-1),(-1,-1),.4,colors.HexColor('#D6DFE6'))]))
   story.extend([table,Spacer(1,8)]);continue
  if line.startswith('# '):story.append(par(line[2:],'h1'))
  elif line.startswith('## '):story.append(par(line[3:],'h2'))
  else:story.append(par(line))
  i+=1
 if pn<len(page_chunks):story.append(PageBreak())
def decorate(canvas,doc):
 w,h=A4;canvas.saveState()
 canvas.setFillColor(teal);canvas.rect(0,h-8,w,8,fill=1,stroke=0)
 canvas.setFont('Bold',8);canvas.setFillColor(gray)
 canvas.drawString(42,h-30,'CSC3002  /  FALL 2026  /  MIDTERM')
 canvas.setFont('Body',8);canvas.drawRightString(w-42,h-30,'LECTURES 1-9')
 canvas.setStrokeColor(colors.HexColor('#D6DFE6'));canvas.line(42,35,w-42,35)
 canvas.setFont('Body',7.4);canvas.drawString(42,23,'Definitions  /  Rules  /  C++17 Archive/Build Outputs/Playground/examples')
 canvas.drawRightString(w-42,23,str(doc.page))
 canvas.restoreState()
doc=SimpleDocTemplate(str(output),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=48,bottomMargin=46,title='CSC3002 Midterm Revision Guide - Lectures 1-9',author='CSC3002 study notes',pageCompression=1)
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
from pypdf import PdfReader
r=PdfReader(output)
print(json.dumps({'pdf':str(output),'pages':len(r.pages),'intended_pages':len(page_chunks),'bytes':output.stat().st_size}))
for i,p in enumerate(r.pages,1):
 text=p.extract_text() or ''
 print(i, len(text),text.splitlines()[2:4])
