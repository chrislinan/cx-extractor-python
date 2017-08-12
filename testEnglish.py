import os
from CxExtractor import CxExtractor
files = os.listdir('./bbcnews-html')
cx = CxExtractor(threshold=186)
for f in files:
    text = ''
    html = cx.readHtml('./bbcnews-html/'+f,'utf-8')
    content = cx.filter_tags(html)
    text = cx.getText(content)
    with open('./bbcnews-text/'+f.split('.')[0] + '.txt','w',encoding='utf-8') as textfile:
        textfile.write(text)


