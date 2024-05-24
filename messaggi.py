import time

def send_message(redis, from_user, to_user):
    message = input('> ')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if int(redis.hget(f"user:name:{to_user}", "stato")) == 1:
        print("!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA")
    elif message.upper()=='ESC': 
        return message   
    else:
        message_data = f"{timestamp}|{from_user}|{message}"
    # last_element = redis.zrevrange(f"messages:{from_user}:{to_user}", 0, 0, withscores=True)
    # print(last_element[0])
    #time.time()*1000
        redis.zadd(f"messages:{from_user}:{to_user}", {message_data: time.time()})
        redis.zadd(f"messages:{to_user}:{from_user}", {message_data: time.time()})

        redis.sadd(f"chats:{from_user}", to_user)
        redis.sadd(f"chats:{to_user}", from_user)
    
    
def read_messages(redis, user_id, chat_id):
    messages = redis.zrange(f"messages:{user_id}:{chat_id}", 0, -1)
    formatted_messaged = []
    for message in messages:
        timestamp, sender, msg = message.split("|", 2)
        prefix = '>' if sender == user_id else '<'
        formatted_messaged.append(f"{prefix} {msg} [{timestamp}]")
    formatted_messaged.reverse()  
    return formatted_messaged