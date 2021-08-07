# Purple
## Ecommerce Website for Gifts

### Create virualenv
    pip3 install virtualenv 
    virtualenv venv 
### Activate virtualenv
    source venv/bin/activate
### set up databases
    python3 manage.py makemigrations
    python3 manage.py migrate
### add Product details to database
goto Account/generate.py and copy all lines(ctrl+a & ctrl+c)
goto Account/views.py and paste copied code on line 20
    python3 manage.py runserver
look at terminal to see Product names ,when completed,delete copied code from Account/views.py and save(or Ctrl+z & save)
