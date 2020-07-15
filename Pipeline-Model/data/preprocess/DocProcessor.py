from html.parser import HTMLParser
from html.entities import name2codepoint
import re
import io

class _HTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'br') and not self.hide_output:
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p':
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r'\s+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = unichr(name2codepoint[name])
            self._buf.append(c)

    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._buf.append(unichr(n))

    def get_text(self):
        return re.sub(r' +', ' ', ''.join(self._buf))

class DocProcessor():
    def html_to_text(self,html):
        """
        Given a piece of HTML, return the plain text it contains.
        This handles entities and char refs, but not javascript and stylesheets.
        """
        parser = _HTMLToText()
        try:
            parser.feed(html)
            parser.close()
        except HTMLParseError:
            pass
        return parser.get_text()

    def text_to_html(self,text):
        """
        Convert the given text to html, wrapping what looks like URLs with <a> tags,
        converting newlines to <br> tags and converting confusing chars into html
        entities.
        """
        def f(mo):
            t = mo.group()
            if len(t) == 1:
                return {'&':'&amp;', "'":'&#39;', '"':'&quot;', '<':'&lt;', '>':'&gt;'}.get(t)
            return '<a href="%s">%s</a>' % (t, t)
        return re.sub(r'https?://[^] ()"\';]+|[&\'"<>]', f, text)

    def process_html(self,path):
        try:
            f = io.open(path,mode="r", encoding="utf-8")
            html = f.read()
            text = self.html_to_text(html)
            return text
        except FileNotFoundError as e:
            print('ERR')
            print(e)
            print('(ignored)')


# import sys
# if __name__ == '__main__':
# 	path = sys.argv[1]
# 	prs = DocProcessor()
# 	print prs.process_html(path)
