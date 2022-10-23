import re
from typing import List


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO


class URLFinder:
    """
    Parse pdf file and returns all links from it

    Attributes
        filename: str
            Path to pdf file

    Methods
        get_links
    """
    def __init__(self, filename: str):
        self.filename: str = filename

    def get_links(self) -> List[str]:
        """Parse pdf file and returns all links from it"""

        text: str = self._pdf_to_text()
        links: List[str] = self._get_all_links(text)

        return links

    def _pdf_to_text(self) -> str:
        """Return content from pdf as string"""

        manager = PDFResourceManager()
        retstr = BytesIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        filepath = open(self.filename, 'rb')
        interpreter = PDFPageInterpreter(manager, device)

        for page in PDFPage.get_pages(filepath, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        filepath.close()
        device.close()
        retstr.close()

        return text.decode()

    @staticmethod
    def _get_all_links(text: str) -> List[str]:
        """Return list of all links and emails from string"""

        pattern = r'(http.*)|(www.*)|(.*@.*)'
        result: list = re.findall(pattern, text)
        return [
            i
            for elem in result
            for i in elem
            if i
        ]
