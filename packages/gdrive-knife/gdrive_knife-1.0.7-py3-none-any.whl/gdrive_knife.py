# Copyright (c) 2023 Jakub Czajka <jakub@ekhem.eu.org>
# License: GPL-3.0 or later.

import argparse
import io
import json
import os.path
import shutil
import sys
import urllib.parse
import uuid
import zipfile

from apiclient.http import MediaFileUpload
from cryptography.fernet import Fernet
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from wsgiref.simple_server import make_server

SCOPES = ['https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file']

def file_path(parser, path):
    if not os.path.isfile(path):
        return parser.error(f'{path} does not exist!')
    return path

def fernet_key(parser, path_or_string):
    if os.path.isfile(path_or_string):
        with open(path_or_string, 'rb') as f:
            return Fernet(f.read())
    return Fernet(path_or_string)

def auth_token(parser, path_or_string):
    creds = None
    if os.path.isfile(path_or_string):
        creds = Credentials.from_authorized_user_file(path_or_string, SCOPES)
    else:
        as_json = json.loads(path_or_string)
        creds = Credentials(
            token=as_json['token'],
            refresh_token=as_json['refresh_token'],
            token_uri=as_json['token_uri'],
            client_id=as_json['client_id'],
            client_secret=as_json['client_secret'],
            scopes=as_json['scopes'],
        )
    if not creds or not creds.valid:
        print(f'Token is not valid. Use `auth` to obtain a new one.')
        sys.exit(1)
    return creds

def get_path_on_drive(file_path):
    if os.path.isabs(file_path):
        return '/tmp' + file_path
    return '/tmp/' + file_path

def get_file_id(drive, file_path):
    path_on_drive = get_path_on_drive(file_path)
    query_result = drive.files().list(q=f"name='{path_on_drive}'",
        fields='files(id)').execute()
    maybe_id = query_result.get('files', [])
    if not maybe_id:
        return None
    return maybe_id[0]['id']

# Standard Fernet encryption/decryption requires whole file in memory. This has
# memory contrains. Instead, this program splits the file into blocks and
# encrypts/decrypts them separately. See https://stackoverflow.com/a/71068357.
def encrypt_chunks_in_place(encryption_key, path):
    block = 1 << 16

    file_size = os.path.getsize(path)
    processed_bytes = 0
    percentage = 0

    tmp_path = path + str(uuid.uuid4())
    with open(path, 'rb') as input_file, open(tmp_path, 'wb') as output_file:
        while True:
            unencrypted_bytes = input_file.read(block)
            if len(unencrypted_bytes) == 0:
                break
            encrypted_bytes = encryption_key.encrypt(unencrypted_bytes)
            bytes_as_int = len(encrypted_bytes).to_bytes(4, 'big')
            output_file.write(bytes_as_int)
            output_file.write(encrypted_bytes)

            processed_bytes = processed_bytes + len(unencrypted_bytes)
            new_percentage = int(processed_bytes / file_size * 100)
            if new_percentage > percentage + 7:
               percentage = new_percentage
               print(f'Encrypt: {percentage}%')

            if len(unencrypted_bytes) < block:
                break
    os.rename(tmp_path, path)

def decrypt_chunks_in_place(encryption_key, path):
    file_size = os.path.getsize(path)
    processed_bytes = 0
    percentage = 0

    tmp_path = path + str(uuid.uuid4())
    with open(path, 'rb') as input_file, open(tmp_path, 'wb') as output_file:
        while True:
            encrypted_bytes = input_file.read(4)
            if len(encrypted_bytes) == 0:
                break
            bytes_as_int = int.from_bytes(encrypted_bytes, 'big')
            chunk = input_file.read(bytes_as_int)
            decrypted_bytes = encryption_key.decrypt(chunk)
            output_file.write(decrypted_bytes)

            processed_bytes = processed_bytes + 4 + len(chunk)
            new_percentage = int(processed_bytes / file_size * 100)
            if new_percentage > percentage + 7:
               percentage = new_percentage
               print(f'Decrypt: {percentage}%')

    os.rename(tmp_path, path)

class auth_server():

    def __init__(self, flow, redirect_url):
        self.flow = flow
        self.url = redirect_url

    def handle_one_on(self, host, port):
        print(f'Polling on {host}:{port}...')
        with make_server(host, port, self) as httpd:
            print(f'Authentication URL: {self.flow.authorization_url()[0]}')
            httpd.handle_request()

    def __call__(self, environ, start_response):
        parameters = urllib.parse.parse_qs(environ['QUERY_STRING'])
        self.flow.fetch_token(code=parameters['code'][0])

        if self.url:
            start_response('308 Permanent Redirect', [('Location', self.url)])
        else:
            start_response('200 OK', [('Content-type', 'text/html')])
        return [b'Obtainted new credentials.']

def auth(args):
    creds = None
    write_token_to_file = False
    if os.path.exists(args.token):
        print(f'{args.token} exists. Trying to authenticate with it.')
        try:
            creds = Credentials.from_authorized_user_file(args.token, SCOPES)
        except ValueError:
            os.remove(args.token)
            print(f'{args.token} is malformed. Reset permissions at '
                   'https://myaccount.google.com/permissions and retry.')
            sys.exit(1)
    if creds and creds.expired and creds.refresh_token:
        print(f'{args.token} has expired. Refreshing.')
        try:
            creds.refresh(Request())
            write_token_to_file = True
        except RefreshError:
            print(f'Could not refresh an invalid token. Obtaining a new one.')
            os.remove(args.token)
    if not creds or not creds.valid:
        print(f'{args.token} does not exist. Obtaining a new token.')
        flow = Flow.from_client_secrets_file(args.credentials, scopes=SCOPES,
          redirect_uri=args.on_token)
        # Run the server on localhost because wsgi does not use HTTPS.
        auth_server(flow, args.on_success).handle_one_on('localhost', args.port)
        creds = flow.credentials
        write_token_to_file = True
    if write_token_to_file:
        print(f'Writing new token to {args.token}.')
        with open(args.token, 'w') as token:
            token.write(creds.to_json())
    print('Authentication successful.')

def list(args):
    drive = build('drive', 'v3', credentials=args.token)

    files_on_drive = drive.files().list(q='trashed=false',
        fields='files(id, originalFilename)').execute()

    for file_on_drive in files_on_drive['files']:
        print(file_on_drive['originalFilename'])

def download(args):
    drive = build('drive', 'v3', credentials=args.token)

    maybe_id = get_file_id(drive, args.path)
    if not maybe_id:
        print(f'File {args.path} not found.')
        sys.exit(1)

    request = drive.files().get_media(fileId=maybe_id, acknowledgeAbuse=True)

    path_in_tmp = '/tmp/' + str(uuid.uuid4())
    with io.FileIO(path_in_tmp, mode='wb') as stream_input:
        downloader = MediaIoBaseDownload(stream_input, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download: {int(status.progress() * 100)}%.')

    decrypt_chunks_in_place(args.key, path_in_tmp)
    print(f'{args.path} decrypted.')

    if zipfile.is_zipfile(path_in_tmp) and not args.leave_as_archive:
        os.makedirs(args.output, exist_ok=True)
        shutil.unpack_archive(path_in_tmp, extract_dir=args.output, format='zip')
        print(f'Unarchived to {args.output}.')
    else:
        destination = args.output + '/' + os.path.basename(args.path)
        shutil.move(path_in_tmp, destination)
        print(f'Moved to {destination}.')

    if os.path.exists(path_in_tmp):
        os.remove(path_in_tmp)
        print(f'Removed {path_in_tmp}.')

def upload(args):
    drive = build('drive', 'v3', credentials=args.token)

    path = args.name if args.name else args.file
    path_in_tmp = get_path_on_drive(path)

    if os.path.isdir(args.file):
        archive = shutil.make_archive(base_name=path_in_tmp, format='zip',
            root_dir=os.path.dirname(args.file),
            base_dir=os.path.basename(args.file))
        os.rename(archive, path_in_tmp)
        print(f'Archived {args.file} in {path_in_tmp}.')
    else:
        os.makedirs(os.path.dirname(path_in_tmp), exist_ok=True)
        if args.file != path_in_tmp:
            shutil.copy(args.file, path_in_tmp)
            print(f'Copied {args.file} to {path_in_tmp}.')

    encrypt_chunks_in_place(args.key, path_in_tmp)
    print(f'Encrypted {args.file} in {path_in_tmp}.')

    body = { 'name': path_in_tmp, 'originalFilename': path }
    media = MediaFileUpload(path_in_tmp, resumable=True)

    maybe_id = get_file_id(drive, path)
    if maybe_id:
        drive.files().update(fileId=maybe_id, body=body,
            media_body=media).execute()
        print(f'Updated {path} on drive.')
    else:
        drive.files().create(body=body, media_body=media).execute()
        print(f'Created {path} on drive.')

    os.remove(path_in_tmp)
    print(f'Removed {path_in_tmp}.')

def delete(args):
    drive = build('drive', 'v3', credentials=args.token)

    maybe_id = get_file_id(drive, args.path)
    if not maybe_id:
        print(f'File {args.path} not found.')
        sys.exit(1)

    drive.files().delete(fileId=maybe_id).execute()
    print(f'Deleted {args.path} on drive.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gdrive_knife', description='Swiss '
        'army knife for working with Google Drive.')

    subparsers = parser.add_subparsers()

    auth_parser = subparsers.add_parser('auth', help='Obtain an authentication '
        'token.')
    auth_parser.add_argument('-c', '--credentials', required=True,
        type=lambda x : file_path(parser, x), help='File with credentials.')
    auth_parser.add_argument('-p', '--port', type=int, default=8080, help='Port '
        'for the authentication server.')
    auth_parser.add_argument('--on_success', help='URL to redirect to after '
        'successful authentication.')
    auth_parser.add_argument('--on_token', default='http://localhost:8080',
        help='URL to redirect to after successful authentication.')
    auth_parser.add_argument('-t', '--token', default='token.json',
        required=True, help='File with the authentication token (created if '
        'missing).')
    auth_parser.set_defaults(func=auth)

    list_parser = subparsers.add_parser('list', help='List files.')
    list_parser.add_argument('-t', '--token', required=True,
        type=lambda x : auth_token(parser, x), help='File with the '
        'authentication token.')
    list_parser.set_defaults(func=list)

    download_parser = subparsers.add_parser('download', help='Download a file.')
    download_parser.add_argument('path', help='File to download.')
    download_parser.add_argument('output', help='Where to save the file.')
    download_parser.add_argument('-k', '--key', required=True,
        type=lambda x : fernet_key(parser, x), help='File with the decryption '
        'key.')
    download_parser.add_argument('-t', '--token', required=True,
        type=lambda x : auth_token(parser, x), help='File with the '
        'authentication token.')
    download_parser.add_argument('--leave-as-archive', action='store_true',
        help='Skip unarchiving for directories.')
    download_parser.set_defaults(func=download)

    upload_parser = subparsers.add_parser('upload', help='Upload a file '
        '(override if it exists).')
    upload_parser.add_argument('file', help='File to upload.')
    upload_parser.add_argument('name', help='Name on the drive.', nargs='?')
    upload_parser.add_argument('-k', '--key', required=True,
        type=lambda x : fernet_key(parser, x), help='File with the decryption '
        'key.')
    upload_parser.add_argument('-t', '--token', required=True,
        type=lambda x : auth_token(parser, x), help='File with the '
        'authentication token.')
    upload_parser.set_defaults(func=upload)

    delete_parser = subparsers.add_parser('delete', help='Delete a file.')
    delete_parser.add_argument('path', help='File to delete.')
    delete_parser.add_argument('-t', '--token', required=True,
        type=lambda x : auth_token(parser, x), help='File with the '
        'authentication token.')
    delete_parser.set_defaults(func=delete)

    args = parser.parse_args()

    args.func(args)
