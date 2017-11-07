import json
import urllib.request as ur

# For getting access token: https://graph.facebook.com/oauth/access_token?client_id=______&client_secret=_________&grant_type=client_credentials

def get_feedPosts(access_token,pageId,numPost=15):
	"""Returns a dictionary of the posts of a page with postId as a key and the first line of the messgage/story as value.

	Parameters: 
	access_token - Generated using API key to communicate with the Graph API
	pageId - The id of the page you want to scrape. If you can't find the id of the page, search page_id in the source code of the page
	numPosts - The number of posts you want to scrape, maximum limit of graph API is 100

	"""
	postDict ={}
	postID_array=[]
	url=ur.urlopen("https://graph.facebook.com/v2.10/"+str(pageId)+"/feed?limit=" + str(numPost) + "&access_token=" + access_token)
	url = json.loads(url.read())
	for i in url['data']:
		if 'message' in i.keys():
			try:
				postDict[i['id']]=[i['message'][:i['message'].index("\n")]]
			except ValueError:
				postDict[i['id']]=[i['message']]
		elif 'story' in i.keys():
			postDict[i['id']]=[i['story']]
		#postDict[i['id']]=i['story']

	return postDict

def get_CommentLikes(access_token,postId):
	"""Returns the number of likes and comments for a particular post.

	Parameters: 
	access_token - Generated using API key to communicate with the Graph API
	postId - The id of the post you want, can be obtained from get_feedPosts function
	"""
	comment_likes = ur.urlopen("https://graph.facebook.com/v2.10/"+str(postId)+"?fields=comments.summary(total_count),likes.summary(total_count)&access_token=" + access_token)
	comment_likes = json.loads(comment_likes.read())
	commentCount = comment_likes["comments"]["summary"]["total_count"]
	likeCount = comment_likes["likes"]["summary"]["total_count"]
	return commentCount, likeCount

def sortByLikes(jsonDict):
	"""Returns a dictionary sorted by the number of likes

	Parameter:
	jsonDict - Obtained by reading the file formed by savePostsToFile function
				The values in jsonDict are lists with first element as the message, 
				second element as likes and third element as number of comments 

	"""
	sortedLikes = sorted(jsonDict.items(), key = lambda x: x[1][1],reverse = True)
	return sortedLikes
	
def sortByComments(jsonDict):
	"""Returns a dictionary sorted by the number of comments

	Parameter:
	jsonDict - Obtained by reading the file formed by savePostsToFile function
				The values in jsonDict are lists with first element as the message, 
				second element as likes and third element as number of comments 

	"""
	sortedComments = sorted(jsonDict.items(), key = lambda x: x[1][2], reverse = True)
	return sortedComments

def savePostsToFile(token,pageId,num):
	"""Writes output to a file 'posts.txt' 
	
	Parameters:
	token - Generated using API key to communicate with the Graph API
	pageId - The id of the page you want to scrape. If you can't find the id of the page,
			 search page_id in the source code of the page
	num - The number of posts you want to scrape, maximum limit of graph API is 100

	Output:
	A file containing a dictionary with keys as post_id and values as list with message, 
	no. of likes and no. of comments as 0th,1st and 2nd elements respectively.
	
	giveJsonDict function has also been created for reading the file created by this function and converting it to dictionary
	which can be given as a input to the sortedByLikes and sortedByComments functions.
	"""
	posts = get_feedPosts(token,pageId,num)
	for i in posts.keys():
		comments,likes = get_CommentLikes(token,i)
		posts[i].append(likes)
		posts[i].append(comments)
	#print(posts)
	with open("posts.txt","w",encoding='utf-8') as file:
			file.write(str(posts))



def giveJsonDict():
	"""Returns a jsonDict which can be used by sortedByLikes and sortedByComments functions 
	The file read is the output of savePostsToFile function
	"""
	readFile = open("posts.txt","r")  #Change  the name of file if you have saved it in another file
	feedData = eval(readFile.read())
	readFile.close()
	return feedData


def saveSortedLikesToFile(feedData):
	"""Writes posts sorted by likes to a file SortedByLikes.txt in human readable format

	Parameter:
	feedData - the dictionary returned by giveJsonDict function
	"""
	sortedDataLikes = sortByLikes(feedData)
	print("Sorted by Likes")
	with open("SortedByLikes.txt","w",encoding='utf-8') as f:
		f.write("#Likes \t Story \n")
		for i in sortedDataLikes:
			likes = i[1][1]
			story = i[1][0]
			f.write("%d \t %s \n" % (likes,story))

def saveSortedCommentsToFile(feedData):
	"""Writes posts sorted by comments to a file SortedByComments.txt in human readable format

	Parameter:
	feedData - the dictionary returned by giveJsonDict function
	"""
	sortedDataComments = sortByComments(feedData)
	print("Sorted by Comments")
	with open("SortedByComments.txt","w",encoding='utf-8') as f:
		f.write("#Comments \t Story \n")
		for j in sortedDataComments:
			comments = j[1][2]
			story = j[1][0]
			f.write("%d \t %s \n" % (comments,story))

#---------------------------------------------------------------------------------#

#Sample usage:
# For getting access token: https://graph.facebook.com/oauth/access_token?client_id=______&client_secret=_________&grant_type=client_credentials
# If you can't find the id of the page, search page_id in the source code of the page

pageId = #Assingn page id 
token = #Assign access token

#This may take upto 80-90 seconds if you do with 100 posts

savePostsToFile(token,pageId,100)  #Saves 100 posts to posts.txt
feedData = giveJsonDict() #Reads posts.txt and creates a dictionary
saveSortedCommentsToFile(feedData) #Creates SortedByComments.txt in human readable format
saveSortedLikesToFile(feedData) #Creates SortedByLikes.txt in human readable format