import datetime

from google.appengine.api import mail
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app


class ChatMessage(db.Model):
    user = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    message = db.TextProperty(required=True)

    def __str__(self):
        return "%s (%s): %s" % (self.user, self.timestamp, self.message)


startTimestamp = datetime.datetime.now()


class ChatRoomPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
            <html>
                <head>
                    <title>Dustin's AppEngine Chat Room</title>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" />
                </head>
                <body>
                    <h1>Welcome to Dustin's AppEngine Chat Room</h1>
                    <p>(Current time is %s)</p>
                    <p>(Server started at %s)</p>
                    """ % (datetime.datetime.now(), startTimestamp))
        # Output the set of chat messages
        messages = db.GqlQuery("SELECT * From ChatMessage ORDER BY timestamp")
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
                    <form action="/talk" method="post">
                        <div>
                            <b>Name:</b>
                            <textarea name="name" rows="1" cols="20"></textarea>
                        </div>
                        <p><b>Message</b></p>
                        <div><textarea name="message" rows="5" cols="60"></textarea></div>
                        <div><input type="submit" value="Send ChatMessage"></input></div>
                    </form>
                </body>
            </html>
        """)


class ChatRoomCountViewPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
            <html>
                <head>
                    <title>Dustin's AppEngine Chat Room</title>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" />
                </head>
                <body>
                    <h1>Welcome to Dustin's AppEngine Chat Room</h1>
                    <p>(Current time is %s; viewing the 20 last messages)</p>
                    <p>(Server started at %s)</p>
                    """ % (datetime.datetime.now(), startTimestamp))
        # Output the set of chat messages
        messages = db.GqlQuery("SELECT * From ChatMessage ORDER BY timestamp DESC LIMIT 20").fetch(20)
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
                    <form action="/talk" method="post">
                        <div>
                            <b>Name:</b>
                            <textarea name="name" rows="1" cols="20"></textarea>
                        </div>
                        <p><b>Message</b></p>
                        <div><textarea name="message" rows="5" cols="60"></textarea></div>
                        <div><input type="submit" value="Send ChatMessage"></input></div>
                    </form>
                </body>
            </html>
        """)


class ChatRoomTimeViewPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
            <html>
                <head>
                    <title>Dustin's AppEngine Chat Room</title>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" />
                </head>
                <body>
                    <h1>Welcome to Dustin's AppEngine Chat Room</h1>
                    <p>(Current time is %s)</p>
                    <p>(Server started at %s)</p>
                    """ % (datetime.datetime.now(), startTimestamp))
        # Output the set of chat messages
        messages = ChatMessage.gql("WHERE timestamp > :fiveago ORDER BY timestamp",
                                   fiveago=datetime.datetime.now() - datetime.timedelta(minutes=5))
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
                    <form action="/talk" method="post">
                        <div>
                            <b>Name:</b>
                            <textarea name="name" rows="1" cols="20"></textarea>
                        </div>
                        <p><b>Message</b></p>
                        <div><textarea name="message" rows="5" cols="60"></textarea></div>
                        <div><input type="submit" value="Send ChatMessage"></input></div>
                    </form>
                </body>
            </html>
        """)


class ChatRoomEmailViewPage(webapp.RequestHandler):
    def get(self):
        mail.send_mail("chat@vvs-praktikum-2019.appspotmail.com", "dustin.hellmann@alumni.fh-aachen.de",
                       "Hi Dustin!", "I'm still running")
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
            <html>
                <head>
                    <title>Dustin's AppEngine Chat Room</title>
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css" />
                </head>
                <body>
                    <h1>An Email was sent to the administrator!</h1>
                    <p>(Current time is %s)</p>
                    <p>(Server started at %s)</p>
                    """ % (datetime.datetime.now(), startTimestamp))
        self.response.out.write("""
                </body>
            </html>
        """)


class ChatMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        mail.send_mail(sender="admin@vvs-praktikum-2019.appspotmail.com",
                       to="dustin.hellmann@alumni.fh-aachen.de",
                       subject="CHAT ADMIN MAIL: %s" % mail_message.subject,
                       body="Original message from: %s\n%s" %
                            (mail_message.sender,
                             mail_message.body))


class ChatRoomPoster(webapp.RequestHandler):
    def post(self):
        chatter = self.request.get("name")
        msgtxt = self.request.get("message")
        msg = ChatMessage(user=chatter, message=msgtxt)
        msg.put()
        self.redirect('/limited/time')


chatapp = webapp.WSGIApplication([('/', ChatRoomPage),
                                  ('/talk', ChatRoomPoster),
                                  ('/limited/count', ChatRoomCountViewPage),
                                  ('/limited/time', ChatRoomTimeViewPage),
                                  ('/email', ChatRoomEmailViewPage)])


def main():
    run_wsgi_app(chatapp)


if __name__ == "__main__":
    main()
