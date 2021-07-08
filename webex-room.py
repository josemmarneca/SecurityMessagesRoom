import json
import sys
import requests

#MISSION: FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN = "OGY1MjNmZjYtNmUyYS00ZTlhLWFlM2MtNTFiZmRkMTBhNjJmMjRmNzUyNWMtMTMw_PF84_d271076d-2eb0-42d9-a748-a369ce92b135" #Replace None with your access token between quotes.
BOT_ID = "Y2lzY29zcGFyazovL3VzL1BFT1BMRS81MDI5Mjg4YS00OWEzLTQ3MTctYjUyMy0yYWUzYzQyNjg1M2I"


#sets the header to be used for authentication and data format to be sent.
def getWebexTeamsHeader():
    accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
    webex_teams_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
    return (webex_teams_header)


#check if the room already exists. If so return the space id
def findRoom(headers, room_name):
    roomId=None
    uri = 'https://api.ciscospark.com/v1/rooms'
    resp = requests.get(uri, headers=headers)
    resp = resp.json()
    print('resp', resp)
    for room in resp["items"]:
        if room["title"] == room_name:
            print()
            print("findRoom JSON: ", room)

            roomId=room['id']
            break
    return(roomId)

# checks if the room already exists and if true returns that room ID. If not creates a new room and returns the space id.
def createRoom(headers, room_name):
    roomId=findRoom(headers, room_name)
    if roomId==None:
        roomInfo = {"title":room_name}
        uri = 'https://api.ciscospark.com/v1/rooms'
        resp = requests.post(uri, json=roomInfo, headers=headers)
        var = resp.json()
        print()
        print("createRoom JSON: ", var)
        print("createRoom JSON: ", var['id'])

        roomId=var['id']
    return(roomId)

# adds a new member to the space. Member e-mail is test@test.com
def addDxnetBot(headers, roomId):
    member = {"roomId":roomId,"personEmail": "dxnet-labs@webex.bot", "isModerator": False}
    uri = 'https://api.ciscospark.com/v1/memberships'
    resp = requests.post(uri, json=member, headers=headers)
    resp_json = resp.json()
    print("addMembers JSON: ", resp_json)
    return resp_json

# posts a message to the space
def sendMsgToPerson(headers, personId, message):
    message = {"toPersonId":personId,"text":message}
    uri = 'https://api.ciscospark.com/v1/messages'
    resp = requests.post(uri, json=message, headers=headers)
    print()
    print("postMsg JSON: ", resp.json())

# posts a message to the space
def sendMsgToRoom(headers, roomId, message):
        message = {"roomId": roomId, "text": message}
        uri = 'https://api.ciscospark.com/v1/messages'
        resp = requests.post(uri, json=message, headers=headers)
        resp_json = resp.json()
        print()
        print("sendMsgToRoom JSON: ", resp_json)
        return resp_json

def getMyOwnDetails(headers):
    uri = 'https://api.ciscospark.com/v1/people/me'
    resp = requests.get(uri, headers=headers)
    resp_json =  resp.json()
    print("getMyOwnDetails JSON: ", resp_json)
    return resp_json

def getPersonDetails(headers, personId):
    uri = 'https://api.ciscospark.com/v1/people/' + personId
    resp = requests.get(uri, headers=headers)
    resp_json =  resp.json()
    print("getMyOwnDetails JSON: ", resp_json)
    return resp_json

def getDirectMessages(headers, personId):
    uri = 'https://api.ciscospark.com/v1/messages/direct'
    queryParams = {'personId': personId}

    resp = requests.get(uri, headers=headers, params=queryParams)
    resp_json = resp.json()
    print("getMyOwnDetails JSON: ", resp_json)
    return resp_json

# MISSION: WRITE CODE TO RETRIEVE AND DISPLAY DETAILS ABOUT THE ROOM.
def getRoomInfo(headers, roomId):
    print("In function getRoomInfo")
    #MISSION: Replace None in the URI variable with the Webex Teams REST API call
    uri = None
    if uri == None:
        sys.exit("Please add the URI call to get room details. See the Webex Teams API Ref Guide")
    resp = requests.get(uri, headers=headers)
    print("Room Info: ",resp.text)
    resp = resp.json()

    print(resp)

    # MISSION: WRITE CODE TO RETRIEVE AND DISPLAY DETAILS ABOUT THE ROOM.

def postUserInMainRoomEvent(email):
    message = {"email": email}
    uri = 'https://dxnet-webex-api.herokuapp.com/postUserInRoom'
    resp = requests.post(uri, json=message)
    resp_json = resp.json()
    print()
    print("sendMsgToRoom JSON: ", resp_json)
    return resp_json

def createWebhook(headers, name, targetUrl, resource, event, filter):
    message = {"name":name,"targetUrl": targetUrl, "resource":resource, "event":event, "filer": filter}
    uri = 'https://api.ciscospark.com/v1/webhooks'
    resp = requests.post(uri, json=message, headers=headers)
    print()
    resp_json = resp.json()
    print("postMsg JSON: ", resp_json)
    return resp_json

if __name__ == '__main__':
    # TODO: Pre requirements and set the ACCESS_TOKEN see(https://developer.webex.com/docs/api/getting-started) in right panel "Accounts and Authentication" see Your Personal Access Token
    if ACCESS_TOKEN==None :
        sys.exit("Please check that variables ACCESS_TOKEN, have values assigned.")

    # TODO: Create room
    #createRoom(getWebexTeamsHeader(), "Dxnet_Devnet2021")


    roomId = "OGY1MjNmZjYtNmUyYS00ZTlhLWFlM2MtNTFiZmRkMTBhNjJmMjRmNzUyNWMtMTMw_PF84_d271076d-2eb0-42d9-a748-a369ce92b135"


    # TODO: Create webbhook
    # ngrokServer= "https://1c44d8254e24.ngrok.io"
    # webhookServer= ngrokServer + "/webhookMsgInRoom"
    # filter = "roomId=" + roomId
    # createWebhook(getWebexTeamsHeader(), "webhookMsgInRoom", webhookServer, "messages", "created", filter)

    # TODO: send msg to room
    #sendMsgToRoom(getWebexTeamsHeader(), roomId, "https://ola.com")
