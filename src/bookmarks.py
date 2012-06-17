# TODO
# Code is incredibly sloppy right now with the way I'm parsing the bookmarks file - Clean this up. Use a stack data structure.
# Also, after restructuring the parser, clean up how we create the lists & clips.
# 
# Check if file exists
# Check to ensure file is valid bookmark file (Check first line for <!DOCTYPE NETSCAPE-Bookmark-file-1> ?)

import json, urllib, requests, sys
from HTMLParser import HTMLParser

# Authentication ( With Python Requests )
def pyRespAuth(headers):
	r = requests.get('https://kippt.com/api/account/', headers=header_py_requests)
	print "Authentication Response: "
	if r.status_code == 200:
		print "Username: \t" + r.json['username']
		print "API Token: \t" + r.json['api_token']
		return True
	else:
		print "Invalid username/API token combination."
		return False
		
# Creating Clip ( With Python Requests )
def pyRespCreateClip(url, listID):	
	clipdata = {'url': url, 'list': '/api/lists/' + listID}
	r = requests.post('https://kippt.com/api/clips/', data=json.dumps(clipdata), headers=header_py_requests)

# Creating List ( With Python Requests )	
def pyRespCreateList(name):
	clipdata = {'title': name}
	r = requests.post('https://kippt.com/api/lists/', data=json.dumps(clipdata), headers=header_py_requests)
	return r.json['id']
	
def getListObj(headers):
	r = requests.get('https://kippt.com/api/lists', headers=header_py_requests)
	return r.json['objects']

class MyHTMLParser(HTMLParser):
	inA = False
	inH3 = False
	inP = False # Needs to be False if from Chrome and True if from FF - Not sure why...
	curFolder = ""
	
	isLink = False
	curLink = ""
	curTitle = ""
	
	def handle_starttag(self, tag, attrs):
		if tag == "a":
			attrs = dict(attrs)
			if attrs['href'][:4] == 'http':
				#print "Bookmark link: \t", attrs['href']
				self.curLink = attrs['href']
				self.isLink = True
				if self.inP:
					bob = None
					#print "In Folder: \t" + self.curFolder
				else:
					self.curFolder = ""
					#print "Not in a folder."
				self.inA = True
		if tag == 'h3':
			self.inH3 = True
		if tag == 'p':
			if self.inP == False:
				self.inP = True
			else:
				self.inP = False
	def handle_data(self, data):
		if self.inA:
			#print "Bookmark title: ", data
			self.curTitle = data
			self.inA = False
			#print
		if self.inH3:
			self.curFolder = data
			self.inH3 = False
	
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print "Please start the script like so: python kippt.py <username> <API_Token>"
	else:
		# Gather our user's credentials and test the request, exit if invalid.
		username = sys.argv[1]
		apitoken = sys.argv[2]
		filename = sys.argv[3]
		header_py_requests = {'X-Kippt-Username': username, 'X-Kippt-API-Token': apitoken, 'X-Kippt-Client': 'ThomasBiddle-Kippt-Bookmark-Importer,me@ThomasBiddle.com,https://github.com/thomasbiddle/Kippt-Projects', 'content-type': 'application/vnd.kippt.20120609+json'}
		if not (pyRespAuth(header_py_requests)):
			sys.exit()
		print
			
		# Get our user's Kippt lists.
		listObj = getListObj(header_py_requests)
		
		# Read in our bookmarks.html file.
		with open(filename, "r") as f:
			bookmark_lines = f.readlines()
			parser = MyHTMLParser()
			for x in bookmark_lines:
				parser.feed(x)
				if parser.isLink:
					listObj = getListObj(header_py_requests)
					foundList = False
					print "Title: \t", parser.curTitle
					print "Folder: \t", parser.curFolder
					print "Link: \t", parser.curLink
					for x in listObj:
						if x['title'] == parser.curFolder:
							print "Found match! ID: " + str(x['id'])
							pyRespCreateClip(parser.curLink, str(x['id']))
							foundList = True
					if not foundList:
						if len(parser.curFolder) > 0:
							newFolderID = pyRespCreateList(parser.curFolder)
							pyRespCreateClip(parser.curLink, str(newFolderID))
						else:
							pyRespCreateClip(parser.curLink, "0")
					#print "Title: \t", parser.curTitle
					#print "Folder: \t", parser.curFolder
					#print "Link: \t", parser.curLink
					parser.isLink = False
		f.close()
		