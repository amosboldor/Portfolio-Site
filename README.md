# Portfolio-Site

#### Getting Started
-------------------
##### (1.) Clone repository
```user@computer:~$ git clone https://github.com/amosboldor/Portfolio-Site.git```
##### (2.) Go into directory
```user@computer:~$ cd Portfolio-Site```
##### (3.) Create virtual environment with `virtualenv`
```user@computer:~/Portfolio-Site$ virtualenv env```

-------------------
##### (4.) Activate the Enviroment

OS | Activate | Deactivate
------------ | ------------ | -------------
Windows | ```cd env\Scripts && activate && cd ../../``` | ```cd env\Scripts && deactivate && cd ../../```
Linux | ```source env/bin/activate``` | ```deactivate```
-------------------
##### (5.) Install requirements
```user@computer:~/Portfolio-Site$ pip install -r requirements.txt```
##### (6.) Run develop command
```user@computer:~/Portfolio-Site$ python setup.py develop```
##### (7.) Initialize the database
```user@computer:~/Portfolio-Site$ initialize_portfolio_db development.ini```
##### (8.) Serve
```user@computer:~/Portfolio-Site$ pserve development.ini```

-------------------
