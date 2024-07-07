import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/drive.file"]
SHARED_FOLDER = "0AOS8kYKJqV9AUk9PVA"

def upload_files(service):
    for f in {"ayden.py", "aymarri.py", "aynira.py", "breionna.py", "ceslee.py", 
                "eli.py", "garrett.py", "imani.py", "jairus.py", "jamiya.py", 
                "LeoJamersonAydenAzyrion.py", "maurice.py", "michya.py", 
                "motion_productions.py", "nevaeh.py", "raye.py", "samantha.py"}:
    
        upload_file = "roster/{fname}".format(fname=f)

        file_metadata = {"name": f, "driveId": SHARED_FOLDER, "mimeType": "text/x-python", 
                        "parents": [SHARED_FOLDER]}
        media = MediaFileUpload(
            upload_file, mimetype="text/x-python", resumable=True
        )
        # pylint: disable=maybe-no-member
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id",
                supportsAllDrives=True)
            .execute()
        )

def read_files(service):
    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)", 
            includeItemsFromAllDrives=True, supportsAllDrives=True,
            q=f"parents in '{SHARED_FOLDER}'")
        .execute()
    )
    items = results.get("files", [])

    if not items:
      print("No files found.")
      return
    print("Files:")
    for item in items:
      print(f"{item['name']} ({item['id']})")

def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)

    upload_files(service)
    
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()