#!/usr/bin/env python3
"""
    implement of console file that manage all my action in this project
"""


import cmd
import shlex
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.place import Place


from models import storage
import shlex


my_models = {"BaseModel": BaseModel, "User": User,
             "Place": Place, "Amenity": Amenity,
             "Review": Review, "State": State, "City": City}


class HBNBCommand(cmd.Cmd):

    prompt = "(hbnb) "
    doc_header = """Documented commands (type help <topic>):"""

    def do_quit(self, line):
        "Quit command to exit the program"
        return True

    def do_EOF(self, line):
        "Quit command to exit the program"
        return True

    def postloop(self):
        "print new line after each command"
        print("")

    def emptyline(self):
        "over Write one empty line method"
        pass

    def do_create(self, model_name):
        "create an instance of a passed class"
        if not model_name:
            print("** class name missing **")
        elif model_name not in my_models.keys():
            print("** class doesn't exist **")
        else:
            new_instance = my_models[model_name]()
            storage.save()
            print(new_instance.id)

    def do_show(self, args=None):
        "Show the string implementation of the class"
        storage.reload()
        all_model = storage.all()
        class_name_id = shlex.split(args)
        # print(class_name_id)
        if len(class_name_id) == 0:
            print("** class name missing **")
        elif class_name_id[0] not in my_models.keys():
            print("** class doesn't exist **")
        elif len(class_name_id) < 2:
            print("** instance id missing **")
        else:
            curr_key = f"{class_name_id[0]}.{class_name_id[1]}"

            check = True
            for key in all_model.keys():
                if curr_key in key:
                    print(all_model[key])
                    check = False
                    break
            if check:
                print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name
        and id (save the change into the JSON file)."""
        storage.reload()
        all_model = storage.all()
        class_name_id = shlex.split(args)

        if len(class_name_id) == 0:
            print("** class name missing **")
        elif class_name_id[0] not in my_models.keys():
            print("** class doesn't exist **")
        elif len(class_name_id) < 2:
            print("** instance id missing **")
        else:
            key = f"{class_name_id[0]}.{class_name_id[1]}"
            check = True
            if key in all_model:
                del all_model[key]
                storage.save()
                check = False
            if check:
                print("** no instance found **")

    def do_all(self, model_name):
        storage.reload()
        models = storage.all()
        check = False

        for key in models.keys():
            if model_name in key:
                check = True
        if check:
            for key in models:
                print(models[key])
        else:
            print("** class doesn't exist **")

    def do_update(self, args):
        """Updates an instance based on the class
        name and id by adding or updating attribute"""
        storage.reload()
        all_model = storage.all()
        class_name_id = shlex.split(args)

        if len(class_name_id) == 0:
            print("** class name missing **")
        elif class_name_id[0] not in my_models.keys():
            print("** class doesn't exist **")
        elif len(class_name_id) < 2:
            print("** instance id missing **")
        else:
            curr_key = f"{class_name_id[0]}.{class_name_id[1]}"
            check = True
            for key in all_model.keys():
                if curr_key in key:
                    check = False
            if check:
                print("** no instance found **")
            elif len(class_name_id) < 3:
                print("** attribute name missing **")
            elif len(class_name_id) < 4:
                print("** value missing **")
            else:
                curr_model = all_model[curr_key]
                print(curr_model)
                if hasattr(curr_model, class_name_id[2]):
                    # making a casting to previous type.
                    previous_type = type(getattr(curr_model, class_name_id[2]))
                    setattr(curr_model, class_name_id,
                            previous_type(class_name_id[3]))
                else:
                    setattr(curr_model, class_name_id[2], class_name_id[3])
                storage.save()

    def do_count(self, args):
        storage.reload()
        all_object = storage.all()
        cnt = 0
        for obj in all_object:
            if args in obj:
                cnt += 1
        print(cnt)

    def default(self, line):
        my_com = {"all(": self.do_all, "count(": self.do_count,
                  "show(": self.do_show, "destroy(": self.do_destroy,
                  "update(": self.do_update}

        # handle input
        t_city = line.split(".")
        if len(t_city) == 2:
            curr = t_city[1][:t_city[1].find("(") + 1]
            passed = t_city[1][t_city[1].find("(") + 1: -1]
            all = f"{t_city[0]} {passed}"
            li = "update("
            if curr != li and curr in my_com.keys() and t_city[1][-1] == ")":
                my_com[curr](all.strip())
            elif curr == "update(":
                all = t_city[0]
                for i in passed:
                    if i not in [",", "\""]:
                        all += i
                    else:
                        if all[-1] != " ":
                            all += " "
                # print(shlex.split(all))
                my_com[curr](all.strip())


if __name__ == "__main__":
    HBNBCommand().cmdloop()
