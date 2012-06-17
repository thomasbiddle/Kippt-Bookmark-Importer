
This project is used to import bookmarks from your browser's bookmark export file into Kippt.com. It solves the issue of keeping previous folders intact and puts them into proper "Lists" with Kippt.

<b>In example:</b>
If you have folders for "Banking", "Travel", "School", etc - Currently with Kippt's bookmark import those folders are lost and all "clips" (Bookmarks) are put into one folder - this script makes new folders, or if one already exists - places the imported bookmarks into the correct folder.

<h6>TODO</h6>
<ul>
	<li>Bookmark Importer</li>
		<ul>
			<li>Authentication &#x2713;</li>
			<li>Reading Bookmark File &#x2713;</li>
			<li>Parsing Bookmark File &#x2717; (Works, but sloppy and want to update)</li>
			<li>Create lists for bookmarks that were in a folder previously &#x2713;</li>
			<li>Upload clip to proper list &#x2713;</li>
		</ul>
	</ul>
</ul>

<h6>Issues</h6>
<ul>
	<li>Bookmark Importer</li>
		<ul>
			<li>Chrome doesn't recognize it's in a folder hierarchy without flipping the flag for it. Issue #1 &#x2717;</li>
		</ul>
	</ul>
</ul>