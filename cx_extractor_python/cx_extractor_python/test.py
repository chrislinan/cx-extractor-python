from cx_extractor_python import cx_extractor_Python
cx = cx_extractor_Python()
html = cx.getHtml('http://coolshell.cn/articles/5426.html')
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
