import redis
from utente import *
from messaggi import *
from animazione import *

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
    a = ("\nBenvenuto nel sistema di messaggistica!")
    anim(a)
    while True:
        sel = ("\nSeleziona un'opzione:\n"+
              "1. Registrati\n"+
              "2. Login\n"+
              "3. Esci\n")
        anim(sel)
       
        try:
            choice = int(input("Inserisci il numero dell'opzione: "))
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
