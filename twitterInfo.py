import twitter

#Create twitter API
api = twitter.Api(
consumer_key="grfzFcIHU6kiS3xshGUf6Q",
consumer_secret="KKqYXiNCWMuLzIlmx8OLkXG4i3Fsn8i7SNIKC71SOQ",
access_token_key="138811547-PdVqwI2Ne1D2n6gX4IHQnUrICXZl6zqxx79vL6Vm",
access_token_secret="WTokWyRynBMa8FIWIHWWiGJR2bYgPWYcwkH6IowtYRtoy")

#Extract author list
authorList = open('authors.txt', 'r').readlines()
authorList = map(lambda s: s.strip(), authorList)

#Write header
outputFile = open('Author_Info.txt', 'w')
outputFile.write("Twitter name, real name, followers, following, tweets\n")

for author in authorList:
	print author
	usr = api.GetUser(screen_name=author)
	output = author + ', ' + usr.GetName() + ', ' + str(usr.GetFollowersCount()) + ', ' + str(usr.GetFriendsCount()) + ', ' + str(usr.GetStatusesCount()) + '\n'
	outputFile.write(output.encode('utf8'))

outputFile.close()
