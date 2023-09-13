import requests, os, json, sys
from dotenv import load_dotenv

#load virtual env
load_dotenv();

#endpoint
URL_add = os.environ.get('JC_URL') #url remove is the same as console.jumpcloud, however appending the unique id_ created by the application and sending a DELETE request to the api
if not URL_add:
	raise ValueError("JumpCloud env variable is not set.")
API_KEY = os.environ.get('API_KEY_jump')
if not API_KEY:
	raise ValueError("API_KEY env variable is not set.")

#header build
headers = {
	"Accept":"application/json",
	"Content-Type":"application/json",
	"x-api-key":API_KEY
}

#file pointer and file open manipulation
f = open("users.txt", "r")
ff = open("valid_users.txt", "a")
#for loop using contents of file
for line in f:
	#user data to send
	data = {
			"username":line.split('@')[0],
		"email":line
	}
	#request
	req = requests.post(URL_add, headers=headers, json=data);
	if (req.status_code == 400):
		ff.write(line)
		print(line)
	elif (req.status_code == 200):
		reqResult = json.loads(req.text);
		URL_delete = URL_add+"/"+reqResult["_id"]
		rr = requests.delete(URL_delete, headers=headers);
	else:
		f.close()
		ff.close()
		sys.exit("An error occurred")

f.close();
ff.close();
