import requests
from typing import List, Dict, Optional
import logging
import os

class FileExchange:
    '''
        This class is used to interact with the client file exchange. User will be logged in on class initiallization.

        Attributes:
            base_url (str): The base url of the client file file_exchange.
            user_name (str): The user name of the account.
            password (str): The password of the account.
            log_level (str, optional): The logging level ('debug' or 'info'). Defaults to 'info'.
            user_agent (str,optional): The user agent of the client if needing to change it. Defaults to 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/

        Methods:
            upload(file_paths, upload_to_path): Uploads files to a specified path on the cloud system.

        Example:
            >>> upload_client = FileExchange('https://files.file_exchangesite.com', 'your_username', 'your_password')
            >>> upload_client.upload(['/path/to/file.txt', 'relative_path.csv'], 'path/on/fileexchange')
    '''
    def __init__(self,base_url: str, user_name: str, password: str, log_level: str = 'info', user_agent: Optional[str] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG if log_level == 'debug' else logging.INFO,
            format='%(asctime)s - file_exchange - %(levelname)s - %(message)s',
            errors='ignore',
        )
        self.session = requests.Session()
        self.user_name = user_name
        self.password = password
        self.base_url = base_url
        self.user_agent = user_agent
        self.files = []
        self._login()

    def _login(self):
        '''
                An internal method to authenticate the user with the file exchange.
                This method is automatically called during initialization.
        '''
        self.logger.debug(f'Atempting to login to {self.base_url} as user: {self.user_name}')
        url = f'{self.base_url}/core/loginguest?userid={self.user_name}&password={self.password}&passwordType=text&tfa=1'
        payload = {}
        headers = {
          'Accept': 'application/json',
          'Accept-Language': 'en-US,en;q=0.9',
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': self.user_agent,
          'X-Requested-With': 'XMLHttpRequest',
          'X-XSRF-TOKEN': 'NONE',
        }
        try:
            response = self.session.request('POST', url, headers=headers, data=payload)
            self.logger.debug(response)
            self.logger.debug(f'Response: {str(response.text)}')
            response.raise_for_status()
            self.logger.info('Login successful')
        except:
            raise Exception('Login failed')

    def upload(self, file_paths: List[str], upload_to_path: 'str'):
        '''
            Uploads files to a specified path on the client file exchange.

            Args:
                file_paths (list of str): A list of local file paths to upload.
                upload_to_path (str): The destination path on the client file exchange, you can get this by navigating to the folder on the file_exchange and copying the path from the side bar.

            Returns:
                list of dict: A list of dictionaries containing the status of each file upload.

            Example:
                >>> upload_path = '/SHARED/folder/second_folder'
                >>> files_to_upload = ['/path/to/file.txt','test.csv', 'file_other.json']
                >>> base_url = 'https://files.fake_file_exchange.com'
                >>> upload_client = FileExchange(base_url, 'your_username', 'your_password')
                >>> status = upload_client.upload(file_paths=files_to_upload, upload_to_path=upload_path)

                returns: [{'file_path': '/path/to/file.txt', 'file_name': 'file.txt', 'status': 'success'},{'file_path': '/path/to/relative_path.csv', 'file_name': 'relative_path.csv', 'status': 'success'},{'file_path': '/path/to/not_a_file.csv', 'file_name': 'not_a_file.csv', 'status': 'failed'}]
        '''
        self.logger.debug(f'Files to upload: {file_paths}')
        self.files = [{'file_path': os.path.abspath(file_path),
                    'file_name': file_path.split('/')[-1],
                    'status': 'incomplete'} for file_path in file_paths]
        headers = {
            'Accept': 'application/json',
        }
        for file_object in self.files:
            try:
                url = f'''{self.base_url}/core/upload?appname=explorer&path={upload_to_path}&uploadpath=&offset=0&filename={file_object['file_name']}&complete=1'''
                file_to_upload={'file': (open(file_object['file_path'],'rb'))}
                self.logger.debug(f'''Uploading file: {file_object['file_path']}''')
                response = self.session.post(url=url, headers=headers, files=file_to_upload, cookies=self.session.cookies)
                self.logger.debug(response)
                self.logger.debug(f'Response: {str(response.text)}')
                response.raise_for_status()
                self.logger.info(f'''File: {file_object['file_name']} uploaded successfully''')
                file_object['status'] = 'success'
            except Exception as e:
                self.logger.error(f'''Error uploading file: {file_object['file_name']}''')
                self.logger.error(e)
                file_object['status'] = 'failed'
        return self.files
