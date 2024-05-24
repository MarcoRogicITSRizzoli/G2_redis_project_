import time

def send_message(r, from_user, to_user, message, temporary=False):
    message = input()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if int(r.hget(f"user:name:{to_user}", "stato")) == 1:
        message_data = f"{timestamp}|{from_user}|{"!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA"}" 
    elif message.upper()=='ESC': 
        return message   
    else:
        message_data = f"{timestamp}|{from_user}|{message}"
    #time.time()*1000
    r.zadd(f"messages:{from_user}:{to_user}", {message_data: time.time()})
    r.zadd(f"messages:{to_user}:{from_user}", {message_data: time.time()})

    r.sadd(f"chats:{from_user}", to_user)
    r.sadd(f"chats:{to_user}", from_user)
    
    if temporary:
        r.expire(f"messages:{from_user}:{to_user}", 60)
        r.expire(f"messages:{to_user}:{from_user}", 60)
    
def read_messages(r, user_id, chat_id):
    messages = r.zrange(f"messages:{user_id}:{chat_id}", 0, -1)
    formatted_messaged = []
    for message in messages:
        timestamp, sender, msg = message.split("|", 2)
        prefix = '>' if sender == user_id else '<'
        formatted_messaged.append(f"{prefix} {msg} [{timestamp}]")
    return formatted_messaged

def delete_messages(r, user_id, chat_id):
    r.delete(f"messages:{user_id}:{chat_id}")
    r.delete(f"messages:{chat_id}:{user_id}")
    r.srem(f"chats:{user_id}", chat_id)
    r.srem(f"chats:{chat_id}", user_id)