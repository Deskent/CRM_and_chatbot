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

        http: str = True
            Flag for search links starts from http

        www: str = True
            Flag for search links starts from www

        email: str = True
            Flag for search links contains character '@'

    Methods
        get_links
    """

    def __init__(self, filename: str, http: bool = True, www: bool = True, email: bool = True):
        self.filename: str = filename
        self.patterns: list[str] = []
        if http:
            self.patterns.append('(http.*)')
        if www:
            self.patterns.append('(www.*)')
        if email:
            self.patterns.append('(.*@.*)')

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
        with open(self.filename, 'rb') as file:
            interpreter = PDFPageInterpreter(manager, device)

            for page in PDFPage.get_pages(file, check_extractable=True):
                interpreter.process_page(page)

            text = retstr.getvalue()

        device.close()
        retstr.close()

        return text.decode()

    def _get_all_links(self, text: str) -> List[str]:
        """Return list of all links and emails from string"""

        pattern = self.patterns[0] if len(self.patterns) == 1 else r'|'.join(self.patterns)
        results: list = re.findall(pattern, text)

        return results if len(results) < 2 else [
            url
            for array in results
            for url in array
            if url
        ]
