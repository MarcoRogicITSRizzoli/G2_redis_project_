import redis
import threading
from utente import *
from messaggi import *
from animazione import *

def utente_session(r, user_name):
    while True:
        print("\nSeleziona un'opzione:\n" +
            "1. Aggiungi un contatto\n" +
            "2. Rimuovi contatto\n" +
            "3. Mostra rubrica\n" +
            "4. Mostra chat iniziate\n" +
            f"5. Modalità Do Not Disturb: {get_status(r,user_name)}\n" +
            "6. Logout")
        choice = input("Inserisci il numero dell'opzione: ")
        
        match choice:
            case '1':
                add_friend(r,user_name)
            case '2':
                remove_friend(r,user_name)
            case '3':
                select_contact_to_chat(r,user_name)
            case '4':
                active_chats(r, user_name)   
            case '5':
                do_not_disturb(r,user_name)
            case '6':
                os.system('cls')
                strlog = f"Logout effettuato con successo. Arrivederci, {user_name}!"
                logout(strlog, user_name)
                break
            case _:
                os.system('cls')
                print("Opzione non valida. Riprova.")

def get_status(r,user_name):
    if int(r.hget(f'{hash_name}{user_name}','stato')) == 0:
        return 'False'
    else:
        return 'True'
    
def select_contact_to_chat(r, user_name):
    contatti = get_friends(r, user_name)
    if contatti:
        chat_utente = input("Inserisci il nome utente del contatto da chat: ")
        if chat_utente.upper() != 'ESC':
            if chat_utente in contatti:
                type_chat = input("Che tipologia di chat vuoi iniziare, normale (N) o effimera (E)?: ")
                if type_chat.upper() == 'E':
                    print("Chat effimera iniziata.")
                    chat_session(r, user_name, chat_utente, True)
                else:
                    print("Chat iniziata.")
                    chat_session(r, user_name, chat_utente, False)
            else:
                print("Utente non trovato.")
    else:
        print("Non hai contatti in rubrica.")

def active_chats(r, user_name):
    while True:
        chats = r.smembers(f"chats:{user_name}")
        os.system('cls')
        print("\nChat attive:\n"+
              '-'*30)
        for chat in chats:
            print(chat)
        print('-'*30)    
        chat_user = input("Inserisci il nome utente per continuare la chat o \nscrivi 'ESC' per tornare al menu delle chat: ")
        if chat_user.upper() == 'ESC':  
            break
        if chat_user in chats:
            chat_session(r, user_name, chat_user,False)

def show_chat(r,from_utente,to_utente):
    os.system('cls')
    print("\nDigita il tuo messaggio o 'ESC' per tornare al menu delle chat attive: \n"+
         f"\n>> Chat con {to_utente} <<\n"+
         '-'*30)
    chat = read_messages(r, from_utente, to_utente)
    if int(r.hget(f"user:name:{to_utente}", "stato")) == 1:
        print("!! IMPOSSIBILE RECAPIRTARE IL MESSAGIO, L'UTENTE HA LA MODALITA' DND ATTIVA") 
    for msg in chat:
        print(msg)
    print('-'*30)
    
def chat_session(r, from_utente, to_utente, temporary:bool):
    os.system('cls')
    threading.Thread(target=subscribe_message, args=(redis, from_utente)).start()
    while True:
        show_chat(r,from_utente,to_utente) 
        message = send_message(r, from_utente, to_utente, temporary)
        if message is not None:
            break
              
def main():
    # Creare una connessione Redis
    r = redis.Redis(
    host='redis-18510.c55.eu-central-1-1.ec2.redns.redis-cloud.com',
    port=18510,
    db=0,
    username='bruno',
    password='User1234?',
    decode_responses=True,
    )
    r.ping()

    #utilizzare match case per fare il controllo
    
    print("Benvenuto nel sistema di messaggistica!")
    while True:
        print("\nSeleziona un'opzione:\n"+
              "1. Registrati\n"+
              "2. Login\n"+
              "3. Esci\n")
        choice = input("Inserisci il numero dell'opzione: ")
        
        match choice:
            case '1':
                sign_up(r)  
            case '2':
                user_name = login(r)
                if user_name != None: 
                    utente_session(r, user_name)
            case '3':
                print("Grazie per aver utilizzato il sistema di messaggistica. Arrivederci!")
                break
            case _:
                print("Opzione non valida. Riprova.")

if __name__ == '__main__':
    main()