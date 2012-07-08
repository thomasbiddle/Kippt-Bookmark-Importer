import json, urllib, requests, sys
import kippt_wrapper as kippt # Kippt Python Wrapper can be found at https://github.com/thomasbiddle/Kippt-Python-Wrapper
	
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print "Please start the script like so: python kippt.py <username> <API_Token> <Bookmark_File_Location>"
	else:
		#	Gather our user's credentials and test the request, exit if invalid.
		client = kippt.user(sys.argv[1], sys.argv[2])
		in_filename = sys.argv[3]
		if not (client.checkAuth()):
			print 'Invalid Username/Token Combination'
			sys.exit()
		
		#	Get a collection of our lists.
		meta, lists = client.getLists()
		
		#   Constants
		ENDFOLDER = "</DL><p>"
		PREFIX = "<DT><H3 ADD_DATE="
		LINK = '<DT><A'
		
		#   Input file
		try:
			f=open(in_filename, 'r+')
		except IOError:
			print in_filename, ' does not exist.'
			sys.exit()
		
		#   Read in the whole input file.
		line_list = f.readlines()
		f.close()
		
		currentFolder = ""
		
		if line_list[0].strip() != '<!DOCTYPE NETSCAPE-Bookmark-file-1>':
			print 'Improperly formatted Bookmark File'
			sys.exit()
		
		for x in line_list:
			#   Remove all leading whitespace.
			line = x.lstrip()
			if line.startswith(PREFIX):
				#   This line tells us about a folder.
				#   Find the next '>' after the prefix.
				lpos = line.find('>', len(PREFIX))
				if lpos > 0:
					#   Find the next '<' after the '>'.
					rpos = line.find('<', lpos)
					#   Extract the folder name.
					currentFolder = line[lpos + 1:rpos]
					
			elif line.startswith(ENDFOLDER):
				currentFolder = ""
					
			elif line.startswith(LINK):
				#	We've found a link, let's grab the information from it.
				linkbeg = line.find('HREF="', len(LINK))
				linkend = line.find('"', linkbeg+6)
				thelink = line[linkbeg+6:linkend]

				#	Make sure it's a real link and not one for the browser, break if it's not.
				if thelink[:4] == 'http':
					#	Let's get the title.
					linktitle = line[line.find('>', linkend)+1:line.find('<', linkend)]
					
					#	Add it to our Kippt Clips
					#	First check if we have a list already with the same name as our folder.
					listID = 0
					for i in lists:
						if i['title'] == currentFolder:
							listID = i['id']
					if listID == 0:
						if len(currentFolder) > 0:
							listID = client.createList(currentFolder)['id']
							#	Update our list information.
							meta, lists = client.getLists()
					client.addClip(url=thelink, listID=listID, title=linktitle)
				
		