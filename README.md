# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## babel + react + es2015 + watchify
npm install --save-dev babel-cli babel-preset-react react react-dom react-devtools
https://blog.yipl.com.np/how-to-get-started-with-react-using-watchify-and-babelify-f87b532d107d
https://jimdoescode.github.io/2015/07/18/npm-with-browserify-and-react.html

https://mae.chab.in/archives/2765
https://codeutopia.net/blog/2016/01/25/getting-started-with-npm-and-browserify-in-a-react-project/
http://easyreactbook.com/blog/react-fundamentals-configuring-browserify-babelify-and-react

https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## react router

https://stackoverflow.com/questions/34595890/react-router-undefined-history
libじゃないが
https://stackoverflow.com/questions/32816678/react-router-after-adding-createbrowserhistory-the-app-is-not-working-as-expect
https://github.com/ReactTraining/history
