Installing
----------------------

### Dependencies
+ Python 2.7
+ pip

### Installing dependencies
    sudo apt-get install ruby
    sudo gem install sass

### Setting up a virtualenv
    Virtualenv is not required (but it's better to use it)
    sudo pip install virtualenv
    mkdir ~/.virtualenvs/
    virtualenv ~/.virtualenvs/searcher --no-site-packages

### Configuring App
    source ~/.virtualenvs/searcher/bin/activate      # if you installed
    pip install -r requirements.txt
    cp app/localsettings.example.py app/localsettings.py

### Setting up your django environment
    ./manage.py migrate
    ./manage.py runserver

### Code style
    source ~/.virtualenvs/searcher/bin/activate      # if you installed
    pip install flake8
    git diff origin/master | flake8 --diff
