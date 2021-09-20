# AddMeToMySQL

## Usage
This is a simple python script to add the data from your *csv* file to a table in MySQL database.

## Instructions

* get a copy of this folder on your local machine;
* go to `config.py` file and change the database settings to your credentials:
```python
DB_SETTINGS = {
    "host": "your_host_name",
    "user": "your_user_name",
    "password": "your_password",
    "db": "your_database_name",
    "table_name": "your_table_name"
}
```
* run addMeToMySQL.py file with providing as an argument the path to your csv data file name:

```bash
$ python addMeToMySQL.py ~/path/to/yourData.csv
```


## Requirements
* Python 3.9 or upper
* Installed packages from `requirements.txt` file. In case if you don't have them you can run:
```bash
$ pip install -r requirements.txt 
```
* You need to have a database and table already created (if you need to 
create one, as an example there is a database model file *(db_model.mwb)* which you can use to generate database and table);
* The data inside csv file should be axactly in the following formats:
  * Date (1 column): date in the format: dd/mm/yy;
  * Ad Unit Name (2 column): string no more than 20 charcters;
  * Ad Unit ID, Typetag (3-4 columns): integers;
  * Revenue Source (5 column): string no more than 10 characters;
  * Market (6 column): string no more than 20 charcters;
  * Queries, Clicks, Impressions (7-9 columns): integers;
  * Page Rpm, Impression Rpm, True Revenue (10-12 columns): integer or decimal no greater than 9999999,9999 with 4 digits after comma;
  * Coverage (13 column): integer or decimal no bigger than 999,99 with 2 digits after comma;
  * Ctr (14 column): integer or decimal no bigger than 9,999999 with 6 digits after comma.

### Cosa avrei fatto in modo migliore se avessi avuto più tempo a disposizione:
#### the question in the task
* Avrei cercato di capire lo scopo principale che mi avrebbe aiutato a capire le possibilità di cancellare alcune condizioni.
Per esempio:
  * si potrebbe cancellare la prima riga dal file csv (headers)? così potremmo cancellare un ciclo 'if':
  ```python
    if line_count == 0:
        line_count += 1
    else:
        ...
    ```
  * si potrebbe cancellare le righe vuote da file csv? così avrei potuto cancellare anche la seconda condizione:
  ```python
    if row[0]=="":
        pass
    else:
        ...
  ```
  evitare le condizioni ci permetterebbe salvare tempo se abbiamo i dati enormi. 
* se ci serve, si potrebbe usare per esempio SQLAlchemy e aggiungere le tabelle direttamente dal codice, se non esiste.
Ma questo è utile in una applicazione particolare forse. Non credo che sia best practice dare il permesso di modifiche database all'utente.
Quindi ho usato pyMySQL con una semplice execute.