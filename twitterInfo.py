import twitter
import argparse

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
	print "Followers output"
	outputFile.write("Test\n")



#Cleaning
outputFile.close()
