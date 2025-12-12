class Node_Reference:

    def __init__(self, components):
        if not isinstance(components, list):
            raise ValueError("components must be a list")
        self.components = []
        for component in components:
            if not (isinstance(component, str) or isinstance(component, int)):
                raise ValueError(f"Reference component '{component}' must be either a 'str' or an 'int'")
            self.components.append(component)
        self.parent = None
        self.item = None

    def to_string(self, depth=0, indentation_space_count=3):

        s = " " * indentation_space_count * depth + "@"
        for component in self.components:
            s += f"[{component}]"

        if self.item is None:
            s += " UNRESOLVED"
        return s + "\n"

    def __str__(self):
        
        s = "@"
        for component in self.components:
            s += f"[{component}]"

        return s

    def __repr__(self):

        return self.__class__.__name__ + f"(components={self.components})"
