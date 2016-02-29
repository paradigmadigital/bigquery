#!flask/bin/python
from app import app
app.debug = False
#app.run()
app.run(host='10.185.48.148')
