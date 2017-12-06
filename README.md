# auth-tutorial
These are some simple (but thoroughly commented!) examples of using Globus Auth. They were developed for use in Globus Auth tutorials.

auth_example.py is a simple web application based on the Flask micro-framework that logs you in via Globus Auth.
* Configure it by editing ``auth_example.conf``. You will need to register an app client with Globus at https://developers.globus.org.
* You can use the built-in HTTPS server certificate (in the keys subdirectory) or replace with your own. If you use the built-in certificate, your browser will complain about the connection not being secure. Bypass this warning to use the application. (The connection IS secure, it's just that the server you're running can't prove its identity. But you know who it is. ;) )
* Start the application on the command line with the command: ``./auth_example.py``
* Connect to the application in your Web browser at https://hostname:5000/ (note use of https!)

native_example.py is a Python command-line script that uses Globus Auth's native app method.
* You can run the script without configuration if you are happy with using the built-in app registration. The built-in registration uses a CLIENT_ID that I generated myself at developers.globus.org. *I plan to keep this registration active, but if I ever deactivate it, the CLIENT_ID will no longer work and you'll need to replace it with your own.*
* You can obtain your own CLIENT_ID by registering a native app client at https://developers.globus.org. If you do this, edit the script file and replace the CLIENT_ID= line with the ID you obtain from Globus.
* Run the script on the command line with the command: ``./native_example.py``
