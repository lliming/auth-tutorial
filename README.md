# auth-tutorial
Files for a Python+Flask tutorial on using Globus Auth

auth_example.py is a simple web application based on the Flask micro-framework that logs you in via Globus Auth.
* Configure it by editing auth_example.conf. You will need to register an app client with Globus at developers.globus.org.
* Run it with the command: FLASK_APP=auth_example.py flask run

native_example.py is a simple command-line application that uses Globus Auth's native app method.
* Configure it by editing the file and entering an app client_id that you obtain by registering a native app client at developers.globus.org.
* Run it with the command: ./native_example.py
