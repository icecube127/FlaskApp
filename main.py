from venv import create
from website import create_app
from flask import Flask

#hope this
app = create_app()

if __name__ == '__main__':
    app.run()