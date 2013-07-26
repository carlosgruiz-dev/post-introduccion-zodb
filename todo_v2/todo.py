from ZODB import (DB, FileStorage)
from persistent import Persistent
import transaction
import argparse

class Task(Persistent):
    def __init__(self):
        self.name = ""
        self.description = ""


class ToDo:
    def __init__(self):
        self.store = FileStorage.FileStorage("ToDo2.fs")
        self.database = DB(self.store)
        self.connection = self.database.open()
        self.root = self.connection.root()
        if not 'Tasks' in self.root:
            self.root['Tasks'] = []
        self.tasks = self.root['Tasks']
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        transaction.get()
        transaction.abort()
        self.connection.close()
        self.database.close()
        self.store.close()
        
    def add(self, name, description):
        if name != "":
            new_task = Task()
            new_task.name = name
            new_task.description = description
            self.tasks.append(new_task)
            self.root['Tasks'] = self.tasks
            transaction.commit()
            print("New task added..")
        else:
            print("Tasks must have a name")
        
    def list(self):
        if len(self.tasks) > 0:
            print("Tasks To Do..")
            for task in self.tasks:
                print("%s\t%s" %(task.name, task.description))
        else:
            print("No pending tasks..")
            
    
    def delete(self, name):
        for i in range(len(self.tasks)):
            deleted = False
            if self.tasks[i].name == name:
                del(self.tasks[i])
                deleted = True
            if deleted:
                self.root['Tasks'] = self.tasks
                transaction.commit()
                print("Task deleted..")
            else:
                print("There is no task '%s'.." % name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', nargs=2, help="add a tast to the ToDo list")
    parser.add_argument('-d', '--delete', nargs=1, help="delete a task from the ToDo list")
    args = parser.parse_args()
    tasks = ToDo()
    if args.add:
        tasks.add(args.add[0],args.add[1])
    elif args.delete:
        tasks.delete(args.delete[0])
    else:
        tasks.list()
