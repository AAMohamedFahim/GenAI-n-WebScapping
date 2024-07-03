import requests
from selectolax.parser import HTMLParser
from fpdf import FPDF
#------------------------------------------------------------------------
class PDF(FPDF):
    def titlee(self):
        self.set_font('Arial', '', 25)
        self.multi_cell(0, 10,"\n\n\n\n\n\nArtificial Intelligence in E-Commerce: The Complete Guide")
        self.ln()
        
    def header(self):
        self.set_font('Arial', '', 6)
        self.cell(0, 10, 'Artificial Intelligence in E-Commerce: The Complete Guide', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
        self.ln(10)
    
    def subheading(self, subheading):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, subheading.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body.encode('latin-1', 'replace').decode('latin-1'))
        self.ln()
#------------------------------------------------------------------------
def main():
    url = 'https://ecom-pedia.com/artificial-intelligence-in-e-commerce-the-guide/'
    response = requests.get(url)
    tree = HTMLParser(response.text)
    main_div = tree.css_first("div.entry-content.alignfull.wp-block-post-content.is-layout-constrained.wp-block-post-content-is-layout-constrained")

    pdf = PDF()
    pdf.add_page()
    pdf.titlee()
    pdf.set_auto_page_break(auto=True, margin=15)
    if main_div:
        for element in main_div.iter():
            if element.tag in ['h2', 'h3', 'p', 'ol', 'ul']:
                text = element.text(strip=True)
                if element.tag == 'h2':
                    pdf.add_page()
                    pdf.chapter_title(text) 
                elif element.tag == 'h3':
                    pdf.subheading(text)
                else:
                    pdf.chapter_body(text)
        pdf.output('text_content11.pdf')
        print("PDF created successfully!")
    else:
        print("Div tag not found.")

#------------------------------------------------------------------------
if __name__ == "__main__":
    main()