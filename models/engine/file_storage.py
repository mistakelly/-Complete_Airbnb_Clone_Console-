from os import path
print("just before importing BaseModel in the Filestorage")
from models.base_model import BaseModel
print("after importing basemodel, now to User")
from models.user import User
print("after importing user")
import json


class FileStorage:
    ALL_CLASSES = {
        'BaseModel': BaseModel,
        'User': User
    }
    __objects = {}
    __filepath = 'file.json'

    def new(self, obj) -> None:
        print("inside new")
        """
            this adding New Object to file storage.
        """
        # construct key
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def all(self) -> dict:
        """
            this method is responsible for returning the whole
            object in the file __objects dictionary.
        """
        return self.__objects

    def save_obj(self) -> None:
        """
            for converting the python objects into python dictionary,
            so they can be stored into the file storage,this process is called
            serialization.
        """

        # declare dictionary.
        serialized_obj = {}

        for k, v in self.__objects.items():
            # call the to_dict method in the basemodel
            # to represent every object to dict.
            serialized_obj[k] = v.to_dict()

        # dump into file storage
        with open(self.__filepath, "w") as obj_dic:
            json.dump(serialized_obj, obj_dic, indent=2)
        print("before leaving save_obj")

    def reload(self) -> None:
        """
            responsible for reloading the object in file storage and
            dynamically create objects out of the data in the file storage
        """

        # open file
        # split the key of the dictionary
        # dynamically create classes base on the class name.
        if path.exists(self.__filepath) and path.getsize(self.__filepath) > 0:
            with open(self.__filepath, "r") as db:

                file_content = json.load(db)

                for k, v in file_content.items():

                    # split the dictionary key
                    cls_name, cls_key = k.split('.')

                    # dynamically create the class object again according to the entry in db.

                    # same as doing.
                    global_class = self.ALL_CLASSES[cls_name]
                    print(global_class)

                    result = global_class(**v)

                    self.__objects[k] = result


print("last last in the filestorage")
