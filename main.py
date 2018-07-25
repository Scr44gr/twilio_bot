# -*- coding: utf-8 -*-
# Imports
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from src.google import news
from src.google import search_news
from src.ai import qnamker
import re

NEWS = news()
NEWS.run()
SEARCH_NEWS = search_news()
AI = qnamker()
# connect to local host w/ Flask (and later to www through ngrok)
app = Flask(__name__)


# Main function
# triggered by a POST request by ngrok
# when an SMS is received, Twilio will send the POST
@app.route('/sms', methods=['POST'])
def sms():
    """
    Use Twilio API to reply to texts
    """
    number = request.form['From']
    message = request.form['Body']      # text from SMS
    response = MessagingResponse()         # init a Twilio response
    print(number)
    if str(number) == str("+16476946020"):
        print("yep")
    if re.search(r'news(.*)', message.lower()):

        if re.search(r'about(.*)', message.lower()) or re.search(r'of(.*)', message.lower()):
            message = message.replace('about', '').replace('About', '').replace('news', '').replace('News', '').replace('of').replace('Of', '')
            s = SEARCH_NEWS.search(q=message)
            response.message(s)

        else:
            s = NEWS.get_news()
            if s == "RESTART":
                NEWS.run()
            else:
                response.message(s)
    else:
        s = AI.get_answer(message)
        response.message(s)

    print("Message obtained by {}:".format(number))
    print("{}".format(message))
    return str(response)

@app.route('/')
def index():
    return "<h1> TEST tovishalpanchal </h1>"


def remove_from(message, keyword):
    """
    Strip the message from the keyword
    """
    message = message.replace(keyword, '').strip()
    return message

if __name__ == '__main__':
    app.run(debug=True, port=80)