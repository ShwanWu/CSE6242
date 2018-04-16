import csv
import json
import time
import tweepy

# You must use Python 2.7.x

# 1 point
def loadKeys(key_file):
    # TODO: put your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    # Load keys here and replace the empty strings in the return statement with those keys
    with open('keys.json', 'r') as f:
        d = json.load(f)
    return str(d['api_key']), str(d['api_secret']), str(d['token']), str(d['token_secret'])

# 4 points
def getPrimaryFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' primary friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    primary_friends_list = api.friends(root_user)
    # Add code here to populate primary_friends
    if len(primary_friends_list) < no_of_friends:
        for each_user in primary_friends_list:
            primary_friends.append((root_user, str(each_user.screen_name)))
    else:
        for i in range(0, no_of_friends):
            primary_friends.append((root_user, str(primary_friends_list[i].screen_name)))
    print "primary_friends:"
    print primary_friends
    return primary_friends

# 4 points
def getNextLevelFriends(api, users_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    next_level_friends = []
    # Add code here to populate secondary_friends
    for users in users_list:
        try:
            next_level_friends_list = api.friends(users[1])
        except tweepy.TweepError:
            print("User: " + users[1] + " is protected. Not be able to get his/her friends.")
        if len(next_level_friends_list) < no_of_friends:
            for each_user in next_level_friends_list:
                next_level_friends.append((users[1], str(each_user.screen_name)))
        else:
            for i in range(0, no_of_friends):
                next_level_friends.append((users[1], str(next_level_friends_list[i].screen_name)))
    print "next_level_friends:"
    print next_level_friends
    return next_level_friends

# 4 points
def getNextLevelFollowers(api, users_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each user in users_list
    # rtype: list containing entries in the form of a tuple (follower,friends_list[i] )
    next_level_followers = []
    # Add code here to populate next_level_followers
    for users in users_list:
        try:
            next_level_followers_list = api.followers(users[1])
        except tweepy.TweepError:
            print("User: " + users[1] + " is protected. Not be able to get his/her followers.")
        if len(next_level_followers_list) < no_of_followers:
            for each_user in next_level_followers_list:
                next_level_followers.append((str(each_user.screen_name), users[1]))
        else:
            for i in range(0, no_of_followers):
                next_level_followers.append((str(next_level_followers_list[i].screen_name), users[1]))
    print "next_level_followers:"
    print next_level_followers
    return next_level_followers

# 3 points
def GatherAllEdges(api, root_user, no_of_neighbours):
    # TODO:  implement this method for calling the methods getPrimaryFriends, getNextLevelFriends
    #        and getNextLevelFollowers. Use no_of_neighbours to specify the no_of_friends/no_of_followers parameter.
    # NOT using the no_of_neighbours parameter may cause the autograder to FAIL.
    # Accumulate the return values from all these methods.
    # rtype: list containing entries in the form of a tuple (Source, Target). Refer to the "Note(s)" in the
    # Question doc to know what Source node and Target node of an edge is in the case of Followers and Friends.
    all_edges = []
    # Add code here to populate all_edges
    primary_friends = getPrimaryFriends(api, root_user, no_of_neighbours)
    next_level_friends = getNextLevelFriends(api, primary_friends, no_of_neighbours)
    next_level_followers = getNextLevelFollowers(api, primary_friends, no_of_neighbours)
    all_users = primary_friends + next_level_friends + next_level_followers
    all_edges.extend(all_users)
    print "all_edges:"
    print all_edges
    return all_edges

# 2 points
def writeToFile(data, output_file):
    # write data to output_file
    # rtype: None
    with open(output_file, 'wb') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for row in data:
            writer.writerow(row)
    pass




"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_GRAPH = 'graph.csv'
    NO_OF_NEIGHBOURS = 20
    ROOT_USER = 'PoloChau'

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    edges = GatherAllEdges(api, ROOT_USER, NO_OF_NEIGHBOURS)
    writeToFile(edges, OUTPUT_FILE_GRAPH)

if __name__ == '__main__':
    testSubmission()

