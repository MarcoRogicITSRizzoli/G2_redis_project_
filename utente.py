import hashlib
import os

user_id = 0
hash_name = 'user:name:' 

class Utente:
    
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_up(redis):
        global hash_name 
        user_name = str(input('Inserisci il tuo nome utente: ').strip())
        hash_key = hash_name+user_name
        check=redis.exists(hash_key)
        if check==0:
            while True:
                password = input('Inserisci la password: ').strip()
                password_valid = input('Conferma la password: ').strip()
                if password != password_valid:
                    print('Le due password sono diverse') 
                else:
                    redis.hset(f'{hash_name}{user_name}',mapping={'user_name': user_name,'password':Utente.hash_password(password),'stato':'False'})
                    os.system('cls')
                    print('Utente Registrato correttamente')
                    break
        else:
            os.system('cls')
            print(f"l'utente {user_name} è già registrato")
            
    def login(redis):
        global hash_name 
        user_name = str(input('Inserisci il tuo nome utente: ').strip())
        password = input('Inserisci la password: ').strip()

        hash_key = hash_name+user_name
        
        check=redis.exists(hash_key)
        
        if check==1:
            password_encripted = redis.hget(hash_key, 'password').decode('utf-8')
            if check==1 and Utente.hash_password(password)==password_encripted:
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
        
    def add_friend(redis,user_name):
        global user_id
        global hash_name 
        
        hash_friend = 'user:friends:'
        
        friend_name = str(input('Inserisci il nome del utente da aggiungere: ').strip())
        
        hash_key_friend = hash_friend+user_name
        hash_key_name= hash_name+friend_name
        
        check=redis.exists(hash_key_name)
        if check==1:
            friend_values = [value.decode('utf-8') for value in redis.lrange(hash_key_friend, 0, -1)]
            if friend_name not in friend_values:   
                redis.rpush(f"{hash_friend}{user_name}", friend_name)
                os.system('cls')
                print('Utente aggiunto correttamente')
            else:
                os.system('cls')
                print('Utente non aggiunto correttamente')
        else:
            os.system('cls')
            print(f'Utente {friend_name} non esiste')
