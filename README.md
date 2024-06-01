<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Indice</summary>
  <ol>
    <li>
      <a href="#il-progetto">Il Progetto</a>
      <ul>
        <li><a href="#librerie-principali">Librerie principali</a></li>
      </ul>
    </li>
    <li>
      <a href="#come-iniziare">Come iniziare</a>
      <ul>
        <li><a href="#prerequisiti">Prerequisiti</a></li>
        <li><a href="#installazioni">Installazioni</a></li>
        <li><a href="#avvio-del-software">Avvio del software</a></li>
      </ul>
    </li>
    <li>
      <a href="#istruzioni">Istruzioni</a>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#fonti">Fonti</a></li>
  </ol>
</details>


## Il Progetto

Abbiamo realizzato un sistema di chat in tempo reale che utilizza Redis come backend per la memorizzazione dei dati e la gestione della messaggistica. La struttura è suddivisa in vari moduli, ognuno dei quali si occupa di specifiche funzionalità. Il tutto è coordinato dal modulo principale, G2_whatsapp_project, che gestisce le interazioni tramite interfaccia utente.

Per sviluppare ulteriori funzionalità e migliorare l'aspetto grafico, abbiamo apportato alcune modifiche rispetto ad alcune richieste di svolgimento del progetto:
1. Oltre al prefisso < per il sender ed il > per il receiver, abbiamo usato il colore rosso per il primo e l'azzurro per il secondo poiché solo il prefisso rendeva confusionaria la visualizzazione
2. Le chat, contrariamente a quanto richiesto, abbiamo preferito una visualizzazione dei messaggi più recenti in fondo poiché più conforme ad un software di messaggistica come whatsapp 
3. Con il comando pubsub abbiamo creato un canale di comunicazione tra due utenti in modo che essa sia in tempo reale e l'inserimento delle notifiche durante la chat 
4. Abbiamo implementato un launcher posizionato all'interno della cartella dist in modo da permettere ad un qualsiasi utente di lanciare il software senza la necessità di installare alcuna libreria, lasceremo però un tutorial su come installarle in caso si volesse fare un giro completo dal modulo principale.

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>



### Librerie principali

- `redis`: Per interagire con il server Redis.
- `hashlib`: Per l'hashing della password.
- `os`: Per le operazioni di sistema
- `re`: Per la gestione delle espressioni regolari
- `time`: Per la gestione dei timestamp
- `colorama`: Per la colorazione dei caratteri

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>



## Come iniziare


### Prerequisiti

Prima di eseguire l'applicazione, assicurarsi di avere i seguenti prerequisiti installati:

1. **Python V 3.12:** Per installare la versione di python necessaria, potete scaricarlo dal sito ufficiale https://www.python.org/downloads/

2. **Server Redis:** Nel codice è già inserito un redis server Cloud per il salvataggio dei dati, se si vuole utilizzare un proprio server redis e visualizzare i dati, ci si può iscrivere gratuitamente al sito tramite il seguente link: https://redis.io/try-free/ .
Effettuata la registrazione si avrà a disposizione un proprio database gratuito con un limite di 30mb, selezionatelo e copiate il public endpoint di cui le cifre finali sono la porta modificando le informazioni presenti nel modulo G2_whatsapp_project 



### Installazioni
1° Metodo

1. Clonare la repository in locale aprendo il terminale dalla cartella in cui si vuole inserire il progetto
   ```sh
   git clone https://github.com/MarcoRogicITSRizzoli/G2_redis_project_.git
   ```
2. Launcher
    Aprire la cartella dist e cliccare due volte su G2_whatsapp_project.exe

2° Metodo
1. Clonare la repository in locale aprendo il terminale dalla cartella in cui si vuole inserire il progetto
   ```sh
   git clone https://github.com/MarcoRogicITSRizzoli/G2_redis_project_.git
   ```
2. Installazione di pip
    Comando per Windows:
   ```sh
   py -m ensurepip --upgrade
   ```
   Comando per Mac:
   ```sh
   python3 -m ensurepip --upgrade
   ```
3. Creazione dell'ambiente di sviluppo venv usando requirements.txt (Per Windows)
   Aprire il terminale tenendo come percorso la cartella in cui si vuole installare l'ambiente
   ```sh
   python -m venv venv
   ```
   ```sh
   venv\Scripts\activate
   ```
   ```sh
   pip install -r requirements.txt
   ```
4. Creazione dell'ambiente di sviluppo venv usando requirements.txt (Per Mac)
    Aprire il terminale tenendo come percorso la cartella in cui si vuole installare l'ambiente
    ```sh
    python3 -m venv venv
    ```
    ```sh
    source venv/bin/activate
    ```
    ```sh
    pip install -r requirements.txt
    ```
    Per verificare la corretta installazione delle librerie, usare il comando:
    ```sh
    pip list
    ```      

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>


### Avvio del software

Il modulo G2_whatsapp_project funge da contenitore del main per il lancio del software ma è possibile avviarlo direttamente da terminale

1. Avvio del software da terminale
    Comando per Windows
   ```sh
   py .\G2_whatsapp_project.py
   ```
   Comando per Mac
   ```sh
   python3 G2_whatsapp_project.py
   ```

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>


## Istruzioni

Il software ha sei funzionalità principali, descritte di seguito:

1. Registrazione:
L'utente può effettuare una registrazione scegliendo uno username ed una password di cui sarà richiesta la conferma.
Nel caso l'utente inserisse uno username già presente su redis non sarà possibile concludere la registrazione e nel caso la password di conferma non coincidesse con quella scritta precedentemente si riceverà un errore.

2. Login:
l'utente inserirà il proprio username e la propria password, se essi non dovessero coincidere o se lo user non esiste si riceverà un errore.

3. Ricerca ed aggiunta alla rubrica di un utente:
L'utente avrà la possibilità di ricercare gli utenti digitando lo username, anche in modo parziale, ricevendo una lista con user simili.
Se verranno inseriti username senza riscontro di verosomiglianza si riceverà un messaggio di errore.

4. Eliminazione di un utente dalla propria rubrica:
L'utente può decidere di eliminare un qualsiasi contatto dalla rubrica con la conseguente eliminazione della chat attiva con lui

5. Visualizzazione della propria rubrica ed inizio di una chat:
L'utente può vedere tutti gli utenti che ha aggiunto e col quale può decidere di iniziare una chat con uno di loro, decidendo se essa dovrà essere standard oppure effimera, ossia con la caratteristica di cancellarsi automaticamente passato il minuto di tempo.
Se da questa schermata si decide di selezionare un'utente con cui si avrà già una chat in corso aprirà la chat attiva.
Se un'utente ci ha aggiunto alla propria rubrica ed inizierà una chat con noi non vedremo il suddetto utente come membro della rubrica in quanto non lo abbiamo aggiunto noi

6. Visualizzazione delle chat attive:
L'utente può visualizzare la lista di tutti gli utenti con cui ha già iniziato una chat.

7. Modalità Do-Not-Disturb:
La modalità Do-Not-Disturb permette agli utenti di disattivare temporaneamente la ricezione dei messaggi. Quando questa modalità è attiva, chiunque tenti di inviare un messaggio all'utente riceverà un avviso che informa che l'utente non è disponibile.

8. Logout:
L'utente tornerà alla schermata con le opzioni di login

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] *Ricerca degli utenti a sistema
- [x] *Aggiunta degli utenti nella propria rubrica
- [x] *Impostazione modalità Do Not Disturb
- [x] *Messaggistica con gli utenti nei contatti 
  - [x] *Messaggio di errore nel caso di invio di un messaggio ad un utente in modalità Do Not    Disturb
- [x] *Chat tra utenti con invio dei messaggi
  - [x] *Possibilità di creare una chat effimera della durata di 1 minuto
  - [x] *Chat con invio dei messaggi live
- [ ] *Creazione di un launcher per l'app
- [ ] *Supporto per l'invio di Media nelle chat


<p align="right">(<a href="#readme-top">torna in cima</a>)</p>


<!-- Fonti -->
## Fonti

Fonti consultate per la realizzazione del progetto

* [Documentazione per l'utilizo delle funzioni di redis](https://redis.io/docs/latest/develop/connect/clients/python/)
* [Documentazione di threading per la live chat](https://docs.python.org/3/library/threading.html)
* [Ringraziamo gli utenti di Stack Overflow di cui abbiamo seguito i thread per i diversi dubbi di progettazione](https://stackoverflow.com/)

<p align="right">(<a href="#readme-top">torna in cima</a>)</p>