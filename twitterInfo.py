#!/usr/bin/python
import twitter
import argparse
import time

#Create twitter API with authentication from Beatrice's profile
api = twitter.Api(
consumer_key="grfzFcIHU6kiS3xshGUf6Q",
consumer_secret="KKqYXiNCWMuLzIlmx8OLkXG4i3Fsn8i7SNIKC71SOQ",
access_token_key="138811547-PdVqwI2Ne1D2n6gX4IHQnUrICXZl6zqxx79vL6Vm",
access_token_secret="WTokWyRynBMa8FIWIHWWiGJR2bYgPWYcwkH6IowtYRtoy")

#Extract author list
authorList = open('authors.txt', 'r').readlines()
authorList = map(lambda s: s.strip(), authorList)

#Handle command line argument
parser = argparse.ArgumentParser()
parser.add_argument("type", help="What type of data to crunch", choices=["info", "followers"])
parser.add_argument("-o", "--output", help="Output file", default="output.txt")
parser.add_argument("-i", "--ids", help="ID list of user")
args = parser.parse_args()

outputFile = open(args.output, 'w')

###########################
#Handle info style output

if args.type == "info":
	#Header
	outputFile.write("Twitter name, real name, followers, following, tweets\n")
	#Content
	for author in authorList:
		print author
		usr = api.GetUser(screen_name=author)
		output = author + ', ' + usr.GetName() + ', ' + str(usr.GetFollowersCount()) + ', ' + str(usr.GetFriendsCount()) + ', ' + str(usr.GetStatusesCount()) + '\n'
		outputFile.write(output.encode('utf8'))

############################
#Handle followers style output


if args.type == "followers":
	#Header and build ID list
	print 'Preliminary work ...'
	#Check if ID list is already submitted, otherwise prepare file for saving
	if args.ids:
		idList = open(args.ids, 'r').readlines()
		idList = map(lambda s: int(s.strip()),idList)
	else:
		idList = []
		idFile = open("ID_info.txt", "w")
	
	outputFile.write('Followers, ')
	for author in authorList:
		outputFile.write(author + ', ')
		if args.ids is None:
			print author
			newID=api.GetUser(screen_name=author).GetId()
			idList.append(newID)
			idFile.write(str(newID)+'\n')
	outputFile.write('\n')
	print 'Done!'
	
	#Content
	for author in authorList:
		print author
		output = author + ', '

		#Build follower list
		cursor=-1
		currentCount=5000
		followers=[]
		while currentCount == 5000:
			try:
				newFollowers = api.GetFollowerIDs(screen_name=author, cursor = cursor, total_count=5000)
				currentCount = len(newFollowers)
				cursor += currentCount
				followers += newFollowers
			except twitter.TwitterError as e:
				#Max rate is error code 88
				if e[0][0]['code'] == 88:
					print "Max rate reached, waiting 15 minutes ..."
					time.sleep(900)
				else:
					raise e
		print len(followers)
		#Check for every ID if it is in the follower list and update output line
		for ID_follower in idList:
			if ID_follower in followers:
				output = output + 'Y, '
			else:
				output = output + ', '
		#Clean line and write to file		
		output = output + '\n'
		outputFile.write(output)
#Cleaning		
outputFile.close()
