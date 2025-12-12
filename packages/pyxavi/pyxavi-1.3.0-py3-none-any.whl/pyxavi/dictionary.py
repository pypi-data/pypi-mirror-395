from __future__ import annotations
from slugify import slugify
import copy

PATH_SEPARATOR_CHAR = "."
LIST_HORIZONTAL_RESOLVING_CHAR = "#"


class Dictionary:
    """Class to handle simple dictionary-based storage

    The value contribution for this class is the ability to
        reference the keys on the tree by paths like:
        "root_object.child_1.child_2.child_3"

    It includes the basic common API
    - get
    - get_all
    - set
    - delete
    - key_exists

    Plus some extra
    - get_keys
    - get_parent
    - get_parent_path
    - get_last_key
    - to_dict
    - merge
    - initialize_recursive
    - resolve_wildcards
    - needs_resolving


    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """

    def __init__(self, content: dict = {}, path_separator_char=None) -> None:
        self._content = content
        self._separator = path_separator_char\
            if path_separator_char is not None else PATH_SEPARATOR_CHAR

    def _is_int(self, element: str) -> bool:
        """Check if the given element is an integer without converting it"""
        if element[0] in ('-', '+'):
            return element[1:].isdecimal()
        return element.isdecimal()

    def get(
        self, param_name: str = "", default_value: any = None, slugify_param_name=False
    ) -> any:
        """
        Returns the value found in the given param_name path,
        otherwise default_value is returned

        Accepts wildcards for the list indexes.
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        if Dictionary.needs_resolving(param_name=param_name):
            return self._get_horizontally(param_name=param_name, default_value=default_value)

        if param_name.find(self._separator) > 0:
            # bring it local so we can play with it
            local_content = self._content
            for item in param_name.split(self._separator):

                if self._is_int(item):
                    # It's an int, so it's meant to be the key of a list
                    item = int(item)

                    if isinstance(local_content, list) and\
                       item < len(local_content) and\
                       local_content[item] is not None:
                        # If exists and is not None we keep digging
                        local_content = local_content[item]
                    else:
                        # Otherwise we just return the default value
                        return default_value
                else:
                    if item in local_content and local_content[item] is not None:
                        # If exists and is not None we keep digging
                        local_content = local_content[item]
                    else:
                        # Otherwise we just return the default value
                        return default_value

            # When reaching the end of the path, we return the value at this point
            return local_content

        # In the case of a single item param_name, get directly from the content.
        return self._content[param_name] \
            if self._content and param_name in self._content \
            else default_value

    def get_all(self) -> dict:
        """Returns the whole internal dictionary"""
        return self._content

    def _is_out_of_range(self, index: int, list_to_check: list) -> bool:
        """Checks if the given index is out of range for the given list"""
        try:
            list_to_check[index]
            return False
        except IndexError:
            return True

    def __recursive_set(self, param_name: str, value: any, dictionary: any = None) -> None:
        """
        Recursively walks through the dictionary to find the key to set, and sets it

        Raises a RuntimeError if any of the keys in the param_name does not exist
        Raises a ValueError if a key from the param_name is an index but the parent is
            not a list.
        """
        if param_name.find(self._separator) > 0:
            pieces = param_name.split(self._separator)
            if self._is_int(pieces[0]):
                item = int(pieces[0])

                # The dictionary argument must be a list. Complain otherwise.
                if not isinstance(dictionary, list):
                    raise ValueError(
                        f"With the key [{param_name}] I expect the parent to be a list," +
                        f" but its [{type(dictionary)}]"
                    )

                if item < len(dictionary) and dictionary[item] is not None:
                    self.__recursive_set(
                        param_name=self._separator.join(pieces[1:]),
                        value=value,
                        dictionary=dictionary[item]
                    )
                else:
                    raise RuntimeError(
                        f"Dictionary path [{item}] is out of bounds for [{dictionary}]"
                    )
            elif isinstance(dictionary, dict):
                # The dictionary argument is a dict

                # Now, the key may not exists.
                if pieces[0] not in dictionary:
                    # This is a set(), if the key doesn't exist, we create it as an empty dict
                    # This should solve the issue of setting into non-existing root paths
                    dictionary[pieces[0]] = {}

                # if pieces[0] not in dictionary:
                #     raise RuntimeError(
                #         f"Dictionary key [{pieces[0]}] is unknown in [{dictionary}]"
                #     )

                self.__recursive_set(
                    param_name=self._separator.join(pieces[1:]),
                    value=value,
                    dictionary=dictionary[pieces[0]]
                )
            else:
                # The dictionary argument is anything but a list or a dict
                raise RuntimeError(f"Dictionary path [{param_name}] unknown in [{dictionary}]")
        else:
            if self._is_int(param_name):
                # It's an int, so it's meant to be the key of a list
                param_name = int(param_name)

                # The dictionary must be a list. Complain otherwise.
                if not isinstance(dictionary, list):
                    raise ValueError(
                        f"With the key [{param_name}] I expect the parent to be a list," +
                        f" but its [{type(dictionary)}]"
                    )

                if param_name < len(dictionary):
                    # Normal set. Possibly an overwrite.
                    dictionary[param_name] = value
                else:
                    # So it is an append or a set out of bounds
                    #   Let's fill with None until the desired index
                    for idx in range(0, param_name + 1):
                        if not self._is_out_of_range(idx, dictionary):
                            continue
                        else:
                            dictionary.append(value if idx == param_name else None)
            else:
                if dictionary is not None:
                    dictionary[param_name] = value
                else:
                    dictionary = {param_name: value}

    def set(self, param_name: str, value: any = None, slugify_param_name=False) -> None:
        """
        Sets the given value into the given param_name path.

        If the final key's parent does not exist, it sets it new
        If the final key's parent exists and is a dict, it adds a new key with the value
        If the final key's parent exists and is not a dict, overwrites it with a dict
            consisting of the new key with the value

        Raises a RuntimeError if any of the keys in the param_name does not exist
        Raises a ValueError if a key from the param_name is an index but the parent is
            not a list.

        Accepts wildcards for the list indexes.
        """
        if param_name is None:
            raise RuntimeError("Params must have a name")

        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        if Dictionary.needs_resolving(param_name=param_name):
            return self._set_horizontally(param_name=param_name, value=value)

        self.__recursive_set(param_name=param_name, value=value, dictionary=self._content)

    def key_exists(self, param_name: str, slugify_param_name=False) -> bool:
        """
        Checks if the given param_name path exists,
        including the indexes inside the list ranges
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        key_to_search = self.get_last_key(param_name=param_name)
        parent_object = self.get_parent(param_name)

        if parent_object is None:
            return False

        if isinstance(parent_object, list) and self._is_int(key_to_search):
            if self._is_out_of_range(int(key_to_search), parent_object):
                return False
            else:
                return True

        if isinstance(parent_object, dict):
            return True if key_to_search in parent_object else False

        return False

    def get_last_key(self, param_name: str, slugify_param_name=False) -> str:
        """
        Returns the last key of the param_name
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        return param_name.split(self._separator)[-1]\
            if param_name.find(self._separator) > 0 else param_name

    def get_parent_path(self, param_name: str, slugify_param_name=False) -> str:
        """
        Returns the all the path without the last key of the param_name
        """
        if slugify_param_name:
            param_name = ".".join([slugify(part) for part in param_name.split(".")])

        return self._separator.join(param_name.split(self._separator)[:-1])\
            if param_name.find(self._separator) > 0 else None

    def get_parent(self, param_name: str, slugify_param_name=False) -> dict:
        """
        Returns the parent object of the given param_name path

        Accepts wildcards for the list indexes.
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        if Dictionary.needs_resolving(param_name=param_name):
            return self._get_parent_horizontally(param_name=param_name)

        if param_name.find(self._separator) > 0:
            pieces = param_name.split(self._separator)
            parent_key = self._separator.join(pieces[:-1])
            return self.get(param_name=parent_key, default_value=None)
        else:
            return self._content

    def delete(self, param_name: str, slugify_param_name=False) -> None:
        """
        Deletes the given param_name path key
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        if self.key_exists(param_name=param_name):
            parent = self.get_parent(param_name=param_name)
            key_to_delete = self.get_last_key(param_name=param_name)

            if isinstance(parent, list) and self._is_int(key_to_delete):
                key_to_delete = int(key_to_delete)

            del parent[key_to_delete]
            return True
        else:
            return False

    def initialise_recursive(self, param_name: str, slugify_param_name=False) -> None:
        """
        Walks through the given param_name path and creates all missing keys and dicts.

        Raises RuntimeError if a key of the param_name path already exists and it's not
            a dictionary or a list (whatever expected), to avoid overwriting.
        """

        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        pieces = param_name.split(self._separator)
        parent_path = ""
        # We start assuming that self._content is already {}
        for piece in pieces:
            path = f"{parent_path}{piece}"
            if not self.key_exists(path):
                parent = self.get_parent(path)
                if (isinstance(parent, dict) and not self._is_int(piece)) or\
                   (isinstance(parent, list) and self._is_int(piece)):
                    self.set(path, {})
                else:
                    # We can't create children on non-dict/non-list values,
                    #   and we won't overwrite current values
                    # This only applies to keysthat are in the middle of the path
                    #   as we're expected to go deep and we actually can't.
                    raise RuntimeError(
                        f"The key {parent_path[:-1]} " +
                        "already exists as a non-dict or non-list. " + "I won't overwrite."
                    )

            parent_path = f"{path}{self._separator}"

    def get_keys_in(self, param_name: str = None, slugify_param_name=False) -> list:
        """Returns the keys on the given param_name path dict"""
        if param_name is not None:
            param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)
            obj = self.get(param_name=param_name)
        else:
            obj = self._content

        if isinstance(obj, dict):
            return [key for key in obj.keys()]
        if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            return [key for key in range(len(obj))]
        else:
            return None

    def to_dict(self) -> dict:
        """Shortcut to get_all()"""
        return self.get_all()

    def merge(
        self, origin: Dictionary, param_name: str = None, slugify_param_name=False
    ) -> None:
        """
        Takes a given Dictionary object and merges it into the current object
            as the given param_name (or at root if None given)

        If the given param_name already exists in the current object,
            - It will be merged if it's a dict
            - It will be added if it's a list
            - It will be overwritten otherwise

        Raises a RuntimeError if any of the keys in the param_name does not exist
        """
        if param_name is None:
            # self._content = {**self._content, **origin.get_all()}
            self._content = Dictionary._merge_complex_recursive(self._content, origin.get_all())
        else:
            param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

            if not self.key_exists(param_name=param_name):
                raise RuntimeError(f"Dictionary path [{param_name}] unknown")

            current_value = self.get(param_name=param_name, default_value={})
            if isinstance(current_value, dict):
                # self.set(param_name=param_name, value={**current_value, **origin.get_all()})
                self.set(
                    param_name=param_name,
                    value=Dictionary._merge_complex_recursive(current_value, origin.get_all())
                )
            elif isinstance(current_value, list):
                current_value.append(origin.get_all())
                self.set(param_name=param_name, value=current_value)
            else:
                self.set(param_name=param_name, value=origin.get_all())

    @staticmethod
    def _merge_simple_recursive(base_dict: dict, over_dict: dict) -> dict:
        for key, value in over_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value,
                                                                                    dict):
                base_dict[key] = Dictionary._merge_simple_recursive(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    @staticmethod
    def _merge_complex_recursive(base_dict: dict, over_dict: dict) -> dict:
        merged_dict = {}
        for key in set(base_dict) | set(over_dict):
            if key in base_dict and key in over_dict:
                if isinstance(base_dict[key], list) and isinstance(over_dict[key], list):
                    merged_dict[key] = base_dict[key] + over_dict[key]
                elif isinstance(base_dict[key], dict) and isinstance(over_dict[key], dict):
                    merged_dict[key] = Dictionary._merge_simple_recursive(
                        copy.deepcopy(base_dict[key]), over_dict[key]
                    )
                else:
                    merged_dict[key] = over_dict[key]
            elif key in base_dict:
                merged_dict[key] = copy.deepcopy(base_dict[key])
            else:
                merged_dict[key] = copy.deepcopy(over_dict[key])
        return merged_dict

    def remove_none(self) -> None:
        self._content = self._remove_none_recursive(self._content)

    def _remove_none_recursive(self, _dict: dict) -> dict:
        """Delete None values recursively from all of the dictionaries, tuples, lists, sets"""
        if isinstance(_dict, dict):
            for key, value in list(_dict.items()):
                if isinstance(value, (list, dict, tuple, set)):
                    _dict[key] = self._remove_none_recursive(value)
                elif value is None or key is None:
                    del _dict[key]

        elif isinstance(_dict, (list, set, tuple)):
            _dict = type(_dict)(
                self._remove_none_recursive(item) for item in _dict if item is not None
            )

        return _dict

    @staticmethod
    def needs_resolving(param_name: str) -> bool:
        """Checks if the param_name path indicates horizontal resoliving"""
        return True if param_name.find(LIST_HORIZONTAL_RESOLVING_CHAR) > -1 else False

    def resolve_wildcards(self, param_name: str = "", slugify_param_name: bool = False) -> list:
        """
        Resolves param_name paths with '#' wildcards

        Returns a list of all resolved paths.
        Non matching paths are ignored.
        """
        param_name = self._slugify_param_name_if_needed(param_name, slugify_param_name)

        # do we actually need to do anything?
        if not Dictionary.needs_resolving(param_name):
            return [param_name]

        # Initialise what we'll return
        returning_stack = []

        # Get the portions between the '#' and clean them (to avoid starting or ending with ".")
        portions = param_name.split(LIST_HORIZONTAL_RESOLVING_CHAR)
        portions = [
            portion.removeprefix(PATH_SEPARATOR_CHAR).removesuffix(PATH_SEPARATOR_CHAR)
            for portion in portions
        ]

        # Now just strip and return the first one
        portion = portions.pop(0)
        keys_in_portion = self.get_keys_in(portion)

        # Now check the keys in portion.
        #   If none here, simply the param_name is wrong
        if keys_in_portion is None:
            return []

        # And walk through all iterations in that list.
        #   Because it MUST be a list
        for key in keys_in_portion:
            path = f"{portion}{PATH_SEPARATOR_CHAR}{key}"

            portions_path = f"{PATH_SEPARATOR_CHAR}"
            portions_path = f"{portions_path}{LIST_HORIZONTAL_RESOLVING_CHAR}"
            portions_path = f"{portions_path}{PATH_SEPARATOR_CHAR}"
            portions_path = portions_path.join(portions)
            if portions_path:
                path = f"{path}{PATH_SEPARATOR_CHAR}{portions_path}"

            if Dictionary.needs_resolving(path):
                # We still have more "#", go deeper.
                returning_stack = returning_stack + self.resolve_wildcards(param_name=path)
            else:
                # No more "#"
                if self.key_exists(path):
                    # just return the value of the whole path only if the key exists
                    returning_stack.append(path)

        # And finally we return all paths that we resolved in this iteration.
        return returning_stack

    def _get_horizontally(self, param_name: str = "", default_value: any = None) -> list:
        """
        Gets the values of all the possible paths
            horizontally across the defined lists iterations

        It will ignore non-existing or not matching param_name path portions.
        """
        all_param_names = self.resolve_wildcards(param_name=param_name)

        returning_stack = []
        for path in all_param_names:
            returning_stack.append(self.get(param_name=path, default_value=default_value))

        return returning_stack

    def _set_horizontally(self, param_name: str, value: any = None):
        """
        Sets the values of all the possible paths
            horizontally across the defined lists iterations

        It will ignore non-existing or not matching param_name path portions.
        """
        all_param_names = self.resolve_wildcards(param_name=param_name)

        for path in all_param_names:
            self.set(param_name=path, value=value)

    def _get_parent_horizontally(self, param_name: str = "", default_value: any = None) -> list:
        """
        Gets the values of all the possible paths
            horizontally across the defined lists iterations

        It will ignore non-existing or not matching param_name path portions.
        """
        all_param_names = self.resolve_wildcards(param_name=param_name)

        returning_stack = []
        for path in all_param_names:
            returning_stack.append(self.get_parent(param_name=path))

        return returning_stack

    def _slugify_param_name_if_needed(
        self, param_name: str, slugify_param_name: bool = False
    ) -> str:
        """
        Slugifies all the parts from the parameter name.

        The slugify respects dots as separators for nested keys.
        It also respects "#" as horizontal list resolving characters.
        """
        if not slugify_param_name:
            return param_name

        if not Dictionary.needs_resolving(param_name):
            return self._separator.join(
                [slugify(part) for part in param_name.split(self._separator)]
            )

        # We have horizontal resolving chars, so we need to respect them
        portions = param_name.split(LIST_HORIZONTAL_RESOLVING_CHAR)
        portions = [
            self._separator.join([slugify(part) for part in portion.split(self._separator)])
            for portion in portions
        ]
        return LIST_HORIZONTAL_RESOLVING_CHAR.join(portions)
