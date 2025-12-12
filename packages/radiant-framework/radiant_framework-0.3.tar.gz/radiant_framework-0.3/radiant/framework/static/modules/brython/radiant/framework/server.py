import os

from browser import document, timer
from .utils import LocalInterpreter
from .html_ import select, html
from browser.template import Template
from interpreter import Interpreter

RadiantServer = None


########################################################################
class RadiantInterfaceApp:
    """
    Represents the core interface for a Radiant Framework application.

    This class initializes the application environment and provides utility methods
    to interact with the DOM, add visual elements, and manage style and functionality
    for web-based applications developed using the framework.

    Attributes
    ----------
    endpoints : list
        A list to store endpoints for the application.
    body : dynamic
        Represents the main body element of the DOM for manipulations.
    head : dynamic
        Represents the head element of the DOM for manipulations.
    """

    endpoints = []

    # ----------------------------------------------------------------------
    def __init__(self, class_, python=[[None, None, None]], **kwargs):
        """
        Creates an instance and initializes it with specified parameters and default settings.

        The class is designed to dynamically set attributes based on the provided list of
        tuples, where each tuple represents a module name, class name, and endpoint. It
        also performs initial mount actions and selects specific DOM elements for later use.

        Parameters
        ----------
        class_ : Any
            A generic parameter representing the class type or any required identifier.
        python : list of list, optional
            A list containing inner lists, where each inner list includes three elements:
            module (str), class name (str), and endpoint (str). Defaults to
            [[None, None, None]].
        kwargs : dict
            Additional keyword arguments that can be passed for further customization.
        """
        for module, class_, endpoint in python:
            if module and module != "None":
                setattr(self, class_, LocalInterpreter(endpoint=endpoint))

        self.body = select("body")
        self.head = select("head")
        self.on_mount()

    def add_css_file(self, file):
        """
        Adds a CSS file to the document's head element.

        This method appends a CSS link element to the <head> section of the document,
        allowing the specific CSS file to be applied to the webpage. The CSS file path
        should be relative to the specified root directory defined in the `href`.

        Parameters
        ----------
        file : str
            The relative path to the CSS file to be added. This path will be combined
            with the root directory to correctly locate the file.
        """
        document.select("head")[0] <= html.LINK(
            href=os.path.join("root", file), type="text/css", rel="stylesheet"
        )

    def map_value(self, x, in_min, in_max, out_min, out_max):
        """
        Maps an input value from one range to another based on linear interpolation.

        The function linearly transforms a value from the input range (in_min, in_max)
        to a corresponding value in the output range (out_min, out_max). It is useful
        for scaling values between different numerical intervals, for example, normalizing
        sensor data or scaling input values for computations.

        Parameters
        ----------
        x : float
            The input value to be mapped.
        in_min : float
            The minimum value of the input range.
        in_max : float
            The maximum value of the input range.
        out_min : float
            The minimum value of the output range.
        out_max : float
            The maximum value of the output range.

        Returns
        -------
        float
            The value scaled to the output range.
        """
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def welcome(self):
        """
        Constructs the `welcome` method which generates the initial web interface
        for the Radiant Framework using an HTML-like structure. It includes headers,
        links to documentation and repository, a terminal button, an embedded logo
        image, and an informational display related to the framework's status.

        This interface is styled using various inline CSS properties and dependencies
        based on the Brython library. The method initializes with consistent color
        schemes, text styles, and button functionality, focusing on providing a
        straightforward and user-friendly design.

        Attributes
        ----------
        body : MutableMapping
            The main HTML body for the web page, styled and populated dynamically
            with framework elements and design.

        Notes
        -----
        The `welcome` method primarily serves as a visual entry point for users
        interacting with the Radiant Framework. The terminal button is functional
        as it triggers a new `Interpreter` instance for executing tasks. The links
        provided aim to guide users to relevant framework resources, such as
        detailed documentation and source code repositories.

        The Radiant Framework logo, styled responsively, enhances the UI with branded
        visuals while maintaining aesthetic consistency.

        No arguments are required to call the method, as all elements and styles
        are defined and managed internally within the function context.
        """
        parent = html.DIV(
            style={"width": "90vw", "margin-left": "5vw", "margin-right": "5vw"}
        )

        links_style = {
            "color": "#28BDB8",
            "text-decoration": "none",
            "font-weight": "400",
        }

        buttons_style = {
            "background-color": "#28bdb8",
            "border": "none",
            "padding": "10px 15px",
            "color": "white",
        }

        with parent.context as parent:
            parent <= html.H1(
                "Radiant Framework", style={"font-weight": "300", "color": "#28bdb8"}
            )
            documentation = html.A(
                " documentation ",
                href="https://radiant-framework.readthedocs.io",
                style=links_style,
            )
            repository = html.A(
                " repository ",
                href="https://github.com/dunderlab/python-radiant_framework",
                style=links_style,
            )
            brython = html.A(
                " Brython ", href="https://brython.info/", style=links_style
            )

            with html.SPAN().context as tagline:
                tagline <= html.SPAN("Visit the")
                tagline <= documentation
                tagline <= html.SPAN("for more information or the")
                tagline <= repository
                tagline <= html.SPAN("to get the source code.")

            with html.DIV(style={"padding": "20px 0px"}).context as container:
                with html.BUTTON(
                    "Open Terminal", style=buttons_style
                ).context as button:
                    button.bind(
                        "click",
                        lambda evt: Interpreter(title="Radiant Framework", cols=80),
                    )

            with html.IMG(
                src="https://radiant-framework.readthedocs.io/en/latest/_static/logo.svg"
            ).context as image:
                image.style.width = "100vw"
                image.style.height = "25vh"
                image.style["background-color"] = "#F2F2F2"
                image.style["border-top"] = "1px solid #cdcdcd"
                image.style["margin-top"] = "5vh"
                image.style["margin-left"] = "-5vw"

            with html.DIV(
                style={
                    "text-align": "center",
                    "font-size": "110%",
                    "width": "100%",
                }
            ).context as container:
                container <= html.SPAN("Radiant Framework is running succesfully!<br>")

                with html.SPAN().context as tagline:
                    tagline <= brython
                    tagline <= html.SPAN("powered!")

        self.body.style = {
            "background-color": "#F2F2F2",
            "font-family": "Roboto",
            "font-weight": "300",
            "margin": "0px",
            "padding": "0px",
        }
        self.body <= parent

    def hide(self, selector):
        """
        Hides the selected element by setting its display style to "none".

        This function returns an event handling function that, when triggered, applies
        a CSS style to hide the specified element on the web page. The element is
        selected using the provided selector string. Useful for creating dynamic
        interactions that visually hide elements in response to certain events.

        Parameters
        ----------
        selector : str
            A CSS selector string used to identify the element to hide.

        Returns
        -------
        function
            An event handling function that hides the selected element when invoked.
        """

        def inset(evt):
            document.select_one(selector).style = {"display": "none"}

        return inset

    def show(self, selector):
        """
        Creates an inset function that sets the display style of an HTML element
        to "block" when an event is triggered. Primarily designed for use in
        JavaScript DOM manipulation.

        Parameters
        ----------
        selector : str
            CSS selector string to identify the target HTML element in the DOM.

        Returns
        -------
        Callable
            A function that takes an event object as input and modifies the
            display style of the target HTML element to "block".
        """

        def inset(evt):
            document.select_one(selector).style = {"display": "block"}

        return inset

    def toggle(self, selector):
        """
        Toggles the display state of an HTML element selected by the provided CSS selector.

        The `toggle` method returns a function that, when triggered (e.g., by an event),
        checks the current `display` style of the targeted HTML element. If the element
        is currently hidden (`display: none`), it will become visible (`display: block`).
        If already visible, it will be hidden.

        Parameters
        ----------
        selector : str
            The CSS selector used to locate the target HTML element in the document.

        Returns
        -------
        function
            A function (event handler) that toggles the visibility of the targeted HTML
            element when invoked.
        """

        def inset(evt):
            if document.select_one(selector).style["display"] == "none":
                document.select_one(selector).style["display"] = "block"
            else:
                document.select_one(selector).style["display"] = "none"

        return inset


class AppRouter(RadiantInterfaceApp):
    """
    Handles routing functionality for an application. This class provides mechanisms to
    bind custom URL endpoints to functions, allowing for dynamic route management and
    execution of logic in a subclass of RadiantInterfaceApp.

    The primary goal of this class is to simplify route registration and encapsulate
    functionality execution in the context of dynamically created class instances. It
    extends RadiantInterfaceApp and manages endpoint associations.

    Attributes
    ----------
    No instance-level attributes are defined since this class focuses on providing
    class-level routing functionality for subclasses of RadiantInterfaceApp.
    """

    @classmethod
    def get_route(cls, url):
        """
        Adds a route, identified by the provided URL, and associates it with the given
        function name. The function is registered as an endpoint for the application.

        This method is designed to handle specific routes by wrapping the provided
        function within a newly instantiated class that derives from RadiantInterfaceApp.
        The provided function is executed with arguments extracted and passed dynamically.

        Parameters
        ----------
        url : str
            The URL route to register for the provided function.

        Returns
        -------
        Callable
            A decorator function that registers the given function as an endpoint
            associated with the provided URL and wraps it inside a dynamically created
            class instance inheriting from RadiantInterfaceApp.

        """

        def inset(fn):
            RadiantInterfaceApp.endpoints.append((url, fn.__name__))

            def subinset(**arguments):
                class Wrapped(RadiantInterfaceApp):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        fn(**{k: arguments[k][0] for k in arguments})

                return Wrapped

            return subinset

        return inset

    @classmethod
    def post_route(cls, url):
        """
        Registers a new route (endpoint) with its associated functionality in the
        RadiantInterfaceApp. This decorator allows specifying a URL endpoint and
        binding it to a specific function. When the endpoint is triggered, the
        wrapped function will be executed with the extracted arguments.

        The registered function, in turn, will be executed in the context of
        a dynamically generated class inherited from RadiantInterfaceApp.

        Parameters
        ----------
        url : str
            The URL endpoint to be registered for the function.

        Returns
        -------
        function
            A decorator wrapping the provided function and associating it with the
            specified URL endpoint. When the function is triggered, its arguments
            are dynamically processed and passed to a subclass of
            RadiantInterfaceApp instantiated at runtime.
        """

        def inset(fn):
            RadiantInterfaceApp.endpoints.append((url, fn.__name__))

            def subinset(**arguments):
                class Wrapped(RadiantInterfaceApp):
                    def __init__(self, *args, **kwargs):
                        super().__init__(*args, **kwargs)
                        fn(**{k: arguments[k][0] for k in arguments})

                return Wrapped

            return subinset

        return inset


def render(template, context={}):
    """
    Renders a template by updating the DOM element represented by a placeholder
    and injecting the provided context into the template.

    This function manipulates the DOM structure by selecting a placeholder element,
    updating its attributes to include the template, and passing the provided
    context variables for dynamic rendering. The rendered content is displayed
    on the web page.

    Parameters
    ----------
    template : str
        The relative path to the template file to be included.
    context : dict, optional
        A dictionary containing the context variables to be used in the rendering
        process. Defaults to an empty dictionary.

    Returns
    -------
    list
        A list of child elements present within the rendered placeholder element
        after the template has been rendered.
    """
    placeholder = "#radiant-placeholder--templates"
    parent = document.select_one(placeholder)
    parent.attrs["b-include"] = f"root/{template}"
    document.select_one("body") <= parent
    Template(placeholder[1:]).render(**context)
    document.select_one(placeholder).style = {"display": "block"}
    return document.select_one(placeholder).children
