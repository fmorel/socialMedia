#!/usr/bin/python
import json
import urllib2
import argparse

#example query
#  - http://otter.topsy.com/search.json?q=m-commerce%20from%3Atcadierno&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d30

#Extract lists from input files
authorList = open('authors.txt', 'r').readlines()
keywordList = open('keywords.txt', 'r').readlines()

authorList = map(lambda s: s.strip(), authorList)
keywordList = map(lambda s: s.strip(), keywordList)

apiKey = "09C43A9B270A470B8EB8F2946A9369F3"

parser = argparse.ArgumentParser()
parser.add_argument("type", help="What type of data to crunch", choices=["stats", "contents"])
parser.add_argument("-o", "--output", help="Output file", default="output.txt")
parser.add_argument("-s", "--stats", help="Output of 'stats' command to help contents search ")
args = parser.parse_args()

outputFile = open(args.output, 'w')

###########################
#Handle stats style output

if args.type == "stats":
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
			myQuery = 'http://otter.topsy.com/search.json?q={}%20from%3A{}&apikey={}&window=d180'.format(urllib2.quote(keyword), author, apiKey)
			response = urllib2.urlopen(myQuery)
			jsonData = json.loads(response.read())
			total = jsonData['response']['total']
			output = output + ', ' + str(total)
			response.close()  # best practice to close the file
		output = output + '\n'
		outputFile.write(output)

############################
#Handle content style output
if args.type == "contents":
	stats=[]
	if args.stats == None:
		print "stats argument is mandatory when working with contents"
		sys.exit()
	else :
		stats = open(args.stats, 'r').readlines()
	
	stats = map(lambda s: s.split(', '), stats)
	header = stats[0]
	stats = stats[1:]
#Build a dictionnary of tweet counts ['author']['keyword']
	statsDict={}
	for stat in stats:
		i=1
		line={}
		for key in header[1:]:
			line[key] = int(stat[i])
			i+=1
		statsDict[stat[0]] = line
#Build output
	for author in authorList:
		output = '\n==================\n' + author + '\n==================\n'
		print author
		for key in statsDict[author]:
			if statsDict[author][key] == 0:
				continue
			output = output + '\n' + key + '\n-----------------\n'
			myQuery = 'http://otter.topsy.com/search.json?q={}%20from%3A{}&apikey={}&window=d180'.format(urllib2.quote(key), author, apiKey)
			response = urllib2.urlopen(myQuery)
			jsonData = json.loads(response.read())
			content = map(lambda l:l['content'], jsonData['response']['list'])
			output = output + '\n'.join(content) +'\n'

		outputFile.write(output.encode('utf8'))


outputFile.close()
