from CxExtractor import CxExtractor
cx = CxExtractor(threshold=186)
# html = cx.getHtml("http://www.bbc.com/news/world-europe-40885324")
html = cx.getHtml("http://news.163.com/17/0810/09/CRFF02Q100018AOR.html")
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
