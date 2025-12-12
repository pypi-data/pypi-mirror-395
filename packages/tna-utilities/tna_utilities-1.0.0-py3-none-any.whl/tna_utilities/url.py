from urllib.parse import urlencode


class QueryStringTransformer:
    """
    A utility class to manipulate query strings.

    Args:
        args: An object representing the query parameters, typically an
              ImmutableMultiDict (Django) or QueryDict (Flask) which can be
              accessed with request.GET (Django) or request.args (Flask).
    """

    def __init__(self, args):
        try:
            args_lists = args.lists()
        except AttributeError:
            raise TypeError(
                "args must be a ImmutableMultiDict (Django) or QueryDict (Flask) object"
            )
        self.args = list(args_lists)

    def parameter_exists(self, parameter):
        """
        Check if a parameter exists in the query parameters.
        """

        return parameter in dict(self.args)

    def parameter_values(self, parameter):
        """
        Get the values associated with a parameter in the query parameters.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                return values
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def add_parameter(self, parameter, values=None):
        """
        Add a new parameter to the query parameters.
        Raises a ValueError if the parameter already exists.
        """

        for key, vals in self.args:
            if key == parameter:
                raise ValueError(f"Parameter '{parameter}' already exists")
        if type(values) is not list:
            values = [str(values)] if values is not None else []
        else:
            values = [str(v) for v in values]
        self.args.append((parameter, values))

    def update_parameter(self, parameter, values=None):
        """
        Update an existing parameter in the query parameters.
        If the parameter does not exist, it will be added.
        """

        try:
            self.remove_parameter(parameter)
        except AttributeError:
            pass
        self.add_parameter(parameter, values)

    def remove_parameter(self, parameter):
        """
        Remove a parameter from the query parameters.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, vals in self.args:
            if key == parameter:
                self.args.remove((key, vals))
                return
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def is_value_in_parameter(self, parameter, value):
        """
        Check if a specific value exists within a parameter's values.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                return value in values
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def add_parameter_value(self, parameter, value):
        """
        Add a specific value to a parameter's values.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if value not in values:
                    values.append(value)
                return
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def toggle_parameter_value(self, parameter, value):
        """
        Toggle a value within a parameter's values.
        If the value exists, it will be removed; if it does not exist, it will be added.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if value in values:
                    self.remove_parameter_value(parameter, value)
                else:
                    self.add_parameter_value(parameter, value)
                return
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def remove_parameter_value(self, parameter, value):
        """
        Remove a specific value from a parameter's values.
        Raises an AttributeError if the parameter does not exist.
        """

        for key, values in self.args:
            if key == parameter:
                if value in values:
                    values.remove(value)
                return
        raise AttributeError(f"Parameter '{parameter}' does not exist")

    def get_query_string(self):
        """
        Get the full query string.
        """

        return f"?{urlencode(self.args, doseq=True)}"
