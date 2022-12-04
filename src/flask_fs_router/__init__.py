import fnmatch
import os
import secrets
from pydoc import locate
from typing import Any


def to_class(path: str) -> Any:
    """
        Converts string class path to a python class

    return:
        mixed
    """
    try:
        class_instance = locate(path)
    except ImportError:
        class_instance = None
    return class_instance or None


class FlaskFSRouter:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for route in FlaskFSRouter().routes_export():
            app.add_url_rule(
                route.get('path'),
                **dict(
                    view_func=route.get('view_func'),
                    endpoint=route.get('endpoint'),
                    methods=[route.get('method')],
                    websocket=route.get("ws")
                )
            )

    def find_routes_files(self):
        self.possible_routes = []
        for root, dirnames, filenames in os.walk('pages'):
            for filename in fnmatch.filter(filenames, '*.py'):
                if filename:
                    self.possible_routes.append(
                        os.path.join( root, filename ).lstrip( "pages" ).lstrip( "\\" ).replace( "\\", "." ) )
        return self

    def generate_fqns(self):
        self.fqdns = []
        for route in self.possible_routes:
            fqdn = f"pages.{route.rstrip('.py')}.default"
            self.fqdns.append(fqdn)
        return self

    def fqdns_to_route_path(self):
        self.route_paths = []
        self.route_map = []
        for path in self.fqdns:
            fqdn = path
            path = path.replace("default", "")
            path = path.replace("pages.", "/")
            path = path.replace(".", "/")

            path = path.replace("index/", "")
            path = path.replace("[", "<").replace("]", ">")


            method = fqdn.split("(")[-1].split(')')[0]
            if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                method = method
            else:
                method = "GET"
            if path == "/":
                pass
            else:
                path = path.rstrip("/")
            fqdn = fqdn.replace("//", '').replace("/", '.').replace("..", '.')
            path = path.replace('_', '-').replace(f'({method})', '').replace("//", '/') or '/'
            self.route_map.append({
                "path": path,
                "fqdn": fqdn,
                "view_func": to_class(fqdn),
                "endpoint": to_class(fqdn.replace("default", "endpoint")) or secrets.token_urlsafe(8),
                "method": method,
                "ws": to_class(fqdn.replace("default", "ws")) or False
            })
            #print({
            #    "path": path,
            #    "fqdn": fqdn,
            #    "view_func": to_class(fqdn),
            #    "endpoint": to_class(fqdn.replace("default", "endpoint")) or secrets.token_urlsafe(8),
            #    "method": method,
            #    "ws": to_class(fqdn.replace("default", "ws")) or False
            #})
        return self

    def routes_export(self):
        return self.find_routes_files().generate_fqns().fqdns_to_route_path().route_map
