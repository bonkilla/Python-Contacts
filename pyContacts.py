from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/contacts']

def check_repetitions( listTels,newTelef):
    checkTel=''
    if newTelef.startswith( '00' ):
        checkTel=newTelef[4:]
    elif newTelef.startswith( '+' ):
        checkTel=newTelef[3:]
    else:
        checkTel=newTelef
    if any(checkTel in unitTel for unitTel in listTels):
        #print ('Warning, possible duplicate numbers')
        return True
    else:
        return False

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
    print('List 500 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=500,
        personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])

    # Loop all connections
    for person in connections:
        names = person.get('names', [])
        telefs = person.get('phoneNumbers', [])
        if names:
            name = names[0].get('displayName')
            numtelef = len(telefs)
            telefConcat=""
            if numtelef > 1:
                list_of_telefs = []
                telefs_modified=telefs.copy()
                # Loop all phones
                for telefSingle in telefs:
                    
                    newTelef=''
                    if telefSingle.get('canonicalForm'):
                        telefConcat=telefConcat +','+telefSingle.get('canonicalForm')
                        newTelef=telefSingle.get('canonicalForm')
                    if telefSingle.get('Company Main'):
                        telefConcat=telefConcat +','+telefSingle.get('value')
                        newTelef=telefSingle.get('value')
                    # If we check the phone is already present in previous ones we delete it
                    if(check_repetitions(list_of_telefs, newTelef)):
                        print('We are going to delete number {} from contact {}'.format(newTelef, name))

                        telefs_modified.remove(telefSingle)
                        person['phoneNumbers']=telefs_modified
                        results = service.people().updateContact(
                            resourceName=person.get("resourceName"),
                            body=person,
                            updatePersonFields='phoneNumbers').execute()
                    else:
                        list_of_telefs.append(newTelef)       
                
if __name__ == '__main__':
    main()