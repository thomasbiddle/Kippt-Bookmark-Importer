
This project is used to import bookmarks from your browser's bookmark export file into Kippt.com. It solves the issue of keeping previous folders intact and puts them into proper "Lists" with Kippt.

<b>In example:</b>
If you have folders for "Banking", "Travel", "School", etc - Currently with Kippt's bookmark import those folders are lost and all "clips" (Bookmarks) are put into one folder - this script makes new folders, or if one already exists - places the imported bookmarks into the correct folder.

<h2>Web Frontend Use</h2>
<p>The frontend uses Flask as it's web framework. Run the bookmarks_web.py to get things started, then go to localhost:5000/upload and you're all set!


<h6>TODO</h6>
 - Work on web frontend
 - - Host
 - - Fallbacks for incorrect credentials/bad file/etc
 - - Security