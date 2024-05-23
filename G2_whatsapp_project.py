import redis
from utente import *
#from messaggi import *

def utente_session(r, user_name):
    while True:
        print("\nSeleziona un'opzione:\n" +
            "1. Aggiungi un contatto\n" +
            "2. Mostra rubrica\n" +
            "3. Imposta modalità Do Not Disturb\n" +
            "4. Logout")
        choice = input("Inserisci il numero dell'opzione: ")
        
        if choice == '1':
            add_friend(r,user_name)
            # results = user_name.search_utente(query)
            # print("Risultati della ricerca:")
            # for result in results:
            #     print(result)
            # contact_id = input("Inserisci l'ID dell'utente da aggiungere ai contatti: ")
            # if user_name.add_friend(user_name, contact_id):
            #     print("Utente aggiunto con successo alla lista contatti.")
            # else:
            #     print("Aggiunta contatto fallita.")
        
        elif choice == '2':
            contacts = user_name.get_contacts(user_name)
            print("La tua rubrica:")
            for contact in contacts:
                print(contact)
            chat_utente = input("Inserisci il nome utente per iniziare una chat: ")
            user_name.add_chat(user_name, chat_utente)
            chat_session(messaggi, user_name, chat_utente)
        
        elif choice == '3':
            chats = user_name.get_chats(user_name)
            print("Chat attive:")
            for chat in chats:
                print(chat)
            chat_utente = input("Inserisci il nome utente per continuare la chat: ")
            chat_session(messaggi, user_name, chat_utente)
        
        elif choice == '4':
            status = input("Imposta modalità Do Not Disturb (on/off): ").lower() == 'on'
            user_name.set_dnd(user_name, status)
            print(f"Modalità Do Not Disturb impostata su {'on' if status else 'off'}")
        
        elif choice == '5':
            print(f"Logout effettuato con successo. Arrivederci, {user_name}!")
            break
        
        else:
            print("Opzione non valida. Riprova.")
            
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