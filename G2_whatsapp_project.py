import redis
from utente import *
from messaggi import *
from animazione import *

 # Creare una connessione Redis
r = redis.Redis(
host='redis-18510.c55.eu-central-1-1.ec2.redns.redis-cloud.com',
port=18510,
db=0,
username='bruno',
password='User1234?',
decode_responses=True,
)
    
def utente_session(r, user_name):
    
    while True:
        sel = ("\nSeleziona un'opzione:\n" +
            "1. Aggiungi un contatto\n" +
            "2. Rimuovi contatto\n" +
            "3. Mostra rubrica\n" +
            "4. Mostra chat iniziate\n" +
            f"5. Modalità Do Not Disturb: {get_status(r,user_name)}\n" +
            "6. Logout\n")
        anim(sel)

        try:
            choice = int(input("Inserisci il numero dell'opzione: "))
            match choice:
                case 1:
                    add_friend(r,user_name)
                case 2:
                    remove_friend(r,user_name)
                case 3:
                    select_contact_to_chat(r,user_name)
                case 4:
                    active_chats(r, user_name)   
                case 5:
                    do_not_disturb(r,user_name)
                case 6:
                    clear_screen()
                    strlog = f"Logout effettuato con successo. Arrivederci, {user_name}!"
                    anim(strlog)
                    break
                case _:
                    clear_screen()
                    print("Opzione non valida. Riprova.")
                    raise ValueError
        except ValueError:
            clear_screen()
            print('Errore hai inserito un opzione inesistente')

    
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
    notification_numer = r.zrange(f"notification:{from_user}:{to_user}", 0, -1)

    if notification and len(notification_numer) > 0:
        for msg in chat[:-len(notification_numer)]:
            print('\n' + msg)
        print(f'\n----------------{Fore.YELLOW} Hai dei nuovi messaggi da {to_user} {Style.RESET_ALL}----------------\n')
        for msg in chat[-len(notification_numer):]:
            print('\n' + msg)
    else:
        for msg in chat:
            print('\n' + msg)
                
                
    if int(r.hget(f"user:name:{to_user}", "stato")) == 1:
        print("!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA")
    
    print('-' * 60)

def delete_notification(r, from_user,to_user):
    r.delete(f"notification:{from_user}:{to_user}")

def chat_session(r, from_user, to_user, temporary:bool):
    clear_screen()
    pubsub = r.pubsub()
    pubsub.psubscribe(**{f"{from_user}:{to_user}": callback_notification})
    pubsub.psubscribe(**{f"{to_user}:{from_user}": callback_notification})
    pubsub.get_message()
    thread = pubsub.run_in_thread(sleep_time=0.01)
    
    show_chat(r,from_user,to_user,True)    
    delete_notification(r, from_user,to_user)
    while True: 
        message = send_message(r, from_user, to_user, temporary)
        if message is not None:
            delete_notification(r, from_user,to_user)
            break
        else:
            show_chat(r,from_user,to_user,False)
            
    thread.stop()

def callback_notification(message):
    to_user,from_user = message['channel'].split(':')
    date,from_user,mess = message['data'].split('|',2)
    print(f'{Fore.RED} < {Style.RESET_ALL}',f" {mess} [{date}]")
    r.zadd(f"notification:{to_user}:{from_user}", {f"{date}|{to_user}|{mess}": time.time()})

 
def main():
    global r
   
    r.ping()
    a = ("\nBenvenuto nel sistema di messaggistica!")
    anim(a)
    while True:
        sel = ("\nSeleziona un'opzione:\n"+
              "1. Registrati\n"+
              "2. Login\n"+
              "3. Esci\n")
        anim(sel)
       
        try:
            choice = int(input(f"{Fore.YELLOW}Inserisci il numero dell'opzione: {Style.RESET_ALL}"))
            match choice:
                case 1:
                    sign_up(r)  
                case 2:
                    user_name = login(r)
                    if user_name != None: 
                        utente_session(r, user_name)
                case 3:
                    strlog = "Grazie per aver utilizzato il sistema di messaggistica. Arrivederci!"
                    anim(strlog)
                    break
                case _:
                    clear_screen()
                    print("Opzione non valida. Riprova.")
                    raise ValueError
        except ValueError:
            clear_screen()
            print('Errore hai inserito un opzione inesistente')

if __name__ == '__main__':
    main()
