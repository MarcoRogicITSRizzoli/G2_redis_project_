import time

def logout(strlog ,user_name):
    for x in range(len(strlog)):
        print(strlog[x], end='', flush=True)
        time.sleep(0.06)