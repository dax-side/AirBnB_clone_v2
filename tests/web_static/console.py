#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from shlex import split


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(hbnb) "

    __classes = {
               'BaseModel',
               'User',
               'Place',
               'State',
               'City',
               'Amenity',
               'Review'
              }

    def emptyline(self):
        """ Ignores empty spaces"""
        pass

    def do_quit(self, line):
        """ Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """ Quit command to exit program at EOF """
        return True

    def do_create(self, line):
        """ Create a new class with the given keys/values and print its id.
            Usage: create <class> <key>=<value> <key>=<value> ...
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for pair in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
                print(obj.id)
                obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """ Prints string representation of an object
            Execeptions:
                SyntaxError: When no args are given
                NameError: When no object with name exists
                IndexError: When no id is given
                KeyError: When wrong id is given
        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroys a specified object
        Exceptions:
            NameError: when there is no object with the name
            SyntaxError: when there are no args given
            IndexError: when ther is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def count(self, line):
        """count the number of instances of a class"""
        counter = 0
        try:
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and returns a string of command
        Args:
            args: input list of args
        Return:
            returns string of arguments
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                    args[1][args[1].find('{').args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        """ retrieve all instance of a class and
            retrieve the number of instances
        """
        my_list = line.split('.')
        if len(my_list) >= 2:
            if my_list[1] == "all()":
                self.do_all(my_list[0])
            elif my_list[1] == "count()":
                self.count(my_list[0])
            elif my_list[1][:4] == "show":
                self.do_show(self.strip_clean(my_list))
            elif my_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(my_list))
            elif my_list[1][:6] == "update":
                args = self.strip_clean(my_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)

    def do_all(self, line):
        """ Shows string representations of all instances
            of a given class. If no class specified display all
            instatiated objects.
        """
        if not line:
            ob = storage.all()
            print([ob[k].__str__() for k in ob])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            ob = storage.all(args[0])
            print([ob[k].__str__() for k in ob])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """ Updates an instance by addin or updating attribute"""
        try:
            if not line:
                raise SyntaxError()
            my_list = split(line, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + mylist[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                v.__dict__[my_list[2]] = my_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing**")
        except ValueError:
            print("** value missing**")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
