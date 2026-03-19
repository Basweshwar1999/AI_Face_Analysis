from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(40, 40, 40)
        self.cell(0, 15, 'AI Face Analysis & Reporting System', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_font('helvetica', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", align='C', new_x='LMARGIN', new_y='NEXT')
        self.line(10, 35, 200, 35)
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 16)
        self.set_fill_color(200, 220, 255)
        self.set_text_color(0, 50, 100)
        self.cell(0, 10, title, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

    def chapter_body(self, key, value):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(50, 10, f"{key}:")
        self.set_font('helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, str(value), new_x='LMARGIN', new_y='NEXT')

    def add_section(self, title, data_dict):
        self.chapter_title(title)
        for k, v in data_dict.items():
            if isinstance(v, dict):
                self.chapter_body(k.replace('_', ' ').capitalize(), "")
                for sub_k, sub_v in v.items():
                    self.set_font('helvetica', '', 12)
                    self.cell(10, 8) # Indent
                    self.cell(40, 8, f"{sub_k.replace('_', ' ').capitalize()}:")
                    self.cell(0, 8, str(sub_v), new_x='LMARGIN', new_y='NEXT')
            else:
                self.chapter_body(k.replace('_', ' ').capitalize(), v)
        self.ln(5)

def generate_report(data, filename="report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    
    if 'demographics' in data:
        pdf.add_section('Demographics', data['demographics'])
        
    if 'geometry' in data:
        pdf.add_section('Face Geometry', data['geometry'])
        
    if 'eyes' in data:
        pdf.add_section('Eye Analysis', data['eyes'])
        
    if 'psychology' in data:
        pdf.add_section('Psychology & Emotion', data['psychology'])
        
    if 'recommendation' in data:
        pdf.add_section('Recommendations', data['recommendation'])
        
    pdf.output(filename)
    return filename
