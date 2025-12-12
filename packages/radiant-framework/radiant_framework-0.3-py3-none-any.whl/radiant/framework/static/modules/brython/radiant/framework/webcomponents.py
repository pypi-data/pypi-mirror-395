from browser import html
from functools import cache

maketag = cache(html.maketag)


class WebComponents:
    """
    Represents a dynamic component builder for generating HTML or web component tags.

    This class is designed to handle the creation of web components or HTML tags
    dynamically. By utilizing Python's attribute overloading, it allows developers
    to generate tag structures for a wide variety of elements by calling attributes
    as functions. The `root` parameter serves as a prefix for generating custom
    components with consistent naming conventions.

    Attributes
    ----------
    root : str
        Prefix to be used for generating custom HTML tags.
    """

    def __init__(self, root=""):
        """
        A class for handling and managing a root directory path.

        This class is designed to store and manage a root directory path, providing
        a foundational setup for file system operations or related tasks.

        Attributes
        ----------
        root : str
            The root directory path to be managed by the instance.
        """
        self.root = root

    def __getattr__(self, attr):
        """
        Defines a dynamic attribute accessor and generator for tagged elements.
        When an attribute is accessed, a callable function is returned, which can
        be used to create tags with customized arguments and keyword arguments.

        Parameters
        ----------
        attr : str
            The name of the attribute being accessed. If the attribute starts with
            an underscore (`_`), it is interpreted differently by processing the
            string to form the appropriate tag.

        Returns
        -------
        element : Callable
            A callable function that generates a tag with the specified arguments
            and keyword arguments. The function processes positional arguments
            and optionally updates keyword arguments by removing trailing
            underscores from the keys to fit the desired format.
        """

        def element(*args, **kwargs):
            # Determine the tag name based on whether the attribute starts with an underscore
            # Underscore means it's a raw tag (e.g., "_input" → "input"), otherwise use the prefixed root
            if attr.startswith("_"):
                tag = maketag(f'{attr[1:].removesuffix("_").replace("_", "-")}')
            else:
                tag = maketag(f'{self.root}-{attr.removesuffix("_").replace("_", "-")}')

            # Normalize keyword arguments by removing trailing underscores (e.g., "class_" → "class")
            kwargs = {k.rstrip("_"): v for k, v in kwargs.items()}

            # Return the tag instance with all arguments and processed attributes
            return tag(*args, **kwargs)

        return element
