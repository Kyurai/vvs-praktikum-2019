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


class ChatMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        user = mail_message.sender
        message = ""
        for content_type, body in mail_message.bodies('text/plain'):
            message += body.decode()

        msg = ChatMessage(user=user, message=message)
        msg.put()

        mail.send_mail(sender="admin@vvs-praktikum-2019.appspotmail.com",
                       to=mail_message.sender,
                       subject="CHAT ADMIN MAIL: %s" % mail_message.subject,
                       body="Original message from: %s\n%s" %
                            (mail_message.sender,
                             message))


chatmail = webapp.WSGIApplication([ChatMailHandler.mapping()])


def main():
    run_wsgi_app(chatmail)


if __name__ == "__main__":
    main()
