from __future__ import annotations

import trafilatura
from bs4 import BeautifulSoup
from readability import Document


def _sanitize_html(html: str) -> str:
    # Remove control chars that can break lxml parsing.
    return "".join(ch for ch in html if ch == "\n" or ch == "\r" or ch == "\t" or ord(ch) >= 32)


class ContentExtractor:
    @staticmethod
    def extract_text(html: str) -> str:
        safe_html = _sanitize_html(html)
        text = trafilatura.extract(safe_html, include_links=False, include_formatting=False)
        if text and len(text.strip()) > 80:
            return text.strip()

        try:
            doc = Document(safe_html)
            readable_html = doc.summary(html_partial=True)
            soup = BeautifulSoup(readable_html, "html.parser")
            text2 = "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
            return text2.strip()
        except Exception:
            fallback = BeautifulSoup(safe_html, "html.parser").get_text("\n")
            return "\n".join(line.strip() for line in fallback.splitlines() if line.strip())
