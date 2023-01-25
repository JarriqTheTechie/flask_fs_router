

Straightforward file-based routing extension for Flask. Introduces the concepts of pages to Flask. 

<br>

# Getting Started
`pip install flask_fs_router`

<br>
Initialize the extension.

```
from flask import Flask
from flask_fs_router import FlaskFSRouter

app = Flask(__name__)
FlaskFSRouter(app)
```

<br>
 
Pages are python files with a **default** function defined. These pages are stored in the `/pages` directory of your project, it is automatically available as a route based on its filename. 


Create an example index route.

`pages/index.py`

```
def default():
    return "Home page"
```


# Conventions


### Index Pages
The index file of any folder is the name of that folder. 


```
pages/ecommerce/index.py              ->         oursite.com/ecommerce     |  GET
pages/products/index.py               ->         oursite.com/products      |  GET
```


### Static Routes

```


pages/index.py              ->        oursite.com/          |  GET
pages/about.py              ->        oursite.com/about     |  GET
pages/about/index.py        ->        oursite.com/about     |  GET
pages/about/me.py           ->        oursite.com/about/me  |  GET
pages/posts/1.py            ->        oursite.com/posts/1   |  GET
pages/posts/[post_id].py    ->        oursite.com/posts/<post_id>  |  GET
```

### Request Methods
By default, pages map to **GET** requests. To change this behavior, define request methods within the file name using parentheses.

```
Example: Request methods

pages/posts/create_post(post).py            ->        oursite.com/posts/create-post  |  POST
```

# Github Page
[https://github.com/JarriqTheTechie/flask_fs_router
](https://github.com/JarriqTheTechie/flask_fs_router)
# Contributing
We love the idea of a community. We'll be putting together a contribution guide in the near future.

# License

flask_fs_router is available as open source under the terms of the MIT License http://opensource.org/licenses/MIT

