#!/usr/bin/python
from linkedin import linkedin

#Create LinkedIn application object
authentication = linkedin.LinkedInDeveloperAuthentication(
"ewawn2wwgpz9",
"SX7DZgcP4EnHoq7t", 
"0cd819ef-5981-4883-96c7-2c560ef79850",
"72b8fe58-671b-4660-ba4c-673365cb80e1",
"http://localhost:8000",
linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

#Extract LinkedIn URLs
urlList = open('linkedin_1.txt', 'r').readlines()
urlList = map(lambda s: s.strip(), urlList)

#Write header
outputFile = open('Linkedin_Info.txt', 'w')
outputFile.write("LinkedIn URL, real name, connections, headline\n")

for url in urlList:
	#Get standard profile information
	profile = application.get_profile(member_url=url, selectors=['first-name', 'last-name', 'num-connections', 'headline'])
	output = url + ', ' + profile['firstName'].encode('utf8') + ' ' + profile['lastName'].encode('utf8') + ', '
	
	#Num connections not always present
	if 'numConnections' in profile :
		output = output + str(profile['numConnections']) + ', '
	else :
		output = output + '#, '
	#Same for headline
	if 'headline' in profile :
		output = output + profile['headline'].encode('utf8') + ', '
	else :
		output = output + '#, '

	#Try to fetch membership
	try:
		groups =application.get_memberships(member_url=url)
		print groups
	except linkedin.LinkedInError:
		pass
	
	output = output + '\n'
	outputFile.write(output)
	print profile['lastName']


