# -*- coding: utf-8 -*-

from ZODB import (DB, FileStorage)
import transaction
import argparse

class ToDo:
    def __init__(self):
        self.store = FileStorage.FileStorage("ToDo.fs")
        self.database = DB(self.store)
        self.connection = self.database.open()
        self.root = self.connection.root()
    
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        transaction.get()
        transaction.abort()
        self.connection.close()
        self.database.close()
        self.store.close()
        
    def add(self, key, value):
        if key != "":
            self.root[key] = value
            transaction.commit()
            print("New task added..")
        else:
            print("A task must have a name")
        
    def list(self):
        print("Tasks To Do..")
        for k in self.root.keys():
            print("%s\t%s" % (k, self.root[k]))
            
    
    def delete(self, key):
        if key in self.root.keys():
            del(self.root[key])
            transaction.commit()
            print("Task deleted..")
        else:
            print("There is no task '%s'.." % key)


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