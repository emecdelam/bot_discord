import json
import pickle
from datetime import datetime

from aioconsole import ainput
from logging_system import log__,Colors,Level

async def clean_log(*args):
    """Cleans the log"""
    with open('error.log','w') as log_file:
        log_file.write('')
    await log__("Log file cleaned.",Level.DEBUG,Colors.lightcyan)
async def print_db(*args):
    """Writes the messages in the db"""
    messages = pickle.load(open("db\\messages.p","rb"))
    with open("admin/db.json","w") as file:
        json.dump(messages,file,indent = 4)
    await log__("Message writted in admin/db",Level.DEBUG,Colors.lightcyan)
async def switch_db(*args):
    """Switch the state of a user in the messages db list,use msg_id then user_id"""
    messages = pickle.load(open("db\\messages.p","rb"))
    msg_id = args[0]
    user_id = args[1]
    if msg_id in messages.keys():
        if user_id in messages[msg_id].keys():
            messages[msg_id][user_id] = not messages[msg_id][user_id]
            pickle.dump(messages,open("db\\messages.p","rb"))
        else:
            await log__("User not in db",Level.DEBUG,Colors.lightcyan)
    else:
        await log__("Message not in db",Level.DEBUG,Colors.lightcyan)
async def command_handler(client):
    commands_dic = {
        'clean_logs':clean_log,
        'switch_db':switch_db,
        'print_db':print_db
    }
    while True:
        command = await ainput(f'{Colors.reset}{Colors.bold}[{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).ljust(19)}] [{str(Level.INFO).ljust(8)}] Enter a command (or help): {Colors.reset}\n')
        params = command.split(" ")[1:]
        command = command.split(" ")[0]
        if command.lower() == "help":
            res = "\n"
            for cmd,doc in commands_dic.items():
                res += f"{cmd} : {doc.__doc__}\n"
            await log__(res,Level.INFO,Colors.green)
        elif command.lower() in commands_dic:
            await commands_dic[command.lower()](params)
        elif command.lower() == 'exit':
            await client.close()
            break
        else:
            await log__("Unknown command. Try 'clean_logs' or 'exit'.",Level.DEBUG,Colors.orange)