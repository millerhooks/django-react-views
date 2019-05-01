# Django-React-Views

This is a fork of [django-react-views](https://pypi.org/project/django-react-views/). There wasn't a public git repo of it and I might need to change it later, so I'm putting it here.

django-react-riews is a Django app providing generic Class Based views and template tags that make it easy to use react
alongside django views and templates.

It can be used along with [channels-redux-python](https://pypi.org/project/channels-redux/) 
and [channels-redux-js](https://www.npmjs.com/package/channels-redux) to provide a framework to use websockets to keep 
a frontend redux state in sync with the database state.

Quick start
-----------

1. Add "django_react_views" to your INSTALLED_APPS setting like this::
    ```python
    INSTALLED_APPS = [
        ...
        'django_react_views',
    ]
    ```

1. Create a directory in your app called `react`

1. Copy `webpack.config.js` or use you're own webpack config as long as it builds your react components into one of your STATICFILES_DIRS

1. Use npm to install **at least** the packages required for react & building with webpack
    ```bash
    npm install --save-prod react react-dom
    npm install --save-dev babel-core babel-loader babel-preset-env babel-preset-es2015 babel-preset-react glob webpack webpack-cli
    ```

1. Add these scripts to `package.json`
    ```json
    "scripts": {
        "build": "webpack",
        "watch": "webpack --watch"
    },
    ```

1. Execute `npm run watch` to start building your react files

1. Add the react template tag to the template where you want to show your react component

    ```djangotemplate
    {% load react %}
    ...
    {% react %}
    ...
    ```

1. Create a view for your template
    ```python
    from django_react_views.views import ReactDetailView
    class MyReactView(ReactDetailView):
        react_component = 'MyReactComponent.js'  # By default this will resolve to dist/app_name/{react_component}. If {% static %} can not find the file you may need to edit some other properties of this class
        model_serializer = MyModelSerializer
        model = MyModel
    ```

1. Add a url for your view
    ```python
    urlpatterns = [
        ...
        path('my-react-view/<int:pk>/', MyReactView.as_view(), name='my-react-view')
    ]
    ```

1. This framework provides window.props, which contains a javascript object that can be used to hydrate your react state. This has the shape of::
    ```javascript
    window.props = {"objects": {"appname.modelname": {"https://example.com/appname/modelname/1/": {object as serialized by your model serializer}} } }
    ```

1. Start the development server and visit http://127.0.0.1:8000/ and visit your page to see you're react component in action
