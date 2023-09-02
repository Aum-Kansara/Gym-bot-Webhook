from dotenv import load_dotenv
import os
from flask import Flask,jsonify,request
import requests
load_dotenv()
webhook_link=os.getenv("WEBHOOK_URL")
flowise_review=os.getenv("FLOWIAW_REVIEW_URL")
flowise_complaint=os.getenv("FLOWIAW_COMPLAINT_URL")

app=Flask(__name__)


@app.route('/')
def index():
  return "Hello World"

@app.route('/getResponse')
def getResponse():
    email=request.args.get('email','')
    phone=request.args.get('phone','')
    name=request.args.get('name','')
    if email.strip()=='':
        return "Provide Valid Question"
    res=requests.get(webhook_link,params={"email":email,'phone':phone,'name':name})
    if res.text.lower()=='accepted':
        return "Server Error"
    if int(res.text):
        return jsonify({"question" : email,
                        "booking_url":res.headers['bookingurl']
            })
    return jsonify({"question" : email})

@app.route('/getComplaintSummary')
def getComplaintSummary():
    summary=request.args.get('complaint','')
    res=requests.post(flowise_complaint,json={"question":summary})
    return jsonify({"summary":res.text})

@app.route('/getReviewSummary')
def getReviewSummary():
    summary=request.args.get('review','')
    res=requests.post(flowise_review,json={"question":summary})
    return jsonify({"summary":res.text})

if __name__=="__main__":
    app.run(debug=True)