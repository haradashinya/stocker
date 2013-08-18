from flask import request,url_for,redirect
import requests
app_id='526770004048893'
app_secret="2808bb138b8ccd707fdea5b892627a8a"




def connect():
    url = 'http://www.facebook.com/dialog/oauth/?client_id=%s&redirect_uri=%s&scope=email&state=RANDOM_NUMBER_PREVENT_CSRC&response_type=code' % (app_id,'http://localhost:5000/posted')
    return redirect(url)





