import time
from animazione import *
from utente import *
import threading
import redis

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
        
        r.publish(f"channel:{to_user}", message_data)
    
    if temporary is True:
        r.expire(f"messages:{from_user}:{to_user}", 60)
        r.expire(f"messages:{to_user}:{from_user}", 60)
    
def read_messages(r, user_id, chat_id):
    messages = r.zrange(f"messages:{user_id}:{chat_id}", 0, -1)
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
    
def select_contact_to_chat(r, user_name):
    contatti = get_friends(r, user_name) 
    if contatti:
        print("Utenti trovati:")
        for idx, contatto in enumerate(contatti, start=1):
            a = f"{idx}. {contatto}\n"
            anim(a)
        try:
            chat_utente_idx = input("Seleziona un numero per il nome utente del contatto da chat (o digita 'ESC' per uscire): ").strip()
            if chat_utente_idx.upper() == 'ESC':
                clear_screen()
                print("Operazione annullata.")
                return

            chat_utente_idx = int(chat_utente_idx)
            if 1 <= chat_utente_idx <= len(contatti):
                selected_user = contatti[chat_utente_idx - 1]
                type_chat = input("Che tipologia di chat vuoi iniziare, normale (N) o effimera (E)?: ").strip().upper()
                if type_chat == 'E':
                    clear_screen()
                    print("Chat effimera iniziata.")
                    chat_session(r, user_name, selected_user, True)
                else:
                    clear_screen()
                    print("Chat iniziata.")
                    chat_session(r, user_name, selected_user, False)
            else:
                print("Numero selezionato non valido.")
        except ValueError:
            print('Inserisci un numero valido.')
    else:
        print("Non hai contatti in rubrica.")

def active_chats(r, user_name):
    while True:
        chats = r.smembers(f"chats:{user_name}")
        if chats:
            clear_screen()
            print(f"\n {Fore.YELLOW}>> chat attive <<{Style.RESET_ALL}\n"+
                '-'*60)
            for chat in chats:
                print(chat)
            print('-'*60)    
            chat_user = input("Inserisci il nome utente per continuare la chat o \nscrivi 'ESC' per tornare al menu delle chat: ")
            if chat_user.upper() == 'ESC':  
                clear_screen()
                break
            if chat_user in chats:
                chat_session(r, user_name, chat_user,False)
        else:
            clear_screen()
            print(f"\n {Fore.YELLOW} Non hai chat attive {Style.RESET_ALL}")
            break

def show_chat(r, from_user, to_user, notification: bool):
    clear_screen()
    print("\nDigita il tuo messaggio o 'ESC' per tornare al menu delle chat attive: \n" +
          f"\n {Fore.YELLOW} >> Chat con {to_user} << {Style.RESET_ALL} \n" +
          '-' * 60)
    
    chat = read_messages(r, from_user, to_user)
    # notification_numer = r.smembers(f"notification:{from_user}")
    # conut_numer = 0
    # for noti in notification_numer:
    #     date,to_user_to,mess = noti.split('|',2)
    #     if to_user_to == to_user:
    #         conut_numer =+1
    for i, msg in enumerate(chat):
        if notification and i == len(chat) - 1:
            print('\n' + msg + " (nuovo messaggio)")
        else:
            print('\n' + msg)
    
    if int(r.hget(f"user:name:{to_user}", "stato")) == 1:
        print("!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA")
    
    print('-' * 60)

def chat_session(r, from_user, to_user, temporary:bool):
    clear_screen()
    subscribe_message(r, from_user,to_user)
    show_chat(r,from_user,to_user,False)    
    
    while True: 

        message = send_message(r, from_user, to_user, temporary)
        if message is not None:
            break
        else:
            show_chat(r,from_user,to_user,False)
 


def callback_notification(message):
    r = redis.Redis(
    host='redis-18510.c55.eu-central-1-1.ec2.redns.redis-cloud.com',
    port=18510,
    db=0,
    username='bruno',
    password='User1234?',
    decode_responses=True,
    )
    from_user = message['channel'].split(':')[1]
    date,to_user,mess = message['data'].split('|',2)
    r.zadd(f"notification:{from_user}", {f"{date}|{to_user}|{mess}": time.time()})
    #print(f"{Fore.RED} < {Style.RESET_ALL} {mess} [{date}] (Nuovo messaggio)")
         
def subscribe_message(r, from_user,to_user):
    pubsub = r.pubsub()
    pubsub.psubscribe(**{f"channel:{from_user}": callback_notification})
    pubsub.psubscribe(**{f"channel:{to_user}": callback_notification})
    r.publish("utenti:registrazioni", from_user)
    pubsub.run_in_thread(sleep_time=0.01)

            
