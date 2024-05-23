import redis
from utente import *
from messaggi import *

def utente_session(r, user_name):
    stato=''
    while True:
             
        if int(r.hget(f'{hash_name}{user_name}','stato'))==0:
            stato='False'
        else:
            stato='True'
            
        print("\nSeleziona un'opzione:\n" +
            "1. Aggiungi un contatto\n" +
            "2. Mostra rubrica\n" +
            "3. Mostra chat iniziate\n" +
            f"4. Modalità Do Not Disturb: {stato}\n" +
            "5. Logout")
        choice = input("Inserisci il numero dell'opzione: ")
        
        if choice == '1':
            add_friend(r,user_name)
        elif choice == '2':
            select_contact_to_chat(r,user_name)
        elif choice == '3':
            active_chats(r, user_name)
        elif choice == '4':
            do_not_disturb(r,user_name)
        elif choice == '5':
            os.system('cls')
            print(f"Logout effettuato con successo. Arrivederci, {user_name}!")
            break
        else:
            os.system('cls')
            print("Opzione non valida. Riprova.")

def select_contact_to_chat(r, user_name):
    contatti = get_friends(r, user_name)
    chat_utente = input("Inserisci il nome utente del contatto da chat: ")
    if chat_utente.upper() != 'ESC':
        if chat_utente in contatti:
            chat_session(r, user_name, chat_utente)
        else:
            print("Utente non trovato.")

def active_chats(r, user_name):
    while True:
        chats = r.smembers(f"chats:{user_name}")
        print("\nChat attive:")
        for chat in chats:
            print(chat)
        chat_user = input("Inserisci il nome utente per continuare la chat o scrivi 'ESC' per tornare al menu delle chat: ")
        if chat_user.upper() == 'ESC':
            break
        if chat_user in chats:
            chat_session(r, user_name, chat_user)

def chat_session(r, from_utente, to_utente):
    while True:
        chat = read_messages(r, from_utente, to_utente)
        print(f"\n>> Chat con {to_utente} <<")
        for msg in chat:
            print(msg)
        
        print("\nDigita il tuo messaggio o 'ESC' per tornare al menu delle chat attive: ")
        message = input()
        if message.upper() == 'ESC':
            break
        error_message = send_message(r, from_utente, to_utente, message)
        if error_message:
            print(error_message)
            
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
        
        if choice == '1':
            sign_up(r)
        elif choice == '2':
            user_name = login(r)
            if user_name != None: 
                utente_session(r, user_name)

        elif choice == '3':
            print("Grazie per aver utilizzato il sistema di messaggistica. Arrivederci!")
            break
        
        else:
            print("Opzione non valida. Riprova.")

if __name__ == '__main__':
    main()