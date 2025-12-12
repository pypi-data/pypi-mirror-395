from copy import deepcopy
from xiatl.constants import SUCCEEDED, FAILED

class Macro_Signature:

    def __init__(self, items):
        self.items = items
        self.basic_signature = []
        for item in items:
            if isinstance(item, str):
                self.basic_signature.append(item)
            else:
                self.basic_signature.append("()")

    def __repr__(self):
        return f"Macro_Signature({self.items})"

    def generate_argument_dict(self):
        self.argument_dict = {}
        for item in self.items:
            if not isinstance(item, str):
                argument_list = item
                for argument in argument_list.argument_list:
                    if argument.name in self.argument_dict:
                        raise ValueError(f"Argument name '{argument.name}' is repeated.")
                    self.argument_dict[argument.name] = argument

    def assign(self, external_signature):
        if self.basic_signature != external_signature.basic_signature: 
            return None

        target_signature = deepcopy(self)

        for external_item, target_item in zip(external_signature.items, target_signature.items):
            if isinstance(external_item, str):
                continue # we're looking for argument lists not literals
            result = target_item.assign(external_item)
            if result != SUCCEEDED:
                return None

        target_signature.generate_argument_dict()
        return target_signature

class Argument_List:

    def __init__(self, argument_list):
        # assume the argument list has been validated
        self.argument_list = argument_list
        self.argument_dict = {}
        for argument in self.argument_list:
            self.argument_dict[argument.name] = argument

    def __repr__(self):
        return f"Argument_List({self.argument_list})"

    def assign(self, external_argument_list_object):

        external_argument_list = external_argument_list_object.argument_list
        target_argument_list = self.argument_list
        if len(external_argument_list) > len(target_argument_list):
            return FAILED
        
        # handle positional arguments
        keyword_arguments_initial_index = None
        for i, external_argument in enumerate(external_argument_list):
            if external_argument.name is not None:
                keyword_arguments_initial_index = i
                break
            else:
                target_argument_list[i].value = external_argument.value

        # if there are no keyword arguments, check if we are done
        if keyword_arguments_initial_index is None:
            for target_argument in target_argument_list:
                if target_argument.value is None:
                    return FAILED
            return SUCCEEDED

        remaining_external_arguments = external_argument_list[keyword_arguments_initial_index:]
        remaining_target_arguments = target_argument_list[keyword_arguments_initial_index:]
        remaining_target_argument_dict = {}
        for target_argument in remaining_target_arguments:
            remaining_target_argument_dict[target_argument.name] = target_argument

        already_assigned = set()
        for external_argument in remaining_external_arguments:
            if external_argument.name not in remaining_target_argument_dict:
                return FAILED
            elif external_argument.name in already_assigned:
                return FAILED
            else:
                remaining_target_argument_dict[external_argument.name].value = external_argument.value
                already_assigned.add(external_argument.name)

        for target_argument in target_argument_list:
            if target_argument.value is None:
                return FAILED
        return SUCCEEDED

class Argument:
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Argument(name={self.name},value={self.value})"
