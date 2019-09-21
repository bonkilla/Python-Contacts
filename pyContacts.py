from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def check_repetitions( listTels):
    for telefSingle in listTels:
        #Check item
        checkTel=''
        if telefSingle.startswith( '00' ):
            checkTel=telefSingle[4:]
        elif telefSingle.startswith( '+' ):
            checkTel=telefSingle[3:]
        else:
            checkTel=telefSingle
        print ('En el metodo: {} y el formateado {}'.format(telefSingle, checkTel))

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Call the People API
    print('List 10 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=500,
        personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        telefs = person.get('phoneNumbers', [])
        if names:
            name = names[0].get('displayName')
            numtelef = len(telefs)
            telefConcat=""
            #print(name)
            if numtelef > 1:
                list_of_telefs = []
                for telefSingle in telefs:
                    if telefSingle.get('canonicalForm'):
                        telefConcat=telefConcat +','+telefSingle.get('canonicalForm')
                        list_of_telefs.append(telefSingle.get('canonicalForm'))
                    if telefSingle.get('Company Main'):
                        telefConcat=telefConcat +','+telefSingle.get('value')
                        list_of_telefs.append(telefSingle.get('value'))       
                check_repetitions(list_of_telefs)
                print ('Contacto: {} con {} telefono que son: {}'.format(name,numtelef, telefConcat))

if __name__ == '__main__':
    main()