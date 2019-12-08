"""
Sample wsgi file for deploying with apache mod_wsgi

You only need to change the first two lines, the values of secret_key and activate_this

You need to create the virtual environment using 'virtualenv' rather than 'python3 -m venv'
otherwise you don't get an activate_this.py file
"""

# complex random key used by cryptographic components to sign cookies and other things
secret_key = 'my secret'

# method provided by virtualenv to activate a virtual environment while python is running
activate_this = '/usr/local/venvs/bpss-prime-minister/bin/activate_this.py'

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# import the application creation factory method
from prime_minister import create_app

# create the application using the factory method and crytographic key
app = create_app({'SECRET_KEY': secret_key})

# wsgi needs to return an object called application. This can be either app or app.wsgi_app
# app.wsgi_app is a more recent suggestion which doesn't lose reference to app when middle ware used
application = app.wsgi_app
