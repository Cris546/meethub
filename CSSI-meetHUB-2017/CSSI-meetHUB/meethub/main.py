
import webapp2
import jinja2
import logging
import user
from datetime import datetime
import time

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env2 = jinja2.Environment(loader=jinja2.FileSystemLoader('static_files'))

from google.appengine.api import users
from accountuser import Activity
from accountuser import CssiUser
from accountuser import Friend

# global cssi_user_key



class MainHandler(webapp2.RequestHandler):
    def get(self):

        user = users.get_current_user()
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            # We could also do a standard query, but ID is special and it
            # has a special method to retrieve entries using it.
            user_query = CssiUser.query(CssiUser.user_id == user.user_id())
            theUser = user_query.fetch()

            createpost_link_html = '  <link rel="stylesheet" href="static/mainhub.css"></link> <a href="/create_logout_url">Enter the HUB</a>'
            # If the user has previously been to our site, we greet them!

            if theUser != []:
                enterHub = '/createpost'
                self.response.write('<link rel="stylesheet" href="static/mainhub.css"></link><div id="homepage"><a href="%s">Sign out</a><br><br><a href="%s">EnterHUB</a></div>' % (users.create_logout_url('/'), enterHub))
                #
                #
                # ''
                #       <link rel="stylesheet" href="static/mainhub.css"></link>Welcome %s %s (%s)! <br> %s <br> <a href="%s">Log Out</a>''' % (
                #         cssi_user.first_name,
                #         cssi_user.last_name,
                #         email_address,
                #         createpost_link_html,
                #         users.create_logout_url('/')))
            # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''  <link rel="stylesheet" href="static/mainhub.css"></link>
                    <h2 id= "info">Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action="/">
                    First Name: <input type="text" name="first_name"> <br>
                    Last Name: <input type="text" name="last_name"> <br>
                    Username: <input type="text" name="username"> <br>
                    <br> <input type="submit">
                    </form>
                    ''' % (email_address))
        # Otherwise, the user isn't logged in!
        else:
            self.response.write('''  <link rel="stylesheet" href="static/mainhub.css"></link>
                <h1 class= "login">Welcome to meetHUB!</h1> <br>
                <h2 id="signin"><a href="%s">Sign in</a></h2>''' % (
                    users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.error(500)
            return
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            username=self.request.get('username'),
            # ID Is a special field that all ndb Models have, and esnures
            # uniquenes (only one user in the datastore can have this ID.
            user_id=user.user_id()).put()



        createpost_link_html = '<div id="main2"><a href="/createpost">Enter the HUB</a></div>'
        # cssi_user.put()
        self.response.write(' <link rel="stylesheet" href="static/mainhub.css"></link> <h1 id="thanks">  Thanks for signing up, %s! </h1> <br> %s' % (
            self.request.get('first_name'),
            createpost_link_html))

# class DeleteDatabase(webapp2.RequestHandler):
#     def get(self):
#         query = CssiUser.query()
#         all_users = query.fetch()
#         for person in all_users:
#           person.key.delete()
#         query2 = Activity.query()
#         all_activities = query2.fetch()
#         for act in all_activities:
#           act.key.delete()

class CreatePost(webapp2.RequestHandler):
    def get(self):
        # all_users = CssiUser.query().fetch()
        # for usernames in all_users:
        #     if user == usernames.userID:
        #         current_user_key = usernames.key
        # user_key = user.get('key')
        # console.log(user_key)
        # theId = user.user_id()
        user = users.get_current_user()
        user_query = CssiUser.query(CssiUser.user_id == user.user_id())
        current_user_data = user_query.get()
        # self.response.write(current_user_data.username)


        main_template = env.get_template('mainhub.html')
        blog_posts = Activity.query().order(-Activity.date).fetch()
        variables = {'posts': blog_posts}
        self.response.write(main_template.render(variables))

    def post(self):
        post_date = datetime.now()
        # text_input = self.request.get('activity_name')

        user = users.get_current_user()
        user_query = CssiUser.query(CssiUser.user_id == user.user_id())
        current_user_data = user_query.get()

        # global cssi_user_key

        new_post = Activity(name = self.request.get('activity_name'), date = post_date, user=current_user_data.username)
        new_post.put()
        # console.log(new_post)
        time.sleep(1)
        blog_posts = Activity.query().order(-Activity.date).fetch()
        variables = {'posts':blog_posts}
        posts_template = env.get_template('mainhub.html')
        self.response.write(posts_template.render(variables))


class SearchHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('search.html')
        self.response.write(main_template.render())
    def post(self):
        user = users.get_current_user()
        print user
        print user.user_id()
        cssi_user = CssiUser.query(CssiUser.user_id == user.user_id()).get()
        print cssi_user
        your_id = cssi_user.username
        print your_id
        username = self.request.get('search_name')
        friend_user = CssiUser.query(CssiUser.username==username).get()
        if friend_user:
            new_friend = Friend(friend_id= username, your_id= your_id)
            new_friend.put()
            self.response.write("Friend added")
        else:
            self.response.write('User does not exist, please try again <a href="/search">Search for Friends </a>')
        # all_users = CssiUser.query(CssiUser.user_id() != your_id).fetch()
        # variables = {'users': all_users, 'username': username}
        # search_template = env.get_template('search.html')
        # self.response.write(search_template.render(variables))
        # for u_name in all_users:
        #     if username == u_name.userID:
        #         logging.info(u_name.userID)
        # json_string = self.request.body
        # json_object = json.loads(json_string)
        # items = json_object['items']
        # friend_user_name = (json_object['name'])
        # reply_data = {
        # 'name': friend_user_name
        # }
        # self.response.headers['Content-Type'] = "application/json"
        # self.response.write(json.dumps(reply_data))

# class LogOutHandler(webapp2.RequestHandler):
#     def get(self):



#cssi_user = CssiUser(userID="ndsimone", first_name = "Nick", last_name = "dane")
#cssi_user_key = cssi_user.put()
#         all_users = CssiUser.query().fetch()
# username = "ndsimone"
# for u_name in all_users:
#   if username == u_name.userID:
#     print "Yes"


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/createpost', CreatePost),
    # ('/deletedatabase', DeleteDatabase),
    ('/search', SearchHandler),
    # ('/logout' SignOutHandler)
], debug=True)
