import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

DATA_LST = ['name', 'location', 'description', 'friends_count', 'created_at', 'statuses_count']
# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def info(elem, acct):
    print('')

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    print('Retrieving', url)
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    # print(json.dumps(js, indent=2))

    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])

    if elem == 'latest status':
        for u in js['users']:
            print(u['screen_name'])
            try:
                print(u['status']['text'])
            except:
                print("No such data on this user.")
    elif elem == 'all':
        for u in js['users']:
            print(u['screen_name'])
            try:
                for i in DATA_LST:
                    print(u[i])
                print(u['status']['text'])
            except:
                print("No such data on this user.")
    else:
        for u in js['users']:
            print(u['screen_name'])
            try:
                print(u[elem])
            except:
                print("No such data on this user.")


if __name__ == "__main__":
    acct = input('Enter Twitter Account:')
    print("Available data: name, location, description, friends_count, created_at, statuses_count, latest status, all")
    lst = []
    while True:
        print("press ENTER to stop")
        word = str(input("What do you want to see? Choose one or some of the above: ")).strip()
        if len(word) < 1:
            break
        lst.append(word)
    for i in lst:
        print("******* {} *******".format(i))
        info(i, acct)
