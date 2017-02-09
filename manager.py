# -*- coding:utf-8 -*-
# __author__ = 'dayinfinte'

import os
from app import create_app, db
from app.models import User, POST
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_markdown import Markdown 

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
markdown = Markdown(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, POST=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='127.0.0.1', port=5000, user_debugger=True))

#@manager.command
#def test():
#    import unittest
#    tests=unittest.TestLoader().discover('tests')
#    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
