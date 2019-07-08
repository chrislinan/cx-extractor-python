#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import chardet
import asyncio
import requests


class CxExtractor:
    """cx-extractor implemented in Python"""

    __text = []
    __indexDistribution = []

    def __init__(self, threshold=86, blocksWidth=3) -> None:
        self.__blocksWidth = blocksWidth
        self.__threshold = threshold

    async def getText(self, content: str) -> str:
        if self.__text:
            self.__text = []
        lines = content.split('\n')
        for i in range(len(lines)):
            lines[i] = re.sub("\r|\n|\\s{2,}", "",lines[i])
        self.__indexDistribution.clear()
        for i in range(0, len(lines) - self.__blocksWidth):
            wordsNum = 0
            for j in range(i, i + self.__blocksWidth):
                lines[j] = lines[j].replace("\\s", "")
                wordsNum += len(lines[j])
            self.__indexDistribution.append(wordsNum)
        start = -1
        end = -1
        boolstart = False
        boolend = False
        if len(self.__indexDistribution) < 3:
            return 'This page has no content to extract'
        for i in range(len(self.__indexDistribution) - 3):
            if(self.__indexDistribution[i] > self.__threshold and (not boolstart)):
                if (self.__indexDistribution[i + 1] != 0 or self.__indexDistribution[i + 2] != 0 or self.__indexDistribution[i + 3] != 0):
                    boolstart = True
                    start = i
                    continue
            if (boolstart):
                if (self.__indexDistribution[i] == 0 or self.__indexDistribution[i + 1] == 0):
                    end = i
                    boolend = True
            tmp = []
            if(boolend):
                for ii in range(start, end + 1):
                    if(len(lines[ii]) < 5):
                        continue
                    tmp.append(lines[ii] + "\n")
                str = "".join(list(tmp))
                if ("Copyright" in str or "版权所有" in str):
                    continue
                self.__text.append(str)
                boolstart = boolend = False
        result = "".join(list(self.__text))
        if result == '':
            return 'This page has no content to extract'
        else:
            return result

    async def replaceCharEntity(self, htmlstr: str) -> str:
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()
            key = sz.group('name')
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    async def getHtml(self, url: str) -> str:
        response = requests.get(url)
        encode_info = chardet.detect(response.content)
        response.encoding = encode_info['encoding'] if encode_info['confidence'] > 0.5 else 'utf-8'
        return response.text

    async def readHtml(self, path: str, coding: str) -> str:
        page = open(path, encoding=coding)
        lines = page.readlines()
        s = ''
        for line in lines:
            s += line
        page.close()
        return s

    async def filter_tags(self, htmlstr: str) -> str:
        re_doctype = re.compile('<![DOCTYPE|doctype].*>')
        re_nav = re.compile('<nav.+</nav>')
        re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
        re_script = re.compile(
            '<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
        re_style = re.compile(
            '<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
        re_textarea = re.compile(
            '<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+.*?>', re.DOTALL)
        re_comment = re.compile('<!--.*?-->', re.DOTALL)
        re_space = re.compile(' +')
        s = re_cdata.sub('', htmlstr)
        s = re_doctype.sub('',s)
        s = re_nav.sub('', s)
        s = re_script.sub('', s)
        s = re_style.sub('', s)
        s = re_textarea.sub('', s)
        s = re_br.sub('', s)
        s = re_h.sub('', s)
        s = re_comment.sub('', s)
        s = re.sub('\\t', '', s)
        s = re_space.sub(' ', s)
        s = await self.replaceCharEntity(s)
        return s
