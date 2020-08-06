from functions import startupProcess

startupProcess()

from interperter import run

while True:
	text = input('KaasScript > ')

	if text == 'exit': break
	elif text.strip() == '': continue

	result, error = run('<stdin>', text)

	if error: print(error)
	elif result: print(result)
