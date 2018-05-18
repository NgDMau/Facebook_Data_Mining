# Facebook_Data_Mining
Downloads all public posts on a Facebook page
Requirements:

-> Python 3 installed
-> json, requests, string, re, threading installed

Create a folder you want to store data, and place the FacebookDataMining.py in.

If you do not have these packages installed (rarely), the program will install them for you.

First create a text file containing links to the pages from which you want to download posts'content (Each link is on a distinct line, and do not leave any empty line between links).

In the terminal, type:
python FacebookDataMining.py arg[1] arg[2] arg[3]  and wait until the program finishes.

arg[1]: name of the label of data that you want to store.
arg[2]: path to the text file containing links to the pages.
arg[3]: access token from any typical facebook account (open developer.facebook.com for more detail).
