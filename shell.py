from basic import run
from functions import startupProcess 

startupProcess()

while True:
	text = input('KaasScript > ')

	if text == 'exit':
		break

	result, error = run('<pl>', text)

	if error: print(error)
	else: print(result)
