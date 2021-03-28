import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

TOKENS = ["tokens/acc1_token.pickle","tokens/acc2_token.pickle","tokens/acc3_token.pickle","tokens/acc4_token.pickle",
"tokens/acc5_token.pickle","tokens/acc6_token.pickle","tokens/acc7_token.pickle"]

creds = None

PWD = str(os.path.dirname(os.path.abspath(__file__))).replace("/scripts","")

def login(creds):
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f'{PWD}/tokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(f'{PWD}/tokens/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

def load_cred(name):
    if os.path.exists(f'{PWD}/{name}'):
        with open(f'{PWD}/{name}', 'rb') as token:
            creds = pickle.load(token)
            return creds
    else:
        print("token not found")

def match_file_name(file_name,data_name):
    if(file_name.find("metadata")!=-1 and data_name=="adni_metadata"):
        return True
    if(file_name.find("part")!=-1 and data_name=="adni_data" and file_name.find("metadata")==-1 ):
        return True
    if(file_name.find("CAN_META")!=-1 and data_name=="cancer_metadata"):
        return True
    if(file_name.find("CAN")!=-1 and data_name=="cancer_data" and file_name.find("_META")==-1):
        return True   
    if(file_name.find("preprocessed_adni")!=-1 and data_name=="adni_preprocessed"):
        return True 
    if(file_name.find("preprocessed_cancer")!=-1 and data_name=="cancer_preprocessed"):
        return True
    return False


def get_id(creds,name):
    files=[]
    items=[]
    service = build('drive', 'v3', credentials=creds)
    page_token = None
    while True:
        response = service.files().list(fields='nextPageToken, files(id, name)',
        pageToken=page_token).execute()
        items+=response.get('files', [])
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    if items:
        for item in items:
            if(match_file_name(item['name'],name)):
                print(f"Name: {item['name']}\t Id: {item['id']}")
                files.append(item)
    else:
        print("no files found")
    return files

def get_files(name):
    print("\n GETTING FILES \n")
    files=[]
    for token in TOKENS:
        creds=load_cred(token)
        files.extend(get_id(creds,name))
    return files
    
if __name__ == '__main__':
    print(PWD)
    get_files("cancer_data")
