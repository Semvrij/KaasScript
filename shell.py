import basic

runShell = True

while runShell:
	text = input('KaasScript > ')
	result, error = basic.run('<pl>', text)

	if text == 'exit': 
		runShell = False
		break

	if error: print(error)
	else: print(result)
