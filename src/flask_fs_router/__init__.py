import fnmatch
import os
import secrets
from pydoc import locate
from typing import Any
from pathlib import Path


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
        [
            app.add_url_rule(
                route.get('path'),
                **dict(
                    view_func=route.get('view_func'),
                    endpoint=route.get('endpoint'),
                    methods=[route.get('method')],
                    websocket=route.get("ws")
                )
            ) for route in self.routes_export()
        ]

    def find_routes_files(self):
        self.possible_routes = []
        pages_path = Path('pages')
        pages = list(pages_path.glob('**/*.py'))
        [
            self.possible_routes.append(
                str(page).lstrip("pages").lstrip("\\").replace("\\", "."))
            for page in pages
        ]
        return self

    def generate_fqns(self):
        self.fqdns = []
        [
            self.fqdns.append(f"pages.{route.rstrip('.py')}.default") for route in self.possible_routes
        ]
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
        return self

    def routes_export(self):
        return self.find_routes_files().generate_fqns().fqdns_to_route_path().route_map
