from cx_extractor_Python import cx_extractor_Python
cx = cx_extractor_Python()
html = cx.getHtml('http://edition.cnn.com/2016/07/01/asia/taiwan-fires-missile-on-china/index.html')
content = cx.filter_tags(html)
s = cx.getText(content)
print(s)
