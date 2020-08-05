from json import load
from colors import reset, fg_yellow, fg_red

def startupProcess():
	print(fg_yellow, '''
	 _  __                   ____               _         _
	| |/ / __ _   __ _  ___ / ___|   ___  _ __ (_) _ __  | |_
	| ' / / _` | / _` |/ __|\\___ \\  / __|| '__|| || '_ \\ | __|
	| . \\| (_| || (_| |\\__ \\ ___) || (__ | |   | || |_) || |_
	|_|\\_\\\\__,_| \\__,_||___/|____/  \\___||_|   |_|| .__/  \\__|
	                                              |_|
	''', reset)

def getLangSettings():
	settings = open('settings.json')
	data = load(settings)
	settings.close()
	lang = data["language"]
	langList = ['en', 'nl', 'de']

	if lang not in langList: 
		print(fg_red, f"Warning: The specified language ('{lang}') is not supported. Right now, we only support {listToString(langList)}. The default language is English.", reset)
		lang = 'en'

	return lang

def listToString(li):
	newList = ', '.join(li[:-1])
	newList += f' and {li[-1]}'

	return newList

def errorString(text, pos_start, pos_end):
	result = ''

	# Calculate indices
	idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
	idx_end = text.find('\n', idx_start + 1)
	if idx_end < 0: idx_end = len(text)

	# Generate each line
	line_count = pos_end.ln - pos_start.ln + 1
	for i in range(line_count):
		# Calculate line columns
		line = text[idx_start:idx_end]
		col_start = pos_start.col if i == 0 else 0
		col_end = pos_end.col if i == line_count - 1 else len(line) - 1

		# Append to result
		result += line + '\n'
		result += ' ' * col_start + '^' * (col_end - col_start)

		# Re-calculate indices
		idx_start = idx_end
		idx_end = text.find('\n', idx_start + 1)
		if idx_end < 0: idx_end = len(text)

	return result.replace('\t', '')
