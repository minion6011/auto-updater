import os
import requests
import json
import base64


# - Config

github_repo_url = "https://api.github.com/repos/user_name/reposity_name" # Reposity Link
api_token = "" # Github Token
files_to_update = [ # Names of files that the autoupdater should update
	"requirements.txt",
	"main.py",
]

# - Code

def download_file(url):
	headers = {"Authorization": f"token {api_token}"}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		return response.text
	else:
		print(f"[ERROR] Request Status code: {str(response.status_code)}")
		return None

def update_file(filename, content):
	directory = os.path.dirname(filename)
	if directory and not os.path.exists(directory):
		os.makedirs(directory)
		print(f"[LOG] Folder '{directory}' created.")
	with open(filename, "w", encoding="utf-8", newline='\n') as file:
		file.write(content)
	print(f"[LOG] File '{filename}' updated")

def run_autoupdater():
	print("[LOG] Autoupdater started")
	for filename in files_to_update:
		file_url = f"{github_repo_url}/contents/{filename}"
		print(f"[LOG] Checking for updates for '{filename}'")
		file_content = download_file(file_url)
		if file_content is not None:
			file_content = json.loads(file_content)
			file_content = file_content["content"]
			file_content = base64.b64decode(file_content).decode("utf-8")
			update_file(filename, file_content)
		else:
			print(f"[ERROR] Unable to get data for '{filename}'") #If this happens, check that the API Key is valid or that the file name is correct
	print("[LOG] Autoupdater completed")

run_autoupdater()