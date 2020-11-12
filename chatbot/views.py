from django.shortcuts import render

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json

# Create your views here.
PAGE_ACCESS_TOKEN = "EAAI9ufmy7xkBAAIgZB0UR4u50QsvYHPFuPx6hLUvHZCzSQbajLZBiOoGZBuq18oTaZB5PMdSJa98MG926xtY8bVvmQxg1gZBOUTHTmJhIvOASqNYFmUVIesivi4XV7SmUeImhwhksCG5YWtNPfMuo7IKZAzrtfpqdgJSeZCsryVtdG3G0KJcLxCY"
VERIFY_TOKEN = "rasademo"


def post_facebook_message(fbid, recevied_message):

    data = json.dumps({"message": "%s" % recevied_message, "sender": "Me"})
    p = requests.post('http://localhost:5005/webhooks/rest/webhook',
                      headers={"Content-Type": "application/json"}, data=data).json()

    print(p)

    bot_res = p[0]['text']

    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {
        'fields': 'first_name,last_name,profile_pic', 'access_token': PAGE_ACCESS_TOKEN}

    user_details = requests.get(user_details_url, user_details_params).json()

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN

    response_msg = json.dumps(
        {"recipient": {"id": fbid}, "message": {"text": bot_res}})
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)

class BotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        print(incoming_message)
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    post_facebook_message(
                        message['sender']['id'], message['message']['text'])
        return HttpResponse()


def dinhDangJson(s, fbid):
    res = {}
    res['recipient'] = {"id": fbid}
    res['message'] = {}
    for i in s.keys():
        if i == 'text':
            res['message']['text'] = s['text']
        if i == 'buttons':
            buttons = []
            for i in s['buttons']:
                buttons.append(i)

            payload = {
                "template_type": "button",
                "text": "Try the postback button!",
                "buttons": buttons
            }

            attachment = {
                "type": "template",
                "payload": payload}
            res['message']['attachment'] = attachment

    return res
