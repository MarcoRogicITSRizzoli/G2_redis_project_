import redis
from registrazione import *
#from utente import Utente
#from messaggi import *

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
        print("\nSeleziona un'opzione:")
        print("1. Registrati")
        print("2. Login")
        print("3. Esci")
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