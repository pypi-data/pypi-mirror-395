Assignment 2 - Gruppo I processati
Group Members: Carpio Herreros Marco (matricola 899802), Cattaneo Francesco (matricola 900411)

Questa repository contiene la pipeline per l'applicazione Flask **Blog**.

# Descrizione app
Questa descrizione è presa direttamente dalla repository originale dell'app Python: https://github.com/yathishgowdaa/Blog
## FlaskApp

Simple Blog application with authentication and CRUD functionality using the Python Flask micro-framework where user can login post an article, edit the posted article and delete the article. User can read other articles posted by other users as well but not edit or delete.

### Installation

To use this template, your computer needs:

- [Python 2 or 3](https://python.org)
- [Pip Package Manager](https://pypi.python.org/pypi)

### Running the app

```bash
python app.py
```
# Struttura della pipeline
La pipeline è divisa negli *stages* elencati qua sotto.

## Build
Lo stage **Build** ha un solo job chiamato `build-job`. Abbiamo deciso di usare l'ambiente di lavoro virtuale di Python `venv` per separare tutti i file Python dal resto dell'app in maniera efficace. Inoltre, grazie a `venv`, si è reso più facile impostare la dipendenza degli altri job sull'ambiente creato in questo job.

In `requirements.txt`, il file che elenca tutte el dipendenze da installare all'interno di `venv` in questo job, vengono elencate sia tutte le dipendenze dell'app, sia tutte le dipendenze della pipeline (es. Prospector, Bandit, Twine, etc). Abbiamo fatto così per mantenere la struttura della pipeline più pulita, e dover installare tutte le dipendenze una volta sola durante la pipeline.

## Verify
L'obiettivo di questo stage è di controllare lo stile del codice, e per assicurarsi che il codice segua standard di qualità conformi. Usiamo tre diversi job, che vengono eseguiti in parallelo, per effettuare questo controllo.

### prospector
Questo job si occupa di eseguire `Prospector`, uno strumento che controlla lo stile e formattazione, la qualità del codice, ed errori potenziali o di design.

Abbiamo configurato Prospector in modo che ignori le cartelle relative a `venv` e alla cache, poichè sporcano i risultati dell'analisi con dati non affini al nostro lavoro. La configurazione di Prospector è inserita all'interno del file `.prospector.yml`.

Questo job produce come artefatto il file `prospector-report.txt`; anche se questo conterrà errori, la pipeline continuerà ad andare poichè sono errori di stile che non appartengono a una parte di codice scritta da noi.

### bandit
Questo job si occupa di eseguire `Bandit`, uno strumento che cerca vulnerabilità di sicurezza nel codice. 

Abbiamo configurato Bandit in modo che ignori le cartelle relative a `venv` e alla cache, sempre per lo stesso motivo. La configurazione di Bandit è inserita all'interno del file `.bandit.yaml`.

Questo job produce come artefatto il file `bandit-report.html`; come nel job `prospector`, anche se verranno visualizzati degli errori, questi non verranno corretti poichè non appartengono a una parte di codice scritta da noi.

### wapiti
Questo job si occupa di eseguire `Wapiti`, uno strumento di sicurezza che scansiona l'app mentre è in esecuzione, cercando vuknerabilità accessibili via HTTP.

Per poter fare questa analisi è necessario eseguire l'app python; forniamo dunque nel job le variabili segrete per poter inizializzare il database.

Questo job produce come artefatto il file `wapiti-report.html`; se si manifestano errori di vulnerabilità la pipeline continuerà come nei due job precedenti.

## Test
L'obiettivo di questo stage è di verificare il funzionamento corretto delle singole funzionalità CRUD dell'app. Sono state dunque verificate le seguenti funzionalità e nel seguente modo.

I test sono inclusi nel file `unit_testApp.py`

## Integration Test
L'obiettivo di questo stage è di verificare il funzionamento corretto delle singole funzionalità CRUD dell'app. I test sono inclusi nel file `testApp.py`.

Per ogni test che richiede un articolo, abbiamo fatto in modo che la lunghezza del *body* fosse almeno di 30 caratteri, il minimo consentito dall'applicazione Flask. Abbiamo deciso di usare `mock_mysql` nei test per non dipendere da un database vero e proprio. Questo ha reso comunque la verifica dell'esecuzione delle chiamate SQL dall'app più semplice.

## Package
Nello stage Package, viene creato un pacchetto installabile dell'applicazione. 
Questo pacchetto viene creato secondo le specifiche che abbiamo inserito in `setup.py`. Questo file specifica dati del pacchetto (nome, versione, autori, etc), e le dipendenze necessarie.
In questa fase, vengono creati all'interno della cartella `dist/` due file:
- Un pacchetto sorgente che contiene il codice sorgente ed altri file necessari; i file che devono essere inclusi sono specificati nel file `MANIFEST.in`
- Un pacchetto `wheel` che contiene il codice pre-impacchettato

Creiamo anche il pacchetto sorgente perchè PyPI consiglia di caricare entrambi sul proprio sito, così che se la Wheel non è compatibile con una piattaforma, allora verrà usato il pacchetto sorgente come fallback.

## Release
Nello stage Release, rendiamo disponibile il pacchetto sul Python Package Index (PyPI), per renderlo installabile tramite `pip`. Per farlo, abbiamo creato un account su PyPI, e inserito su GitLab come variabili segrete l'username e token di accesso per `twine`. 
Carichiamo ciò che è all'interno della cartella `dist/` tramite `twine`.

## Docs
Nello stage Docs, rendiamo disponibile la documentazione dell'applicazione al sito [GitLab Pages]{https://2025-assignment2-blog-2864c8.gitlab.io/}. Questo viene effettuato tramite lo strumento `mkdocs`; lo stage crea un artefatto che contiene un sito web contenente tutta la documentazione.
Visto che volevamo aggiungere il README.md del progetto nella documentazione, ma `mkdocs` può aggiungere i file presenti soltanto nella cartella `docs/`, durante il job copiamo il file dalla root della repository alla cartella `docs/`, per poi essere aggiunto all'interno della documentazione. 