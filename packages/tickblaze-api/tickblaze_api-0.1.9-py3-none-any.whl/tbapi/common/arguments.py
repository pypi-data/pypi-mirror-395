from typing import Dict, Any

class SerializableArgument:

    def __init__(self):
        self.json_version = 1

    def encode(self) -> Dict[str, Any]:
        dictionary = { key: value for key, value in self.__dict__.items() }

        if "attribute_name" in dictionary:
            dictionary["$type"] = dictionary.pop("attribute_name")

        return dictionary