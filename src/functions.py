from json import load

from src.constants.colors import fg_red, reset


def printWarning(message):
	print(fg_red,message,reset)

def getJsonSettings():
	settings = open('settings.json')
	data = load(settings)
	settings.close()

	return data

def getLangSettings():
	data = getJsonSettings()
	lang = data["language"]
	langList = ['en', 'nl', 'de']

	if lang not in langList: 
		printWarning(f"Warning: The specified language ('{lang}') is not supported. Right now, we only support {listToString(langList)}. The default language is English.")
		lang = 'en'

	return lang

def getWhileLoopLimit():
	data = getJsonSettings()
	limit = data["whileLoopLimit"]

	if isinstance(limit, int): return limit

	printWarning("The value of whileLoopLimit must be a integer.")

def listToString(li):
	newList = ', '.join(li[:-1])
	newList += f' and {li[-1]}'

	return newList
