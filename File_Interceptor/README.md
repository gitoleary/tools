# File Interceptor

* Edting Requests/Responses  
* Replacing Download Requests
* Inject Code/Program

When user requests to download file, replace that file with another file
This is done by changing the response from a 200 OK HTTP code to a 301 Moved Permanently code which would redirect the download to the unwanted file    