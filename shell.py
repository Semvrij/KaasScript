from src.functions import startupProcess

startupProcess()

from src.interperter import run

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
