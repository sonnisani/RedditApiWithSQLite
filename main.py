import praw
import sqlite3
import urllib
import pathlib

#Initialization
Main = 'main'
PathFile = str(pathlib.Path(__file__).parent.absolute())
PathFile = PathFile + PathFile[2] + 'venv' + PathFile[2] + 'Test.db'

#Connect to SQLite
conn = None
try:
    conn = sqlite3.connect(PathFile)
except EOFError as e:
    print(e)
cur = conn.cursor()

#Reddit Log in
reddit = praw.Reddit(client_id='', \
 client_secret='', \
 user_agent='', \
 username='', \
 password='')

#Main
SubName = 'AskReddit'
subreddit = reddit.subreddit(SubName)
CreateTable = 'CREATE TABLE IF NOT EXISTS %s (URL text , Title text)'
cur.execute(CreateTable %SubName)
conn.commit()
for submmission in subreddit.top(limit = 10):
    url = submmission.url
    Title = submmission.title
    if '.png' in url:
        urllib.request.urlretrieve(url,(submmission.title.replace(' ','') + '.png'))
    elif '.jpg' in url:
        urllib.request.urlretrieve(url, (submmission.title.replace(' ', '') + '.jpg'))
    sql = 'INSERT INTO %s VALUES (?,?)'
    cur.execute(sql %SubName , (url,Title))
conn.commit()