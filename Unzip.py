import zipfile
def extractall():
	with zipfile.ZipFile('code2.zip', "r") as z:
    	z.extractall(r"C:\Users\arnav\Desktop\Python\HomeStock")