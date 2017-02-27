import os
from app01 import create_app,db
from app01.Models import User,Role,Post,Student,Class
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

app = create_app(configname='default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role,Post=Post,Student=Student,Class=Class)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()

