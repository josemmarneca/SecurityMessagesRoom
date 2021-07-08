from flask import Flask, request, jsonify
import json
import sys
import requests
app = Flask(__name__)

ACCESS_TOKEN_DXNET_IO= "" #Replace None with your access token between quotes.
MAIN_ROOM_ID=""

def getWebexTeamsHeader():
    accessToken_hdr = 'Bearer ' + ACCESS_TOKEN_DXNET_IO
    webex_teams_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
    return (webex_teams_header)

#check if the room already exists. If so return the space id
def getRoomId(headers, room_name):
    roomId=None
    uri = 'https://api.ciscospark.com/v1/rooms'
    resp = requests.get(uri, headers=headers)
    resp = resp.json()
    for room in resp["items"]:
        if room["title"] == room_name:
            print()
            print("findRoom JSON: ", room)
            print("MISSION: findRoom: REPLACE None WITH CODE THAT PARSES JSON TO ASSIGN ROOM ID VALUE TO VARIABLE roomId")
            roomId=room['id']
            break
    return(roomId)

def sendMsgToRoom(headers, roomId, message):
    message = {"roomId": roomId, "text": message}
    uri = 'https://api.ciscospark.com/v1/messages'
    resp = requests.post(uri, json=message, headers=headers)
    resp_json = resp.json()
    print()
    print("sendMsgToRoom JSON: ", resp_json)
    return resp_json

#check if the room already exists. If so return the space id
def getRoom(headers, room_name):
    roomReturn=None
    uri = 'https://api.ciscospark.com/v1/rooms'
    resp = requests.get(uri, headers=headers)
    resp = resp.json()
    for room in resp["items"]:
        if room["title"] == room_name:
            print()
            print("findRoom JSON: ", room)
            print("MISSION: findRoom: REPLACE None WITH CODE THAT PARSES JSON TO ASSIGN ROOM ID VALUE TO VARIABLE roomId")
            roomReturn = room
            break
    return(roomReturn)

def getMessage(headers, messageId):
    uri = 'https://api.ciscospark.com/v1/messages/' + messageId
    resp = requests.get(uri, headers=headers)
    resp = resp.json()
    print('message:', resp)
    return(resp)

# adds a new member to the space. Member e-mail is test@test.com
def addMembers(headers, roomId, email):
    member = {"roomId":roomId,"personEmail": email, "isModerator": False}
    uri = 'https://api.ciscospark.com/v1/memberships'
    resp = requests.post(uri, json=member, headers=headers)
    responseJson = resp.json()
    print("addMembers JSON: ", responseJson)
    return responseJson

def createWebhook(headers, name, targetUrl, resource, event, filter):
    message = {"name":name,"targetUrl": targetUrl, "resource":resource, "event":event, "filer": filter}
    uri = 'https://api.ciscospark.com/v1/webhooks'
    resp = requests.post(uri, json=message, headers=headers)
    print()
    resp_json = resp.json()
    print("postMsg JSON: ", resp_json)
    return resp_json

@app.route('/getRoomId/', methods=['GET'])
def appGetRoomId():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["ROOM_ID"] = getRoomId(getWebexTeamsHeader(), name)

    # Return the response in json format
    return jsonify(response)

@app.route('/getRoom/', methods=['GET'])
def appGetRoom():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["ROOM"] = getRoom(getWebexTeamsHeader(), name)

    # Return the response in json format
    return jsonify(response)

@app.route('/createWebhookToMessagesInRoom', methods=['POST'])
def createWebhookToRoom():
    json_body = request.json
    if json_body and json_body['name'] and json_body['roomId']:
        roomId = json_body['roomId']
        filter = "roomId="+roomId

        webhookUrl = request.url_root + 'webhookMsgInRoom'
        print('webhookUrl', webhookUrl)
        name = json_body['name']
        return createWebhook(getWebexTeamsHeader(), name, webhookUrl, "messages", "created", filter)
    else:
        return jsonify({
            "ERROR": "no name found, please name to webhook."
        })

@app.route('/postUserInRoom/', methods=['POST'])
def post_something():

    json_body = request.json
    print('content json:', json_body)
    print('email:', json_body['email'])


    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if json_body and json_body['email']:
        email = json_body['email']

        response = addMembers(getWebexTeamsHeader(), MAIN_ROOM_ID, email)
        newLine = "\n"
        return jsonify({
            "MESSAGE": f"Welcome {email} to our awesome platform!! {newLine}"
                       f" Provider by DXNet.io ....{newLine}{newLine}"
                       f"Check your webex account https://web.webex.com/dashboard and enjoy our sharing room ",
            # Add this option to distinct the POST request,
            #"WEBEX_MSG": response['message'],
            "ROOM_ID": MAIN_ROOM_ID
        })
    else:
        return jsonify({
            "ERROR": "no email found, please send a email."
        })


@app.route('/webhookMsgInRoom', methods=['POST'])
def postWebhook():
    print('post webhookMsgInRoom')
    json_body = request.json

    print('post body:' , json_body)

    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if json_body and json_body['data']:
        data = json_body['data']
        messageID = data['id']
        print('message id: ', messageID)
        message = getMessage(getWebexTeamsHeader(), messageID)
        messageText = message['text']
        print('messageText',messageText)
        if data['personId'] in messageText:
            winnerMsg = 'CONGRATULATION ' + data['personEmail'] + ", You are a winner"
            sendMsgToRoom(getWebexTeamsHeader(), data['roomId'], winnerMsg)
            return jsonify({
                "SUCCESS": "Find a winner"
            })
        else:
            return jsonify({
                "SUCCESS": "Analise message"
            })


    else:
        return jsonify({
            "ERROR": "no data found"
        })

@app.route("/")
def home_view():
    return '<iframe id="myiframe" width="100%" height="100%" src="https://www.dxnet.io"></iframe>'

if __name__ == "__main__":
    app.run()