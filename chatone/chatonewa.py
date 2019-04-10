from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime


serverStartupTime = datetime.datetime.now()


class WelcomePage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write(
            """<html>
                <head>
                    <title>Welcome to Dustin's chat service</title>
                </head>
                <body>
                    <h1>Welcome to Dustin's chat service</h1>
                    <h1>The better alternative to WhatsApp</h1>
                <p> The current time is: %s</p>
                <p> The server started at: %s </p>
                </body>
               </html>
            """ % (datetime.datetime.now(), serverStartupTime))


chatapp = webapp.WSGIApplication([('/', WelcomePage)])


def main():
    run_wsgi_app(chatapp)


if __name__ == "__main__":
    main()
