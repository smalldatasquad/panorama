from __future__ import print_function
import httplib2
import os
import base64
import email
import mailbox
import collections
import io, json
import csv
import glob

from apiclient.http import BatchHttpRequest
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import dehtml

from email_reply_parser import EmailReplyParser

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
APPLICATION_NAME = 'Gmail API Panorama'

def autodetect_client_secret_filename():
    try:
        res = glob.glob("client_secret*.json")
        return res[0]
    except:
        return None

def start_gmail_service(CLIENT_SECRET_FILE):

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


def get_myprofile(service):
    myprofile = service.users().getProfile(userId='me').execute()
    return myprofile


def sanitize(filename):
    import string
    valid_chars = frozenset("-_.() %s%s" % (string.ascii_letters, string.digits))
    newfilename = ''.join(c for c in filename if c in valid_chars)
    newfilename = newfilename.replace(" ", "-")
    return newfilename

def csvsave(filename, data):
    if(len(data) > 0):
        with open(sanitize(filename), 'w') as fout:
            writer = csv.DictWriter(fout, fieldnames=data[0].keys(), delimiter=",")    
            writer.writeheader()
            for row in data:
                writer.writerow({k:v for k,v in row.items() })


def jsonsave(filename, data):
    if(len(data) > 0):
        with io.open(sanitize(filename), 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))

def parse_reply_from_email(message):
    # not working right now
    return EmailReplyParser.parse_reply(message)

def email_from_raw(raw):
    msg_bytes = base64.urlsafe_b64decode(raw.encode('ASCII'))
    mime_msg = email.message_from_bytes(msg_bytes)
    maildir_message = str(mailbox.MaildirMessage(mime_msg))
    return maildir_message

def parse_multipart_message(response):
    parts = []
    if 'parts' in response['payload']:
        for p in response['payload']['parts']:
            parts.append(p['body']['data'])
    else:
        parts.append(response['payload']['body']['data'])
    message = ""
    for p in parts:
        message += email_from_raw(p)
    return parse_reply_from_email(message)

def raw_message_to_obj(response):
    global service
    obj = collections.OrderedDict()

    # print(response.keys())
    # print(response['payload'].keys())
    # print(response['payload']['headers'])



    fields = ['Subject', 'Date', 'From', 'To', 'Cc', 'Message-ID']

    try:
        ## THIS IS WHERE THINGS HAPPEN
        for f in fields[:1]:
            v = [x['value'] for x in response['payload']['headers'] if x['name'] == f]
            obj[f] = ''.join(v) #if v is empty array, resolves to empty string
        obj['snippet'] = dehtml.dehtml(response['snippet'])
        # we do this because obj is an ordered dict and we want subject, then snippet
        for f in fields[1:]:
            v = [x['value'] for x in response['payload']['headers'] if x['name'] == f]
            obj[f] = ''.join(v) #if v is empty array, resolves to empty string


        message = parse_multipart_message(response) #UNCOMMENT THIS IF NECESSARY
        obj['message'] = message

    except Exception as error:
        print('An Error occurred: %s' % error)
    return obj




def get_all_messages(service, querystring):
    all_messages = []
    try:
        message_count = 0
        start = True
        while start or 'nextPageToken' in response:
            if start:
                page_token = None
                start = False
            else:
                page_token = response['nextPageToken']

            response = service.users().messages().list(userId='me', pageToken=page_token, q=querystring).execute()
            if 'messages' in response:
                print ("  == Loading ", message_count, "messages")
                message_count += len(response['messages'])

                for message in response['messages']:
                    message_id = message['id']
                    message_full = service.users().messages().get(userId='me', format='full', id=message_id).execute()

                    ## THIS IS EACH OBJ
                    messageObj = raw_message_to_obj(message_full)
                    print ("   = Loading message with SUBJECT: ", messageObj['Subject'], " TO: ", messageObj['To'])
                    all_messages.append(messageObj) # this could hog up memory..

    except errors.HttpError as error:
        print('An HTTPError occurred: %s' % error)

    return all_messages


def get_all_threads(service, querystring):
    all_threads = []
    try:
        thread_count = 0
        start = True
        while start or 'nextPageToken' in response:
            if start:
                page_token = None
                start = False
            else:
                page_token = response['nextPageToken']

            response = service.users().threads().list(userId='me', pageToken=page_token, q=querystring).execute()
            if 'threads' in response:
                thread_count += len(response['threads'])
                print ("  == Loading ", thread_count, "threads")
                for thread in response['threads']:
                    thread['snippet'] = dehtml.dehtml(thread['snippet'])
                    print(thread)
                    all_threads.append(thread)
    except errors.HttpError as error:
            print('An HTTPError occurred: %s' % error)
    return all_threads

            
def get_message_from_id(service, id):
    message_full = service.users().messages().get(userId='me', format='full', id=id).execute()
    ## THIS IS EACH OBJ
    messageObj = raw_message_to_obj(message_full)
    return messageObj



def threads_to_messages(service, all_threads):
    all_messages = []
    for thread in all_threads:
        try:
            messageObj = get_message_from_id(service, thread['id'])
            try: 
                print ("   = Converting Thread to Message: with SUBJECT: ", messageObj['Subject'], " TO: ", messageObj['To'])
                all_messages.append(messageObj) # this could hog up memory..
            except Exception as error:
                print("Some small error occurred, don't worry about it: %s" % error)
        except errors.HttpError as error:
            print('An HTTPError occurred: %s' % error)

    return all_messages


