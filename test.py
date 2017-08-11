from CxExtractor import CxExtractor
cx = CxExtractor(threshold = 186)
html = cx.getHtml("http://www.bbc.com/news/world-europe-40885324")
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
