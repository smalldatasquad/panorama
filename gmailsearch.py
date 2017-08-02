from __future__ import print_function
import httplib2
import os
import base64
import email
import mailbox
import collections
import io, json

from apiclient.http import BatchHttpRequest
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import dehtml
from email_reply_parser import EmailReplyParser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_SECRET_FILE = 'client_secret_25620108186-qr3kcg5v4rbv1r1pg3lri1sb2livbvir.apps.googleusercontent.com.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def start_gmail_service():

    def get_credentials():
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials



    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service




def query_to_filename(querystring):
    return "json_from_gmailsearch__" + querystring + "__.json"

def jsonsave(data, filename):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))



def raw_message_to_obj(response):
    global service
    obj = collections.OrderedDict()

    # print(response.keys())
    # print(response['payload'].keys())
    # print(response['payload']['headers'])

    def email_from_raw(raw):
        print("111")
        msg_bytes = base64.urlsafe_b64decode(raw.encode('ASCII'))
        print("113331")
        mime_msg = email.message_from_bytes(msg_bytes)
        print("113388831")
        maildir_message = mailbox.MaildirMessage(mime_msg)
        print("11338883kkk1")
        return maildir_message

    def parse_reply_from_email(message):
        print("parserpely")
        return EmailReplyParser.parse_reply(message)


    fields = ['Subject', 'Date', 'From', 'To', 'Cc', 'Message-ID']

    print("aa")
    try:
        ## THIS IS WHERE THINGS HAPPEN
        for f in fields:
            v = [x['value'] for x in response['payload']['headers'] if x['name'] == f]
            obj[f] = ''.join(v) #if v is empty array, resolves to empty string
        obj['snippet'] = dehtml.dehtml(response['snippet'])
        print("bbb")
        try: 
            reply = parse_reply_from_email(email_from_raw(response['payload']['parts'][0]['body']['data']))
            obj['full'] = reply
            print("bbcccb")
        except:
            pass
    except Exception as error:
        print('An Error occurred: %s' % error)
    return obj


def get_all_messages(querystring):
    all_messages = []
    global service
    try:
        message_count = 0
        start = True
        while start or 'nextPageToken' in response:
            print("PING")
            if start:
                page_token = None
                start = False
            else:
                page_token = response['nextPageToken']

            response = service.users().messages().list(userId='me', pageToken=page_token, q=querystring).execute()
            if 'messages' in response:
                message_count += len(response['messages'])
                for message in response['messages']:
                    message_id = message['id']
                    message_full = service.users().messages().get(userId='me', format='full', id=message_id).execute()

                    ## THIS IS EACH OBJ
                    messageObj = raw_message_to_obj(message_full)
                    all_messages.append(messageObj) # this could hog up memory..

            print("PINK")
    except errors.HttpError as error:
        print('An HTTPError occurred: %s' % error)

    return all_messages



def get_all_threads(querystring):
    global service
    results = service.users().threads().list(userId='me', q=querystring).execute()
    threads = results.get('threads', [])
    if not threads:
        print('No threads found.')
    else:
        print('Threads:')
        for thread in threads:
            # tdata =.users().threads().get(userId='me', id=thread['id']).execute()
            # nmsgs = len(tdata['messages'])

            # if nmsgs > 2:
            print(dehtml.dehtml(thread['snippet']))
            #print(html2text.html2text(thread['snippet']))


####################3

def main():
    global service
    global myprofile

    service = start_gmail_service()

    myprofile = service.users().getProfile(userId='me').execute()
    print("There are {messagesTotal} messages for {emailAddress}".format(**myprofile))

    querystring = "from:" + myprofile['emailAddress'] + " " + "fuck"

    all_messages = get_all_messages(querystring)

    filename = query_to_filename(querystring)

    jsonsave(all_messages, filename)
#    get_all_threads(service, querystring)


if __name__ == '__main__':
    main()
