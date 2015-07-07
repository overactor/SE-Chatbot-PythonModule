from Module import Command
import requests
import json
import time

sphere_url = "http://api.compilers.sphere-engine.com/api/3/"
token = "b14f4e91ae714f83ba944de1b117feee"
python_id = 4

def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
    global sphere_url
    global token
    global python_id
    response = requests.get(sphere_url + 'languages', params={'access_token':token})
    time.sleep(0.1)
    languages = response.json()
    for language in languages:
        if languages[language].startswith("Python (python 2"):
            python_id = language
            return

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

def parse_python_command(cmd):
    if cmd.startswith("python "):
        return [cmd[7:]]
    else:
        return False

def exec_python(cmd, bot, args, msg, event):
    global sphere_url
    global token
    global python_id
    data = {'language':int(python_id), 'sourceCode':args[0]}
    response = requests.post(sphere_url + 'submissions', data, params={'access_token':token})
    while True:
        output = requests.get(sphere_url + 'submissions/' + str(response.json()['id']), params={'access_token':token, 'withOutput':1})
        if output.json()['status']==0:
            break
        time.sleep(0.2)
    return output.json()['output']
    


commands = [  # A list of all Commands in this Module.
    Command( 'python', exec_python, 'Execute python code and shows you the output.\nSyntax:\n$PREFIXpython <pythoncode>\nSupports multiline programs.', False, False, False, parse_python_command )
]
