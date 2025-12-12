Overview
========

This tool is meant to search many different repositories, looking for information contained inside of git databases.

Git is great at storing files and revisions, however there are many ways to lose track of changes made over time.  It is not a simple task to search for data inside of git.  Many folks have created shell scripts and one-line command line tools to search out changes that were lost or simply need to be found.  These are all great, but they tend to be purpose
built, and not usable by others.

This project attemts to consolidate several techniques for seeking out changes in one or more repositories at the same time.

Details
=======
This tool will search the current repo, or many repos, for text in files, commit messages, authors or commit messages.
The tool uses a standard python conditional to qualify the search using these variables:

message - full contents of message converted to lower case
author - author converted to lower case
email - author's email address converted to lower case
files - list of files in the commit

Usage
-----
Example of search in current directroy
gitgrind -f "('myname' in author or 'myname' in email) and 'mydir/myfile.cpp' in files" 

This will find any commits (dangling, in stash, or normal commits) and show the commit information

