import sys

# Abort execution if running in a Brython (browser) environment
try:
    import browser  # Brython-specific module

    sys.exit()  # Exit if imported in Brython to avoid executing server-side logic
except ImportError:
    pass  # Not running in Brython; continue with server initialization

import os
import json
import shutil

import pathlib
import importlib
import importlib.util
from typing import Union, List, Tuple, Optional

from tornado.web import Application, url, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

DEBUG = True
PATH = Union[str, pathlib.Path]
URL = str
DEFAULT_IP = "0.0.0.0"
DEFAULT_PORT = "5050"
DEFAULT_BRYTHON_VERSION = "latest"
DEFAULT_BRYTHON_DEBUG = 0
MAIN = sys.argv[0]


class RadiantInterfaceApp:
    """
    Base class for applications using the Radiant framework with a hybrid
    Python + Brython architecture.

    This class must be inherited by user-defined applications, and provides
    a unified interface for launching apps either with default or custom
    server settings.
    """

    endpoints = []
    _server_configuration = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __new__(cls, **kwargs):
        """
        Overrides instantiation to redirect to the server launcher.

        This allows instantiating the class to automatically start the server.
        Typically used for quick starts without explicit configuration.
        """
        # When the user "instantiates" the app, start the server immediately.
        return RadiantServer(cls.__name__, **kwargs)

    @classmethod
    def configure(cls, **kwargs):
        """
        Store server configuration options to be used when launching via `.serve()`.

        Parameters
        ----------
        **kwargs : dict
            Configuration options such as `port`, `host`, `brython_version`, etc.

        Returns
        -------
        cls : type
            Returns the class itself with configuration stored.
        """
        # Save server configuration for later use in .serve()
        cls._server_configuration = kwargs
        return cls

    @classmethod
    def serve(cls):
        """
        Launch the application using previously configured options or defaults.

        This method instantiates the RadiantServer using the stored class name
        and configuration passed to `configure()`.
        """
        # Start the server with stored configuration.

        return RadiantServer(cls.__name__, **cls._server_configuration)


class AppRouter:
    """
    Static router class for defining and launching multipage Radiant applications.

    This class provides decorators to register GET and POST routes, and methods to
    configure and launch the Radiant server. It is typically used in routing-based
    (multi-page) mode rather than interface-driven (SPA) applications.
    """

    _server_configuration = {}

    @classmethod
    def configure(cls, **kwargs):
        """
        Store configuration parameters for launching the Radiant server.

        Returns
        -------
        cls : type
            The class itself to allow method chaining with `.serve()`.
        """
        cls._server_configuration = kwargs
        return cls

    @classmethod
    def serve(cls):
        """
        Start the Radiant server using configuration set via `.configure()`.

        Returns
        -------
        None
        """
        return RadiantServer(cls.__name__, **cls._server_configuration)

    @classmethod
    def launch(cls, **kwargs):
        """
        Launch the Radiant server with the given configuration.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments passed to RadiantServer such as port, host, pages, etc.

        Returns
        -------
        None
        """
        # Start the Radiant server for the application using provided arguments.
        return RadiantServer(cls.__name__, **kwargs)

    @classmethod
    def get_route(cls, url):
        """
        Register a new GET route and associate it with a view function.

        Parameters
        ----------
        url : str
            The URL pattern to match.

        Returns
        -------
        function
            A decorator that registers the function with the given URL.
        """

        def inset(fn):
            # Append GET route to global endpoints list
            RadiantInterfaceApp.endpoints.append((url, fn.__name__, "GET", fn))

        return inset

    @classmethod
    def post_route(cls, url):
        """
        Register a new POST route and associate it with a view function.

        Parameters
        ----------
        url : str
            The URL pattern to match.

        Returns
        -------
        function
            A decorator that registers the function with the given URL.
        """

        def inset(fn):
            # Append POST route to global endpoints list
            RadiantInterfaceApp.endpoints.append((url, fn.__name__, "POST", fn))

        return inset


class PythonHandler(RequestHandler):
    """
    Request handler that allows calling internal methods dynamically
    via POST requests with serialized arguments.

    This is useful for remote procedure calls between the client and server.
    """

    def post(self):
        """
        Handle a POST request to dynamically call a method from the handler.

        Expects the following POST parameters:
        - name: Name of the method to call.
        - args: JSON-encoded tuple of positional arguments.
        - kwargs: JSON-encoded dictionary of keyword arguments.
        """
        name = self.get_argument("name")
        args = tuple(json.loads(self.get_argument("args")))
        kwargs = json.loads(self.get_argument("kwargs"))

        # Call the method if it exists, passing in args and kwargs
        if v := getattr(self, name, None)(*args, **kwargs):
            if v is None:
                # Write default zero response if return is None
                data = json.dumps({"__RDNT__": 0})
            else:
                # Write returned data in wrapped format
                data = json.dumps({"__RDNT__": v})
            self.write(data)

    def test(self):
        """
        Example method that returns True.
        Can be invoked remotely via POST with name='test'.
        """
        return True

    def prepare(self):
        """
        Override this method to prepare the request before handling.
        Can be used for parsing headers or authentication in the future.
        """
        pass


class JSONHandler(RequestHandler):
    """
    A simple Tornado handler that returns preloaded JSON data on GET requests.

    This is useful for serving static or dynamically assembled JSON environments
    such as Brython config, template metadata, or other frontend bootstrapping data.
    """

    def initialize(self, **kwargs):
        """
        Store JSON data passed during handler instantiation.

        Parameters
        ----------
        **kwargs : dict
            The data to serve as JSON on GET requests.
        """
        self.json_data = kwargs

    def get(self):
        """
        Return the stored JSON data to the client.
        """
        self.write(self.json_data)

    def test(self):
        """
        Test method that returns True.
        Can be used to verify remote method invocation functionality.
        """
        return True


class RadiantHandler(RequestHandler):
    """
    Tornado request handler used to render the main application template and
    manage static site generation for Brython-based web applications.
    """

    domain = ""

    def initialize(self, **kwargs):
        """
        Initialize handler with environment variables passed via settings.

        Parameters
        ----------
        **kwargs : dict
            Variables that will be injected into the template rendering context.
        """
        self.initial_arguments = kwargs

    def set_default_headers(self):
        """
        Set CORS headers to allow cross-origin requests from any origin.
        Useful for development and embedding.
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        """
        Handle GET requests by rendering the specified HTML template using
        provided settings and optionally exporting a static HTML version.
        """
        # Merge template variables from settings and arguments
        variables = self.settings.copy()
        variables.update(self.initial_arguments)
        variables["argv"] = json.dumps(variables["argv"])

        # Static site generation logic (if enabled)
        if variables["static_app"]:
            html = self.render_string(
                f"{os.path.realpath(variables['template'])}", **variables
            )

            # Define output directory
            if isinstance(variables["static_app"], str):
                parent_dir = variables["static_app"]
            else:
                parent_dir = f"{variables['class_']}_static"

            # Clean and recreate directory
            if os.path.exists(parent_dir):
                shutil.rmtree(parent_dir)

            shutil.copytree(os.path.dirname(MAIN), os.path.join(parent_dir, "root"))
            shutil.copytree(
                os.path.join(os.path.dirname(__file__), "static"),
                os.path.join(parent_dir, "static"),
            )

            # Remove git-related files if present
            for element in [".git", ".gitignore"]:
                if os.path.exists(os.path.join(parent_dir, "root", element)):
                    try:
                        shutil.rmtree(os.path.join(parent_dir, "root", element))
                    except:
                        os.remove(os.path.join(parent_dir, "root", element))

            # Write rendered HTML to disk
            with open(os.path.join(parent_dir, "index.html"), "wb") as file:
                file.write(html)

            # Create folder for Brython environment variables
            environ_path = os.path.join(parent_dir, self.domain.lstrip("/"))
            if not os.path.exists(environ_path):
                os.mkdir(environ_path)

            # Write initial arguments to environ.json
            with open(os.path.join(environ_path, "environ.json"), "w") as file:
                json.dump(self.initial_arguments, file)

            # Copy optional files (e.g., GitHub Pages metadata)
            for element in ["CNAME", ".nojekyll"]:
                if os.path.exists(element):
                    shutil.copyfile(element, os.path.join(parent_dir, element))

        # Add raw request arguments for template rendering
        variables["arguments"] = self.request.arguments

        # Render final page to response
        self.render(f"{os.path.realpath(variables['template'])}", **variables)


def RadiantHandlerPost(fn):
    """
    Decorator to wrap a function as a POST request handler using the RadiantHandler base.

    This allows registering simple functions as HTTP POST endpoints
    by returning a dynamically constructed RequestHandler.
    """

    class RadiantHandler_(RadiantHandler):
        """
        Internal subclass of RadiantHandler to handle POST requests by executing the provided function.
        """

        def post(self):
            """
            Handle POST request by collecting form data and invoking the decorated function.

            Converts all request arguments into a dictionary and passes them as keyword arguments.
            Sends back the result as a JSON response.
            """
            # Collect all arguments from the request
            data = {key: self.get_argument(key) for key in self.request.arguments}

            # Call the provided function with unpacked arguments
            response = fn(**data)

            # Send JSON response
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(response))

    return RadiantHandler_


# ----------------------------------------------------------------------
def make_app(
    class_: str,
    /,
    brython_version: str,
    debug_level: int,
    pages: Tuple[str],
    endpoints: Tuple[str],
    template: PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html"),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
    python: Tuple[PATH, str] = ([None, None, None]),
    theme: PATH = None,
    path: List = [],
    autoreload: bool = False,
    static_app: bool = False,
    domain: Optional[str] = "",
    templates_path: PATH = None,
    modules: Optional[list] = [],
    page_title: Optional[str] = "",
    page_favicon: Optional[str] = "",
    page_description: Optional[str] = "",
    page_image: Optional[str] = "",
    page_url: Optional[str] = "",
    page_summary_large_image: Optional[str] = "",
    page_site: Optional[str] = "",
    page_author: Optional[str] = "",
    page_copyright: Optional[str] = "",
):
    """
    Assemble and return a Tornado web Application configured for Radiant.

    This function dynamically binds all server-side routes, static file handlers,
    Brython environment metadata, and associated request handlers. It supports
    multipage and SPA-style routing, static app generation, and Python–Brython bridging.

    Parameters
    ----------
    class_ : str
        Name of the main Brython-executed class.
    brython_version : str
        Brython runtime version to inject.
    debug_level : int
        Brython debug level (0–2).
    pages : Tuple[str]
        List of URL patterns mapped to Brython-executed classes.
    endpoints : Tuple[str]
        List of HTTP endpoints (registered via decorators).
    template : str
        Path to the main HTML template.
    environ : dict
        Metadata and runtime configuration shared with Brython.
    mock_imports : Tuple[str]
        List of modules to exclude from import errors in Brython.
    handlers : Tuple
        Custom Tornado handler definitions.
    python : Tuple
        Handlers for native Python routes or logic modules.
    theme : str
        Path to XML theme definition.
    path : list
        Extra Brython paths to expose.
    autoreload : bool
        Enables Tornado's autoreload dev feature.
    static_app : bool
        Flag for static site generation.
    domain : str
        Root-relative domain prefix for routes.
    templates_path : str
        Custom path for Jinja2 templates.
    modules : list
        Optional Brython module list to preload.
    page_title, page_favicon, page_description, ...
        Metadata for dynamic page rendering or SEO.

    Returns
    -------
    tornado.web.Application
        A configured Tornado app ready to be served.
    """

    # Tornado core settings
    settings = {
        "debug": DEBUG,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "static_url_prefix": f"{domain}/static/",
        "xsrf_cookies": False,
        "autoreload": autoreload,
    }

    # Optionally add custom Jinja2 template path
    if templates_path:
        settings["template_path"] = templates_path

    # Populate environ with runtime context and Brython/SEO metadata
    environ.update(
        {
            "class_": class_,
            "python_": python,
            "module": os.path.split(sys.path[0])[-1],
            "file": os.path.split(MAIN)[-1].replace(".py", ""),
            "file_path": os.path.join(f"{domain}/root", os.path.split(MAIN)[-1]),
            "theme": theme,
            "argv": [MAIN],
            "template": template,
            "mock_imports": mock_imports,
            "path": [f"{domain}/root/", f"{domain}/static/modules/brython"] + path,
            "brython_version": brython_version,
            "debug_level": debug_level,
            "static_app": static_app,
            "domain": domain,
            "modules": modules,
            "page_title": page_title,
            "page_favicon": page_favicon,
            "page_description": page_description,
            "page_image": page_image,
            "page_url": page_url,
            "page_summary_large_image": page_summary_large_image,
            "page_site": page_site,
            "page_author": page_author,
            "page_copyright": page_copyright,
            "wrapped": False,
        }
    )

    # List of Tornado URL routes and handlers
    app = []

    # Main root route for RadiantHandler (except for API-only mode)
    if class_ and class_ != "AppRouter":
        RadiantHandler.domain = domain
        app += [url(r"^/$", RadiantHandler, environ)]

    # Core static routes: theme, root files, and environ JSON
    app += [
        # url(rf"^{domain}/theme.css$", ThemeHandler),
        url(rf"^{domain}/root/(.*)", StaticFileHandler, {"path": sys.path[0]}),
        url(rf"^{domain}/environ.json$", JSONHandler, environ),
    ]

    # Dynamically resolve pages if passed as import path string
    if isinstance(pages, str):
        *package, module_name = pages.split(".")
        module = importlib.import_module(".".join(package))
        pages = getattr(module, module_name)

    # Register Brython-mapped pages as routes
    for url_, module in pages:
        environ_tmp = environ.copy()
        # If module is a class (subclass of RadiantInterfaceApp), use its name
        if not isinstance(module, str) and issubclass(module, RadiantInterfaceApp):
            environ_tmp["file"] = os.path.split(sys.argv[0])[-1].rstrip(".py")
            environ_tmp["class_"] = module.__name__
        else:
            # If module is a string, split for file/class assignment
            *file_, class_ = (
                module.split(".")
                if "." in module
                else f"{os.path.split(MAIN)[-1][:-3]}.{module}".split(".")
            )
            environ_tmp["file"] = ".".join(file_)
            environ_tmp["class_"] = class_
        app.append(url(url_, RadiantHandler, environ_tmp))

    # Dynamically resolve endpoints if passed as import path string
    if isinstance(endpoints, str):
        *package, module_name = endpoints.split(".")
        module = importlib.import_module(".".join(package))
        endpoints = getattr(module, module_name)

    # Sort endpoints to ensure POSTs are registered before GETs
    reference_order = ["POST", "GET"]
    sorted_endpoints = sorted(
        RadiantInterfaceApp.endpoints,
        key=lambda x: (
            reference_order.index(x[2]) if x[2] in reference_order else float("inf")
        ),
    )

    # Register POST/GET endpoint handlers
    handlers_ = {}
    for url_, module, method, fn in sorted_endpoints:
        environ_tmp = environ.copy()
        environ_tmp["file"] = os.path.split(sys.argv[0])[-1].rstrip(".py")
        environ_tmp["class_"] = module
        environ_tmp["wrapped"] = True
        if method == "POST":
            handlers_[url_] = RadiantHandlerPost(fn)
        elif method == "GET":
            handler = handlers_.pop(url_, RadiantHandler)
            app.append(url(url_, handler, environ_tmp))

    # Append remaining POST handlers to the Tornado route list
    for url_ in handlers_:
        app.append(url(url_, handlers_[url_], environ_tmp))

    # Register native Python route handlers
    for module, class_, endpoint in python:
        python_path = (
            os.path.join(sys.path[0], module) if not os.path.isabs(module) else module
        )
        spec = importlib.util.spec_from_file_location(
            ".".join([module, class_]).replace(".py", ""), python_path
        )
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        app.append(url(f"^{endpoint}", getattr(foo, class_)))

    # Register custom user-defined handlers
    for handler in handlers:
        if isinstance(handler[1], tuple):
            spec = importlib.util.spec_from_file_location(
                ".".join(handler[1]).replace(".py", ""),
                os.path.abspath(handler[1][0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            app.append(url(handler[0], getattr(foo, handler[1][1]), handler[2]))
        else:
            app.append(url(*handler))

    # Serve any additional static directories in Brython path
    for dir_ in path:
        app.append(
            url(
                rf'^/{os.path.split(dir_)[-1].strip("/")}/(.*)',
                StaticFileHandler,
                {"path": dir_},
            )
        )

    # Merge settings with environ for template access
    settings.update(environ)

    return Application(app, **settings)


def RadiantServer(
    class_: Optional[str] = None,
    host: str = DEFAULT_IP,
    port: str = DEFAULT_PORT,
    pages: Tuple[str] = (),
    endpoints: Tuple[str] = (),
    brython_version: str = DEFAULT_BRYTHON_VERSION,
    debug_level: int = DEFAULT_BRYTHON_DEBUG,
    template: PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html"),
    environ: dict = {},
    mock_imports: Tuple[str] = [],
    handlers: Tuple[URL, Union[List[Union[PATH, str]], RequestHandler], dict] = (),
    python: Tuple[PATH, str] = (),
    theme: Optional[PATH] = None,
    path: Optional[list] = [],
    autoreload: Optional[bool] = False,
    callbacks: Optional[tuple] = (),
    static_app: Optional[bool] = False,
    domain: Optional[str] = "",
    templates_path: PATH = None,
    modules: Optional[list] = ["roboto"],
    page_title: Optional[str] = "",
    page_favicon: Optional[str] = "",
    page_description: Optional[str] = "",
    page_image: Optional[str] = "",
    page_url: Optional[str] = "",
    page_summary_large_image: Optional[str] = "",
    page_site: Optional[str] = "",
    page_author: Optional[str] = "",
    page_copyright: Optional[str] = "",
    **kwargs,
):
    """
    Launch the Radiant development server with the given configuration.

    This function sets up a Tornado HTTP server that integrates a Brython-based
    frontend environment with a Python backend. It dynamically injects application
    configuration and optionally launches callback routines after server setup.

    Parameters
    ----------
    class_ : str
        Name of the main Brython class to render and execute.
    host : str
        IP address or hostname where the server will run.
    port : str
        Port number where the server will listen.
    pages : Tuple[str]
        List of URL routes mapped to Brython classes.
    endpoints : Tuple[str]
        Registered route endpoints for GET/POST handlers.
    brython_version : str
        Brython version string to be injected into the environment.
    debug_level : int
        Debug level passed to Brython.
    template : str
        Path to the main HTML template for rendering the UI.
    environ : dict
        Dictionary of variables passed to the frontend environment.
    mock_imports : Tuple[str]
        List of modules to ignore during Brython import resolution.
    handlers : Tuple
        Custom Tornado handlers provided by the user.
    python : Tuple
        Native Python handler definitions.
    theme : str
        Path to XML theme file for dynamic stylesheet rendering.
    path : list
        List of static directories to expose to Brython.
    autoreload : bool
        Enable Tornado autoreload server setting.
    callbacks : tuple
        Tuple of callables or (module_path, function_name) tuples to run after server launch.
    static_app : bool
        Flag to activate static app export.
    domain : str
        Domain prefix for routing purposes.
    templates_path : str
        Optional override path for Jinja2 templates.
    modules : list
        Additional Brython modules to preload.
    page_* : str
        Metadata for SEO and social preview purposes.
    **kwargs : dict
        Extra keyword arguments forwarded to make_app().

    Returns
    -------
    None
    """

    # Print launch message
    print(f"Radiant server running at http://{host}:{port}/")

    # Create Tornado application with all routes and environment configuration
    application = make_app(
        class_,
        python=python,
        template=template,
        handlers=handlers,
        theme=theme,
        environ=environ,
        mock_imports=mock_imports,
        path=path,
        brython_version=brython_version,
        pages=pages,
        endpoints=endpoints,
        debug_level=debug_level,
        static_app=static_app,
        domain=domain,
        templates_path=templates_path,
        modules=modules,
        page_title=page_title,
        page_favicon=page_favicon,
        page_description=page_description,
        page_image=page_image,
        page_url=page_url,
        page_summary_large_image=page_summary_large_image,
        page_site=page_site,
        page_author=page_author,
        page_copyright=page_copyright,
    )

    # Initialize HTTP server and bind it to host:port
    http_server = HTTPServer(application)
    http_server.listen(port, host)

    # Execute any post-launch callbacks if defined
    for handler in callbacks:
        if isinstance(handler, tuple):
            # Dynamically load and execute function by path
            spec = importlib.util.spec_from_file_location(
                ".".join(handler).replace(".py", ""),
                os.path.abspath(handler[0]),
            )
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            getattr(foo, handler[1])()
        else:
            handler()

    # Start Tornado I/O loop
    IOLoop.instance().start()


def render(*args, **kwargs):
    """
    This function has no effect on the server side.

    It is meant to be overridden or used only in the Brython (browser-side)
    context for DOM rendering purposes.
    """
    # No-op on server: only meaningful in Brython client-side execution
    return None


def launch_from_settings(module):
    config = {k.lower(): getattr(module, k) for k in dir(module) if k.isupper()}
    RadiantServer(**config)
