import hashlib
import re
from animazione import *

hash_name = 'user:name:' 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(redis):
    global hash_name 
    user_name = str(input('Inserisci il tuo nome utente: ').strip())
    hash_key = hash_name+user_name
    check=redis.exists(hash_key)
    if check==0 and user_name!='':
        while True:
            password = input('Inserisci la password: ').strip()
            if password!= '':
                password_valid = input('Conferma la password: ').strip()
                if (password != password_valid):
                    print('Le due password sono diverse') 
                else:
                    redis.hset(f'{hash_name}{user_name}',mapping={'user_name': user_name,'password':hash_password(password),'stato':0})
                    clear_screen()
                    print('Utente Registrato correttamente')
                    break
            else:
                clear_screen()
                print('Hai inserito una password vuota')
    else:
        clear_screen()
        print(f"l'utente {user_name} è già registrato")
        
def login(redis):
    global hash_name 
    user_name = str(input('Inserisci il tuo nome utente: ').strip())
    password = input('Inserisci la password: ').strip()

    hash_key = hash_name+user_name
    
    check=redis.exists(hash_key)
    
    if check==1:
        password_encripted = redis.hget(hash_key, 'password')
        if hash_password(password)==password_encripted:
            clear_screen()
            print(f"{user_name} hai effettuato correttamente il login")
            return user_name
        else:
            clear_screen()
            print('Dati non inseriti correttamente')
            return None
    else:
        clear_screen()
        print('Dati non inseriti correttamente')
        return None

def choice():
    ...
    
def add_friend(redis, user_name):
    global hash_name
    
    hash_friend = 'user:friends:'
    hash_key_friend = hash_friend + user_name

    clear_screen()
    
    friend_search_pattern = str(input('Inserisci il nome (o parziale) del utente da aggiungere: ').strip())
    regex_pattern = re.compile(friend_search_pattern.replace('*', '.*'), re.IGNORECASE)
    
    matching_friends = []
    for key in redis.scan_iter(f'{hash_name}*'):
        friend_name = key.replace(hash_name, '')
        if regex_pattern.match(friend_name):
            matching_friends.append(friend_name)
    
    if matching_friends:
        print("Utenti trovati:")
        for idx, friend in enumerate(matching_friends, start=1):
            print(f"{idx}. {friend}")
        
        try:
            selezione = int(input('Seleziona un numero per aggiungere un amico: ').strip())
            if 1 <= selezione <= len(matching_friends):
                selected_friend = matching_friends[selezione - 1]
                if not redis.sismember(hash_key_friend, selected_friend):
                    redis.sadd(hash_key_friend, selected_friend)
                    clear_screen()
                    print(f'Utente {selected_friend} aggiunto correttamente')
                else:
                    clear_screen()
                    print('Utente già presente nella lista amici')
            else:
                print('Selezione non valida')
        except TypeError:
            print('Inserisci un numero valido')
    else:
        clear_screen()
        print('Nessun amico trovato con quel criterio di ricerca')


def remove_friend(redis, user_name):
    hash_friend = 'user:friends:'
    
    friend_name = str(input('Inserisci il nome del utente da rimuovere: ').strip())
    hash_key_friend = hash_friend + user_name
    
    if redis.exists(hash_key_friend):
        friend_values = {value for value in redis.smembers(hash_key_friend)}
        if friend_name in friend_values:
            redis.srem(hash_key_friend, friend_name)
            clear_screen()
            print(f'Utente {friend_name} rimosso correttamente')
        else:
            clear_screen()
            print(f'Utente {friend_name} non è presente nella lista amici')
    else:
        clear_screen()
        print(f'Utente {friend_name} non è presente nella lista amici')

def get_friends(redis, user_name):

    hash_friend = 'user:friends:'
    hash_key_friend = hash_friend + user_name

    if redis.exists(hash_key_friend):
        friend_values = [value for value in redis.smembers(hash_key_friend)]
        if friend_values!=None:
            clear_screen()
            return friend_values
        else:
            clear_screen()
            print(f'{user_name} non ha amici nella lista')
    else:
        clear_screen()
        print(f'Lista degli amici per {user_name} non esiste')

def do_not_disturb(redis,user_name):
    global hash_name
    if int(redis.hget(f'{hash_name}{user_name}','stato')) == 0:
        redis.hset(f'{hash_name}{user_name}','stato',1)
        clear_screen()
        print('Sei in modalità non disturbare')
    elif int(redis.hget(f'{hash_name}{user_name}','stato')) == 1:
        redis.hset(f'{hash_name}{user_name}','stato',0)
        clear_screen()
        print('Non sei in modalità non disturbare')
