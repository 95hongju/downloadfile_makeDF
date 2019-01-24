import requests
from bs4 import BeautifulSoup
import sys
from itertools import zip_longest
from collections import OrderedDict

def gethtml(TITLE):
	
	S = requests.Session()
	URL = "https://bots.snpedia.com/api.php"

	PARAMS = {
    'action': "parse",
    'page': TITLE,
    'section': 0,
    'format': "json"
    }
	try:
		res = S.get(url=URL, params=PARAMS)
		data = res.json()
		wikitext = data['parse']['text']['*']
		lines = wikitext.split('|-')
		return lines
	except (KeyError):
		print("CHECK THE rsID : no data")
		return []
	except Exception as e:
		print("unexpected error, ", e)
		return []


def make_report(rsID, rawHTML):
	if len(rawHTML)==0:
		data_gene = 'N/A'
		data_table = OrderedDict()
		data_desc = ['N/A']

	else:
		#replace some texts to find each data what i want
		rsID_getTable =rawHTML[0].replace('sortable smwtable','getdata1')
		rsID_getGENE =rsID_getTable.replace('<td width="90">Gene</td>','<td width="90" class="getdata2">Gene</td>')

		#makeSoup with replaced rawHTML
		soup = BeautifulSoup(rsID_getGENE, 'html.parser')

		#step 1, find gene name
		#-------------------------------------------
		try:
			data_temp = soup.find(class_='getdata2')
			data_gene = data_temp.findNext('td').a['title']
		except Exception as e:
			print('step 1 :'+str(e))
			data_gene = 'N/A'
		#step 2, find table as OrderedDict
		#-------------------------------------------
		try:
			table_html = soup.find(class_="getdata1")
			table_text = table_html.get_text()
			table_text = table_text.split('\n')
			#cut front & last space
			table_text = table_text[1:-1]
			column = table_text[:7]
			data = table_text[7:]
			grouped_data = list(zip_longest(*(iter(data),)*7))
			data_table = []
			for i in range(len(grouped_data)):
				data_table.append(OrderedDict((k,v) for k, v in zip(column,grouped_data[i])))
		except Exception as e:
			print('step 2 :'+str(e))
			data_table = OrderedDict()


		#step 3, find table as df
		#-------------------------------------------
		try:
			ptags = soup.find_all("p")[1:6]
			data_desc = []
			for ele in ptags:
				data_desc.append(ele.get_text())
		except Exception as e:
			print('step 3 :'+str(e))
			data_desc = ['N/A']
	
	return rsID, data_gene, data_table, data_desc
		
	
def make_OrderedDict(rs,ge,tb,ds):
	result = OrderedDict([('rsID',rs),('GENE',ge),('TABLE',tb),('DESC',ds)])
	return result

def test():
	print('testing')

def making_table_process(rsID):
	#get html
	print('rsID - '+rsID +' start' )
	raw_html = gethtml(rsID)
	#make orderedDict
	rs,ge,tb,ds = make_report(rsID,raw_html)
	report = make_OrderedDict(rs,ge,tb,ds)
	print('rsID - '+rsID +' done' )
	return report

def main():
    pass


if __name__ == '__main__':
    main()