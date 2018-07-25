# -*- coding: utf-8 -*-


import http.client, urllib.parse, json, time

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

class qnamker:

    def __init__(self):
        pass

    def get_answer(self, quest):

        question = {
            'question': quest,
            'top': 3
        }
        self.content = json.dumps(question)
        self.__focus_process__()
        return self.pretty_print()

    def pretty_print(self):
    # Note: We convert content to and from an object so we can pretty-print it.
        return json.loads(self.content)['answers'][0]['answer']

    def __focus_process__ (self):
        #print ('Calling ' + self.host + self.path + '.')
        headers = {
            'Authorization': 'EndpointKey ' + self.endpoint_key,
            'Content-Type': 'application/json',
            'Content-Length': len (self.content)
        }
        conn = http.client.HTTPSConnection(self.host)
        conn.request ("POST", self.method, self.content, headers)
        response = conn.getresponse ()
        self.content = response.read ()
