from Module import Command
import requests
import time
from threading import Thread
import re
import SaveIO

sphere_url = "http://api.compilers.sphere-engine.com/api/3/"
python_id = 4
save_subdir = "python"


def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
    global sphere_url
    global python_id
    response = requests.get(sphere_url + 'languages', params={'access_token':get_token()})
    time.sleep(0.1)
    languages = response.json()
    for language in languages:
        if languages[language].startswith("Python (python 3"):
            python_id = language
            return
    print "token: " + get_token()
    print "WARNING: failed to find python, perhaps you didn't correctly set your Sphere Engine API key in /botdata/python/SphereEngineKey.txt?"

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

def get_token():
    return SaveIO.load(save_subdir, "SphereEngineKey", "txt")

def parse_python_command(cmd):
    if cmd.startswith("python "):
        return [cmd[7:]]
    else:
        return False

def get_python_result(id, msg, room):
    while True:
        output = requests.get(sphere_url + 'submissions/' + id, params={'access_token':get_token(), 'withOutput':1, 'withStderr':1, 'withCmpinfo':1})
        if output.json()['status'] == 0:
            break
        time.sleep(0.2)
    result = ''
    if output.json()['result'] == 15:
        reply = 'result:'
        result = output.json()['output']
    elif output.json()['result'] == 11:
        reply = 'compiler error:'
        result = output.json()['cmpinfo']
    elif output.json()['result'] == 12:
        reply = 'runtime error:'
        result = output.json()['stderr']
    elif output.json()['result'] == 13:
        reply = "I'm afraid your code ran for too long."
    elif output.json()['result'] == 17:
        reply = "Your code took up too much memory"
    elif output.json()['result'] == 19:
        reply = "Do you really want to hurt me?"
    else:
        reply = "Oops, something went wrong, try submitting your code again, or contact $OWNER_NAME if the problem persists."
    msg.reply(reply)
    if result:
        result = re.compile('^', re.M).sub('    ', result)
        room.send_message(result)


def exec_python(cmd, bot, args, msg, event):
    global sphere_url
    global python_id
    try:
        data = {'language':int(python_id), 'sourceCode':args[0]}
        response = requests.post(sphere_url + 'submissions', data, params={'access_token':get_token()})
        python_thread = Thread(target=get_python_result, args=(str(response.json()['id']), msg, bot.room))
        python_thread.start()
        return "I'm working on it."
    except KeyError:
        return "Oops, something went wrong, try submitting your code again, or contact $OWNER_NAME if the problem persists."
    


commands = [  # A list of all Commands in this Module.
    Command( 'python', exec_python, 'Execute python 3 code and shows you the output.\nSyntax:\n$PREFIXpython <pythoncode>\nSupports multiline programs.', False, False, False, parse_python_command )
]

module_name = "python"
