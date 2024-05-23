import redis
from utente import *
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