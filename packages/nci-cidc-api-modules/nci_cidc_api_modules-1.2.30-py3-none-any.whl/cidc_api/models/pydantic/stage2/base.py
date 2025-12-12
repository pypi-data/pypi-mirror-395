from pydantic import BaseModel, ConfigDict
from contextlib import contextmanager

import copy


class Base(BaseModel):

    model_config = ConfigDict(validate_assignment=True, from_attributes=True)

    # Validates the new state and updates the object if valid
    def update(self, **kwargs):
        self.model_validate(self.__dict__ | kwargs)
        self.__dict__.update(kwargs)

    # CM that delays validation until all fields are applied.
    # If validation fails the original fields are restored and the ValidationError is raised.
    @contextmanager
    def delay_validation(self):
        original_dict = copy.deepcopy(self.__dict__)
        self.model_config["validate_assignment"] = False
        try:
            yield
        finally:
            self.model_config["validate_assignment"] = True
        try:
            self.model_validate(self.__dict__)
        except:
            self.__dict__.update(original_dict)
            raise

    @classmethod
    def split_list(cls, val):
        """Listify fields that are multi-valued in input data, e.g. 'lung|kidney'"""
        if type(val) == list:
            return val
        elif type(val) == str:
            if not val:
                return []
            return val.split("|")
        else:
            raise ValueError("Field value must be string or list")
