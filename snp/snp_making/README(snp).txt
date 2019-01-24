get_rsIDs.py
	get rsIDs from categories in SNPedia
	make that as a [category name].txt
	combine all output file 

text_from_wiki-with_soup.ipynb
	get HTML code from  SNPedia API
	process to how to convert it as an OrderedDict

make database.ipynb
	< rsID from get_rsIDs > inner join < rsID from GSA 1.2 >
	result ---> DB	
	using the gettingAPI function, make DB
	it helps making report process more speedy

LogUpdateTest.ipynb
	when program use API, rsIDs are saved at Log.txt
	using the Log.txt, once a week
	DB will automatically updated (logUpdate.py)
	
