from src.constants.colors import fg_yellow, reset
from src.interperter import run

print(fg_yellow, r'''
 _  __                   ____               _         _
| |/ / __ _   __ _  ___ / ___|   ___  _ __ (_) _ __  | |_
| ' / / _` | / _` |/ __|\___ \  / __|| '__|| || '_ \ | __|
| . \| (_| || (_| |\__ \ ___) || (__ | |   | || |_) || |_
|_|\_\\__,_| \__,_||___/|____/  \___||_|   |_|| .__/  \__|
                                              |_|
''', reset)

while True:
	text = input('KaasScript > ')

	if text == 'exit': break
	elif text.strip() == '': continue

	result, error = run('<stdin>', text)

	if error: print(error)
	elif result:
		if len(result.elements) == 1:
			print(repr(result.elements[0]))
		else: print(repr(result))
