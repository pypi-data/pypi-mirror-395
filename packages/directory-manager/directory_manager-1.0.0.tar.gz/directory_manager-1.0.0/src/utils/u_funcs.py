"""
***Functions Utilities***

Here ends up all ideas that couldn't fit in a class and general use case functions.
"""

from urllib.parse import urlparse, ParseResult

def is_valid_url(url : str):
        """
        Check if URL is valid.
        """
        parsed : ParseResult = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

if __name__ == '__main__':
    print(__doc__)