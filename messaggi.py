import time
from animazione import *
from utente import *

def send_message(r, from_user, to_user, temporary=False):
         
    message = input(f'\n{Fore.CYAN} > {Style.RESET_ALL}')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if message.upper()=='ESC': 
        return message
    elif int(r.hget(f"user:name:{to_user}", "stato")) == 1:
        print("!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA")  
        return None
    else:
        message_data = f"{timestamp}|{from_user}|{message}"
        r.zadd(f"messages:{from_user}:{to_user}", {message_data: time.time()})
        r.zadd(f"messages:{to_user}:{from_user}", {message_data: time.time()})

        r.sadd(f"chats:{from_user}", to_user)
        r.sadd(f"chats:{to_user}", from_user)
        
        r.publish(f"{to_user}:{from_user}", message_data)
        #r.publish(f"channel:{to_user}", message_data)
        #print(f"{Fore.RED} < {Style.RESET_ALL} {message} [{timestamp}] (Nuovo messaggio)")
    
    
    if temporary is True:
        r.expire(f"messages:{from_user}:{to_user}", 60)
        r.expire(f"messages:{to_user}:{from_user}", 60)
    
def read_messages(r, user_id, chat_id):
    new_var = f"messages:{user_id}:{chat_id}"
    messages = r.zrange(new_var, 0, -1)
    
    formatted_messaged = []
    for message in messages:
        timestamp, sender, msg = message.split("|", 2)
        prefix = (f'{Fore.CYAN} > {Style.RESET_ALL}') if sender == user_id else (f'{Fore.RED} < {Style.RESET_ALL}')
        formatted_messaged.append(f"{prefix} {msg} [{timestamp}]")
    return formatted_messaged

def delete_messages(r, user_id, chat_id):
    r.delete(f"messages:{user_id}:{chat_id}")
    r.delete(f"messages:{chat_id}:{user_id}")
    r.srem(f"chats:{user_id}", chat_id)
    r.srem(f"chats:{chat_id}", user_id)


def get_status(r,user_name):
    if int(r.hget(f'{hash_name}{user_name}','stato')) == 0:
        return 'False'
    else:
        return 'True'
