import redis
import hashlib
import os

import redis

r = redis.Redis(
  host='redis-13373.c300.eu-central-1-1.ec2.redns.redis-cloud.com',
  port=13373,
  db =0,
  password='vbcod20kBBvGKDqux3rNg24FbFpmVU2K')
r.ping

user_id = 0

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    hash_name = 'user:name:'
    user_name = str(input('Inserisci il tuo nome utente: ').strip())
    hash_key = hash_name+user_name
    check=r.exists(hash_key)
    if check==0:
        while True:
            password = input('Inserisci la password: ').strip()
            password_valid = input('Conferma la password: ').strip()
            if password != password_valid:
                print('Le due password sono diverse') 
            else:
                r.hset(f'{hash_name}{user_name}',mapping={'user_name': user_name,'password':hash_password(password),'pass':password,'stato':'False'})
                os.system('cls')
                print('Utente Registrato correttamente')
                break
    else:
        os.system('cls')
        print(f"l'utente {user_name} è già registrato")
        
        
def login():
    hash_name = 'user:name:'
    user_name = str(input('Inserisci il tuo nome utente: ').strip())
    password = input('Inserisci la password: ').strip()

    hash_key = hash_name+user_name
    
    check_name=r.exists(hash_key)
    check=r.exists(hash_key)
    
    if check==1:
        password_encripted = r.hget(hash_key, 'password').decode('utf-8')
        if check_name==1 and hash_password(password)==password_encripted:
            os.system('cls')
            print(f"{user_name} hai effettuato correttamente il login")
            return user_name
        else:
            os.system('cls')
            print('Dati non inseriti correttamente')
            return None
    else:
        os.system('cls')
        print('Dati non inseriti correttamente')
        return None
    
def add_friend(user_name):
    global user_id
    hash_friend = 'user:friends:'
    hash_name = 'user:name:'
    
    friend_name = str(input('Inserisci il nome del utente da aggiungere: ').strip())
    
    hash_key_friend = hash_friend+user_name
    hash_key_name= hash_name+friend_name
    
    check=r.exists(hash_key_name)
    if check==1:
        friend_values = [value.decode('utf-8') for value in r.lrange(hash_key_friend, 0, -1)]
        if friend_name not in friend_values:   
            r.rpush(f"{hash_friend}{user_name}", friend_name)
            os.system('cls')
            print('Utente aggiunto correttamente')
        else:
            os.system('cls')
            print('Utente non aggiunto correttamente')
    else:
        os.system('cls')
        print(f'Utente {friend_name} non esiste')

def main():
    print('Connesso a Redis.')
    while True:
        print('-'*30)
        print('1. login')
        print('2. sign up')
        print('-'*30)
        scelta = input('Scelta: ')
        if scelta == '1':
            logg=login()
            if logg!=None:
                while True:
                    print('-'*30)
                    print('1. Aggiungi amico')
                    print('2. Inizia una nuova chat')
                    print('3. Visulizza chat recenti')
                    print('0. Exit')
                    print('-'*30)
                    scelta = input('Scelta: ')
                    
                    if scelta=='1':
                        add_friend(logg)
                        
                        ...
                    elif scelta == '2':  
                        ...
                    elif scelta ==' 0':
                        break
            else:
                print('Errore hai inserito delle credenziali errate')
        elif scelta == '2':
            sign_up()
        else:
            os.system('cls')
            print('scelta non valida')
            

if __name__ == '__main__':
    main()

