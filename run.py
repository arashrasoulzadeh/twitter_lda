# encoding=utf8
# imports
import pprint
import sqlite3
import string
from datetime import datetime

from tqdm import tqdm

conn = sqlite3.connect('web/db.sqlite3')

pp = pprint.PrettyPrinter(indent=4)
# statements
print("starting application ...")

# data
path = 'test.txt'
data = []
person = []
time = []
tweet = []

# read
with open(path, encoding="utf-8") as f:
    data += f.readlines()

data = data[1:]

RTcount = 0
FAVcount = 0

step = 1


class Twitt():
    username, date, text = "", "", ""

    def __init__(self):
        pass

    def __str__(self):
        return "'{}' : '{}' at '{}' ".format(self.username, self.text, self.date)


twitts = []
currentTwitt = Twitt()
for item in data:
    if step is 1:
        dt = item[2:].rstrip()
        datetime_object = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        currentTwitt.date = datetime_object
        time += [item]
    elif step is 2:
        item = item[9:].rstrip()
        currentTwitt.username = item.replace("twitter.com/", "")
        person += [item]
    elif step is 3:
        currentTwitt.text = item[2:].rstrip()
        tweet += [item]
    if step is 4:
        step = 1
        twitts += [currentTwitt]
        currentTwitt = Twitt()
    else:
        step += 1

person = list(map(lambda x: x[:len(x)], person))

data = []
for p, d, t in zip(person, time, tweet):
    if " RT " in t:
        RTcount += 1
    if " @ " in t:
        FAVcount += 1

    data += [{"person": p, "time": d, "tweet": t}]

unique = []
[unique.append(item) for item in person if item not in unique]

print("FAV COUNT {},RT COUNT {}, TWEETES {}".format(FAVcount, RTcount, len(tweet)))

print(twitts[40])
c = conn.cursor()


def getId(username):
    sql = "SELECT * FROM panel_twitterusers WHERE username='twitter.com/{}'".format(username)
    c.execute(sql)
    row = c.fetchone()
    return row

# add twitts 

# for twitt in tqdm(twitts):
#     try:
#         sql = "INSERT INTO panel_twitterpost VALUES (null,'{}','{}',{})".format(twitt.text, twitt.date,
#                                                                                  getId(twitt.username)[0])
#         print(sql)
#         c.execute(sql)
#         c.execute("COMMIT")
#     except:
#         pass


# add users

#
# for p in tqdm(person):
#     try:
#         c.execute("INSERT INTO panel_twitterusers VALUES (null,'{}')".format(p))
#         c.execute("COMMIT")
#     except:
#         pass
# print("not added: {} , exist".format(p))

# from here on the gui

# TODO :: user activitys

# todo :: lda topic extraction  for each month or day  (or by hashtag)

# todo :: rt netowrk for each topic

# TODO :: what is difference of reply and mention

# TODO :: interaction matrix


# todo :: rt netowrk
