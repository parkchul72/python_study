import twitter

CONSUMER_KEY = "7PfWHL33szlVW24dp5dFKZYdI"
CONSUMER_SECRET = "3QQgVcdezhScRk59feRCbKFNTKvTf2HE4Z1G8hyU8SaZR0rEET"
ACCESS_KEY = "43056838-02IGXWGRoBAdrR610t9zJ9JK9jr4lnfW1wcz0FTo6"
ACCESS_SECRET = "FaZU5GkYv36u8KPZ1fOzdTJU3ttZ01rZ6BRn8ktMYtlRv"

def print_users(users):
    for user in users:
        print "[%20s]: %s" % (user.screen_name, user.name)

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_KEY,
                  access_token_secret=ACCESS_SECRET)

friends = api.GetFriends()
followers = api.GetFollowers()
print_users(friends)
print_users(followers)