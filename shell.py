from functions import startupProcess

startupProcess()

from basic import run


while True:
	text = input('KaasScript > ')

	if text == 'exit':
		break

	result, error = run('<pl>', text)

	if error: print(error)
	elif result: print(result)
