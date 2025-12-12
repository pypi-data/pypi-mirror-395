import os
import multiprocessing
import logging
from typing import Any, Union, Optional


class Environ_:
    """
    A simple utility class to interact with environment variables.

    This class provides an encapsulated way to access environment variables using
    either function or attribute-like syntax. It facilitates fetching the values
    of environment variables with the ability to specify a default value if the
    requested variable is not set.

    Methods
    -------
    __call__(value, default=None)
        Fetches the value of the environment variable with an optional default
        fallback if the variable is not found.

    __getattr__(value)
        Retrieves the value of the environment variable or returns None if it's
        not found.
    """

    def __call__(self, value: str, default: Any = None) -> Union[str, Any]:
        """
        Retrieves the value of an environment variable if it exists, otherwise returns a default value.

        This function serves as a wrapper for `os.getenv`, allowing the caller to fetch the value of
        a specified environment variable. If the environment variable does not exist or is unset, a
        default value can be optionally provided to be returned.

        Parameters
        ----------
        value : str
            The name of the environment variable to retrieve.
        default : any, optional
            The default value to return if the specified environment variable is not found.
            If not provided, `None` will be returned.

        Returns
        -------
        str or any
            The value of the environment variable if it exists or the default value if it does not exist.
        """
        return os.getenv(value, default)

    def __getattr__(self, value: str) -> Optional[str]:
        """
        Retrieves the value of an environment variable.

        This method attempts to fetch the value associated with an environment variable
        using the provided `value` as the variable's name. If the specified environment
        variable is not set, it returns None instead of raising an exception.

        Parameters
        ----------
        value : str
            The name of the environment variable whose value needs to be retrieved.

        Returns
        -------
        str or None
            The value of the specified environment variable if it exists, otherwise None.

        """
        return os.getenv(value, None)


environ = Environ_()


def run_script(script: str, port: int) -> None:
    """
    Runs a specified script in a new process and passes a port as an argument.

    The function checks if the provided script exists. If it does, a new process
    is created to execute the script with the provided port as an argument. If
    the script does not exist, a warning is logged.

    Parameters
    ----------
    script : str
        The path to the script file to execute.
    port : int
        The port number to pass as an argument to the script being executed.
    """
    if os.path.exists(script):

        def worker(script, port):
            os.system(f"python {script} {port}")

        p = multiprocessing.Process(target=worker, args=(script, port))
        p.start()
    else:
        logging.warning(f"{script} not exists")
