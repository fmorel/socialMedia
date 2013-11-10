import json
import urllib2

#example query
#  - http://otter.topsy.com/search.json?q=m-commerce%20from%3Atcadierno&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d30
#Fetch some URL



keyword = 'mobile'
author='tcadierno'
myQuery = 'http://otter.topsy.com/search.json?q={}%20from%3A{}&apikey=09C43A9B270A470B8EB8F2946A9369F3&window=d180'.format(keyword, author)
response = urllib2.urlopen(myQuery)
#print response.info()
json = json.loads(response.read())
# do something
total = json['response']['total']
print "Total tweets : "
print total
response.close()  # best practice to close the file
