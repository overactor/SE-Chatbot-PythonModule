from Module import Command
import requests


# def on_bot_load(bot): # This will get called when the bot loads (after your module has been loaded in), use to perform additional setup for this module.
#     pass

# def on_bot_stop(bot): # This will get called when the bot is stopping.
#     pass

# def on_event(event, client, bot): # This will get called on any event (messages, new user entering the room, etc.)
#     pass

def parse_python_command(cmd):
    if cmd.startswith("python\n"):
        return [cmd[7:]]
    else:
        return False

def exec_python(cmd, bot, args, msg, event):
    return args[0]


commands = [  # A list of all Commands in this Module.
    Command( 'python', exec_python, 'Execute python code and shows you teh output.\nSyntax:\n$PERFIXpython\n<pythoncode>', False, False, False, parse_python_command )
]
