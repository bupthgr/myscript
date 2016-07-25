# -*- coding: utf_8 -*-
import xml.etree.ElementTree as ET
import requests
import sys


url_config_dict = {
	'keyfrom': 'alfred-hungry',
	'key': '772480796',
	'type': 'data',
	'doctype': 'json',
	'version': '1.1'
}

errCodes = {
	0: '正常',
	20: u'要翻译的文本过长',
	30: u'无法进行有效的翻译',
	40: u'不支持的语言类型',
	50: u'无效的key',
	60: u'无词典结果，仅在获取词典结果生效'
}


def youdao_translate(queue):
	url_config_dict['q'] = queue
	url = 'http://fanyi.youdao.com/openapi.do'

	res = requests.get(url, params = url_config_dict).json()
	if res['errorCode'] != 0:
		return [errCodes[res['errCode']]]

	else:
		if 'basic' in res:
			if res['web']:
				return [u'有道词典结果：' + ', '.join(res['basic']['explains'])] + [(u'网络释义：' + ', '.join(web['value'])) for web in res['web']]
			else:
				returm [', '.join(res['basic']['explains'])]
		else:
			return [u'找不到结果，是不是输错了？']

def format_xml(titles):
	items = ET.Element('items')
	for title in titles:
		item = ET.SubElement(items, 'item')
		ET.SubElement(item, 'title').text = u'Result'
		ET.SubElement(item, 'title').text = title
		
		#ET.SubElement(item, 'icon').text = icon

	return ET.tostring(items, encoding = 'UTF-8', method = 'xml')


if __name__ == '__main__':
	print format_xml(youdao_translate(sys.argv[1]))
