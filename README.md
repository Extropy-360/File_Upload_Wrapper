# File_Upload_Wrapper

A simple wrapper for uploading files to the client portal.

## Installation

You can install the package directly from the GitHub repository:

```sh
pip install git+https://github.com/Extropy-360/File_Upload_Wrapper.git
```

##Example usage

```sh
# Import the FileExchange class
from file_upload_wrapper import FileExchange

# Create an instance of the FileExchange class
upload_client = FileExchange('https://files.file_exchangesite.com', 'your_username', 'your_password')

# Define the files to upload and the upload path on the exchange where you want your files to end up.
files_to_upload = ['/path/to/file.txt', 'relative_path.csv']
upload_path = 'path/on/fileexchange'

# Upload the files
status = upload_client.upload(file_paths=files_to_upload, upload_to_path=upload_path)

# Print the status
print(status)
```
