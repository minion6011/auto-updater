import os
import os.path
import requests
import json
import base64

# - Config

with open("updater_config.json") as f:
	try:
		config = json.load(f)
	except json.decoder.JSONDecodeError as e:
		print("[ERROR] Error in updater_config.json")

api_key = config["github_api_token"]
files_to_update = config["files_to_update"]
url = config["github_reposity_url"]

bin_ext = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.ico', ".ttf")

# - Code

def download_file(url):
	headers = {"Authorization": f"token {api_key}"}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		return response.text
	else:
		print(f"[ERROR] Request Status code: {str(response.status_code)}")
		return None

def check_file(filename, new_content):
	if os.path.isfile(filename):
		if filename.endswith(bin_ext):
			with open(filename, "rb") as file:
				old_content = file.read()
			if old_content == new_content:
				return True
			else:
				return False
		else:
			with open(filename, "r", encoding="utf-8", newline="\n") as file:
				old_content = file.read()
			if old_content == new_content:
				return True
			else:
				return False

def update_file(filename, content):
	directory = os.path.dirname(filename)
	if directory and not os.path.exists(directory):
		os.makedirs(directory)
		print(f"[LOG] Folder '{directory}' created.")
	if filename.endswith(bin_ext):
		with open(filename, "wb") as file:
			file.write(content)
	else:
		content = content.decode("utf-8")
		with open(filename, "w", encoding="utf-8", newline='\n') as file:
			file.write(content)
	print(f"[LOG] File '{filename}' updated")

def run_autoupdater():
	print("[LOG] Autoupdater started")
	for filename in files_to_update:
		file_url = f"{url}/contents/{filename}"
		print(f"[LOG] Checking for updates for '{filename}'")
		file_content = download_file(file_url)
		if file_content is not None:
			if check_file(filename, file_content) == True:
				print(f"[LOG] '{filename}' it's already up to date")
			else:
				file_content = json.loads(file_content)
				file_content = file_content["content"]
				file_content = base64.b64decode(file_content)
				update_file(filename, file_content)
		else:
			print(f"[ERROR] Unable to get data for '{filename}'") #If this happens, check that the API Key is valid or that the file name is correct
	print("[LOG] Autoupdater completed")

run_autoupdater()
