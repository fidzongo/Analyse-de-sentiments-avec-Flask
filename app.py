import pandas as pd
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from werkzeug.exceptions import NotFound, BadRequest
from flask import Flask, jsonify, request, make_response
from pydantic import BaseModel
from flask_pydantic import validate
from textblob import TextBlob

app = Flask(__name__)

class User(BaseModel):
    username: str
    password: int

class Sentiment(BaseModel):
    sentence: str

credentials = pd.read_csv("credentials.csv", sep=',', header=0)
credentials.drop_duplicates()

nltk.download('vader_lexicon')
sent = SentimentIntensityAnalyzer()

# A verifier si important
#def handler_error404(err):
#  return "You have encountered an error of 404",404
#app.register_error_handler(404,handler_error404)

def auth(username, password):
    '''
    user_info = credentials[['username', 'password']][credentials['username'] == username]
    try:
        user_password = user_info.password.values[0]
        if user_password == password:
            return True
        return False
    except IndexError:
        #return "L'utilisateur {} n'existe pas".format(username)
        return "IndexError"
    #except:
        #return "Something is wrong",400
    '''
    if username in credentials['username'].tolist():
        checked_password=credentials[credentials['username']==username]['password'].values[0]
        #print(test)
        if checked_password == password: 
            #print("Password ok")
            return True
        else:
            return False
    else:
        return "UserNotExists"

def user_permissions(username, password):
    user_info = credentials[['v1', 'v2']][(credentials['username'] == username) & (credentials['password'] == password)]
    return "{},{}".format(user_info.v1.values[0],user_info.v2.values[0])

@app.route("/status")
def status():
    return {"status": 1}

@app.route("/welcome")
@validate()
def welcome(query:User):
    is_valide = auth(username=query.username, password=query.password)
    if is_valide == True:
        return "Bonjour {} !".format(query.username)
    elif is_valide == False:
        return "Le mot de passe est incorrect",400
    #elif is_valide == "IndexError":
    elif is_valide == "UserNotExists":
        return "L'utilisateur {} n'existe pas".format(query.username),400
    else:
        return "Something is wrong",400
    
@app.route("/permissions",methods=["POST"])
@validate()
def permissions(body:User):
    try:
        is_valide = auth(username=body.username, password=body.password)
        if is_valide == True:
            permissions = user_permissions(username=body.username, password=body.password)
            permissions_v1 = permissions.split(",")[0]
            permissions_v2 = permissions.split(",")[1]
            #return permissions, 200, {"username": permissions}
            return permissions, 200, {"username": "{v1="+permissions_v1+" ,v2="+permissions_v2+"}"}
        elif is_valide == False:
            return "Le mot de passe est incorrect",400
        #elif is_valide == "IndexError":
        elif is_valide == "UserNotExists":
            return "L'utilisateur {} n'existe pas".format(body.username),400
        else:
            return "Something is wrong",400
            #return BadRequest("Something is wrong")
    except:
        return "Something is wrong",400
        #return BadRequest("Something is wrong")

@app.route("/v1/sentiment",methods=["POST"])
@validate()
def v1_sentiment(body:Sentiment):
    try:
        header_username = request.headers.get("Authorization").split("=")[0]
        try:
            header_password = int(request.headers.get("Authorization").split("=")[1])
        except:
            return "Veuillez verifier le format du mot de passe: type integer",400
    except:
        return "Le header Authorization: username=password est requis",400

    try:
        is_valide = auth(username=header_username, password=header_password)
        if is_valide == True:
            permissions = user_permissions(username=header_username, password=header_password)
            permissions_v1 = permissions.split(",")[0]
            if permissions_v1 == "1":
                polarity = TextBlob(body.sentence).sentiment.polarity
                return {"score":polarity}
            else:
                return "Vous n'avez pas les autorisation pour cette version d'API",400
        elif is_valide == False:
            return "Le mot de passe est incorrect",400
        #elif is_valide == "IndexError":
        elif is_valide == "UserNotExists":
            return "L'utilisateur {} n'existe pas".format(header_username),400
        else:
            return "Something is wrong",400
            #return BadRequest("Something is wrong")
    except:
        return "L'utilisateur {} n'existe pas".format(header_username),400
        #return BadRequest("Something is wrong")


@app.route("/v2/sentiment",methods=["POST"])
@validate()
def v2_sentiment(body:Sentiment):
    try:
        header_username = request.headers.get("Authorization").split("=")[0]
        try:
            header_password = int(request.headers.get("Authorization").split("=")[1])
        except:
            return "Veuillez verifier le format du mot de passe: type integer",400
    except:
        return "Le header Authorization: username=password est requis",400

    try:
        is_valide = auth(username=header_username, password=header_password)
        if is_valide == True:
            permissions = user_permissions(username=header_username, password=header_password)
            permissions_v2 = permissions.split(",")[1]
            if permissions_v2 == "1":
                compound = round(sent.polarity_scores(body.sentence)['compound'], 2)
                return {"score":compound}
            else:
                return "Vous n'avez pas les autorisation pour cette version d'API",400
        elif is_valide == False:
            return "Le mot de passe est incorrect",400
        #elif is_valide == "IndexError":
        elif is_valide == "UserNotExists":
            return "L'utilisateur {} n'existe pas".format(header_username),400
        else:
            return "Something is wrong",400
            #return BadRequest("Something is wrong")
    except:
        return "L'utilisateur {} n'existe pas".format(header_username),400
        #return BadRequest("Something is wrong") 

@app.errorhandler(NotFound)
def handler_error404(err):
  return "L'url que vous essayez d'atteindre n'existe pas",404
