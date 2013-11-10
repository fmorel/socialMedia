import json
import urllib2

#example query
#  - http://otter.topsy.com/search.json?q=m-commerce%20from%3Atcadierno&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d30

#Extract lists from input files
authorList = open('authors.txt', 'r').readlines()
keywordList = open('keywords.txt', 'r').readlines()

authorList = map(lambda s: s.strip(), authorList)
keywordList = map(lambda s: s.strip(), keywordList)

outputFile = open('Author_Keywords.txt', 'w')
#Build Header line
output='Author'
for keyword in keywordList:
	output = output+ ', ' + keyword
output = output + '\n'
outputFile.write(output)

#Build content
for author in authorList:
	output = author
	print '.'
	for keyword in keywordList:
		myQuery = 'http://otter.topsy.com/search.json?q={}%20from%3A{}&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d180'.format(urllib2.quote(keyword), author)
		response = urllib2.urlopen(myQuery)
		jsonData = json.loads(response.read())
		total = jsonData['response']['total']
		output = output + ', ' + str(total)
		response.close()  # best practice to close the file
	output = output + '\n'
	outputFile.write(output)

outputFile.close()
