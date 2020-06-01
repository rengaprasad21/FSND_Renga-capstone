# FSND: Renga Casting agency(Capstone project)
The Casting Agency is a company that is responsible for managing movies and actors .Executive Producer within the company is creating a system to simplify and streamline the management process.

## Content

1. [Description](#Description)
2. [Test Project locally](#Test-locally)
3. [API Documentation](#API)
4. [Authentication](#Authentication)

### Description & Covered Topics

This is the last project of the `Udacity-Full-Stack-Nanodegree` Course.It covers following technical topics in 1 app:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to performance CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentication with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`


### Test-locally

Make sure you `cd` into the correct folder (with all app files) before following the setup steps.
Also, you need the latest version of [Python 3](https://www.python.org/downloads/)
and [postgres](https://www.postgresql.org/download/) installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```bash
  $ python -m venv env
  $ source env/scripts/activate
  ```

2. Install the dependencies:
```bash
$ pip install -r requirements.txt
```

Running this project locally means that it can´t access `Herokus` env variables.
To fix this, you need to source few environemnt variables using  `setup.sh`, so it can
correctly connect to a local database

3. Change database config so it can connect to your local postgres database
- Open `setup.sh` with your editor of choice. 
- Here you can see this below environment variable:
 ```
 export DATABASE_URL='postgresql://postgres:1234@localhost:5432/cast_agency'
```
"sample format DATABASE_URL=postgresql://{}:{}@{}/{}".format('user_name',password,'port', database_name)"
 - Just change `user_name`, `password` and `port` to whatever you choose while installing postgres.
>_tip_: `user_name` usually defaults to `postgres` and `port` always defaults to `localhost:5432` while installing postgres, most of the time you just need to change the `password`.

4. Setup Auth0
If you only want to test the API (i.e. Project Reviewer), you can simply import Postman collection where all tokens are configured properly.


FYI: Here are the steps I followed to enable [Authentication](#Authentication).

5. Run the development server:
  ```bash 
  $ python app.py
  ```

6. (optional) To execute tests, run
```bash 
$ python test_app.py
```

### API 
# API Documentation
<a name="api"></a>

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL

**https://renga-cast-agency.herokuapp.com**
Response:"Welcome to Casting agency"

### Authentication

Please see [API Authentication](#Authentication-bearer)

### Available Endpoints

Here is a short table about which resources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | PATCH  |
                    |------|-------|---------|--------|
      /actors       |  [X] |  [x]  |   [x]   |   [x]  |   
      /movies       |  [x] |  [x]  |   [x]   |   [x]  |   

### How to work with each endpoint

Click on a link to directly get to the resource.

1. Actors
   1. [GET /actors](#get-actors)
   2. [POST /actors](#post-actors)
   3. [DELETE /actors](#delete-actors)
   4. [PATCH /actors](#patch-actors)
2. Movies
   1. [GET /movies](#get-movies)
   2. [POST /movies](#post-movies)
   3. [DELETE /movies](#delete-movies)
   4. [PATCH /movies](#patch-movies)

Each resource documentation is clearly structured:
1. Description in a few words
2. API can be tested via Postman collection by importing cast_agency.postman_collection or it can tested via CURL(details given below)
3. More descriptive explanation of input & outputs.
4. Required permission
5. Example Response.
6. Error Handling (`curl` command to trigger error + error response)


### get-actors

Query paginated actors.

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/actors?page=1
```


#### Example response
```js
{
  "actors": [
    {
      "age": 29,
      "gender": "Male",
      "id": 1,
      "name": "Kamal"
    }
  ],
  "success": true
}
```
#### Errors
If you try fetch a page which does not have any actors, you will encounter an error which looks like this:

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/actors?page=99999
```

will return

```js
{
  "error": 404,
  "message": "no actors found in database.",
  "success": false
}
```

### post-actors

Insert new actor into database.

```bash
$ curl -X POST https://renga-cast-agency.herokuapp.com/actors
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `name` (<span style="color:red">*</span>required)
       2. **integer** `age` (<span style="color:red">*</span>required)
       3. **string** `gender`
- Requires permission: `create:actors`
- Returns: 
  1. **integer** `id from newly created actor`
  2. **boolean** `success`
  3. **integer** `total_actors`

#### Example response
```js

{
    "created": 5,
    "success": true,
    `total_actors`:<total number of actors in database>
}

```
#### Errors
If you try to create a new actor without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/actors?page=123124
```

will return

```js
{
  "error": 422,
  "message": "no name provided.",
  "success": false
}
```

### patch-actors

Edit an existing Actor

```bash
$ curl -X PATCH https://renga-cast-agency.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to update`
- Request Headers: (_application/json_)
       1. **string** `name` 
       2. **integer** `age` 
       3. **string** `gender`
- Requires permission: `edit:actors`
- Returns: 
  1. **integer** `id from updated actor`
  2. **boolean** `success`
  3. List of dict of actors with following fields:
      - **integer** `id`
      - **string** `name`
      - **string** `gender`
      - **integer** `age`

#### Example response
```js
{
    "actor": [
        {
            "age": 30,
            "gender": "Other",
            "id": 1,
            "name": "renga"
        }
    ],
    "success": true,
    "updated": 1
}
```
#### Errors
If you try to update an actor with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://renga-cast-agency.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}
```
Additionally, trying to update an Actor with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}
```

### delete-actors

Delete an existing Actor

```bash
$ curl -X DELETE https://renga-cast-agency.herokuapp.com/actors/1
```

- Request Arguments: **integer** `id from actor you want to delete`
- Request Headers: `None`
- Requires permission: `delete:actors`
- Returns: 
  1. **integer** `id from deleted actor`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete actor with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://renga-cast-agency.herokuapp.com/actors/125
```

will return

```js
{
  "error": 404,
  "message": "Actor with id 125 not found in database.",
  "success": false
}
```

### get-movies

Query paginated movies.

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/movies?page=1
```
- Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
- Request Arguments: 
    - **integer** `page` (optional, 10 movies per page, defaults to `1` if not given)
- Request Headers: **None**
- Requires permission: `read:movies`
- Returns: 
  1. List of dict of movies with following fields:
      - **integer** `id`
      - **string** `name`
      - **date** `release_date`
  2. **boolean** `success`

#### Example response
```js
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Rajini first Movie"
    }
  ],
  "success": true
}

```
#### Errors
If you try fetch a page which does not have any movies, you will encounter an error which looks like this:

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/movies?page=123124
```

will return

```js
{
  "error": 404,
  "message": "no movies found in database.",
  "success": false
}
```

### post-movies

Insert new Movie into database.

```bash
$ curl -X POST https://renga-cast-agency.herokuapp.com/movies
```

- Request Arguments: **None**
- Request Headers: (_application/json_)
       1. **string** `title` (<span style="color:red">*</span>required)
       2. **date** `release_date` (<span style="color:red">*</span>required)
- Requires permission: `create:movies`
- Returns: 
  1. **integer** `id from newly created movie`
  2. **boolean** `success`
  3. **integer**  `total_movies`

#### Example response
```js
{
    "created": 5,
    "success": true
    `total_movies`:<total number of movies in database>
}
```
#### Errors
If you try to create a new movie without a requiered field like `name`,
it will throw a `422` error:

```bash
$ curl -X GET https://renga-cast-agency.herokuapp.com/movies?page=123124
```

will return

```js
{
  "error": 422,
  "message": "no name provided.",
  "success": false
}
```

### patch-movies

Edit an existing Movie

```bash
$ curl -X PATCH https://renga-cast-agency.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to update`
- Request Headers: (_application/json_)
       1. **string** `title` 
       2. **date** `release_date` 
- Requires permission: `edit:movies`
- Returns: 
  1. **integer** `id from updated movie`
  2. **boolean** `success`
  3. List of dict of movies with following fields:
        - **integer** `id`
        - **string** `title` 
        - **date** `release_date` 

#### Example response
```js
{
    "created": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
            "title": "Test Movie 123"
        }
    ],
    "success": true
}

```
#### Errors
If you try to update an movie with an invalid id it will throw an `404`error:

```bash
$ curl -X PATCH https://renga-cast-agency.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "Movie with id 125 not found in database.",
  "success": false
}
```
Additionally, trying to update an Movie with already existing field values will result in an `422` error:

```js
{
  "error": 422,
  "message": "provided field values are already set. No update needed.",
  "success": false
}
```

### delete-movies

Delete an existing movie

```bash
$ curl -X DELETE https://renga-cast-agency.herokuapp.com/movies/1
```

- Request Arguments: **integer** `id from movie you want to delete`
- Request Headers: `None`
- Requires permission: `delete:movies`
- Returns: 
  1. **integer** `id from deleted movie`
  2. **boolean** `success`

#### Example response
```js
{
    "deleted": 5,
    "success": true
}

```
#### Errors
If you try to delete movie with an invalid id, it will throw an `404`error:

```bash
$ curl -X DELETE https://renga-cast-agency.herokuapp.com/movies/125
```

will return

```js
{
  "error": 404,
  "message": "Movie with id 125 not found in database.",
  "success": false
}
```

# <a name="Authentication"></a>
## Authentication

All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to source it from 'setup.sh' accordingly

### Auth0 for locally use
#### Create an App & API

1. Login to https://manage.auth0.com/ 
2. Click on Applications Tab
3. Create Application
4. Give it a name like `movie` and select "Regular Web Application"
5. Go to Settings and find `domain`. 
6. Click on API Tab 
7. Create a new API:
   1. Name: `movie`
   2. Identifier `movie`
   3. Keep Algorithm as it is
8. Go to Settings and find `Identifier`. 
9. Source the environment variables  'AUTH0_DOMAIN','ALGORITHMS','API_AUDIENCE' using 'SETUP.SH' to run it locally and the same need to be added in Heroku config variables while deploying in Heroku server

#### Create Roles & Permissions

1. Before creating `Roles & Permissions`, you need to `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Also, check the button `Add Permissions in the Access Token`.
2. First, create a new Role under `Users and Roles` => `Roles` => `Create Roles`
3. Give it a descriptive name like `Casting Assistant`.
4. Go back to the API Tab and find your newly created API. Click on Permissions.
5. Create & assign all needed permissions accordingly 
6. After you created all permissions this app needs, go back to `Users and Roles` => `Roles` and select the role you recently created.
6. Under `Permissions`, assign all permissions you want this role to have. 


### Auth0 to use existing API
If you want to access the real, temporary API, import postman collections which contains the bearer tokens for all 3 roles are included in the `setup.sh` file.

## Existing Roles

They are 3 Roles with distinct permission sets:

1. Casting Assistant:
  - GET /actors (view:actors): Can see all actors
  - GET /movies (view:movies): Can see all movies
2. Casting Director (everything from Casting Assistant plus)
  - POST /actors (create:actors): Can create new Actors
  - PATCH /actors (edit:actors): Can edit existing Actors
  - DELETE /actors (delete:actors): Can remove existing Actors from database
  - PATCH /movies (edit:movies): Can edit existing Movies
3. Exectutive Dircector (everything from Casting Director plus)
  - POST /movies (create:movies): Can create new Movies
  - DELETE /movies (delete:movies): Can remove existing Motives from database

In your API Calls, add them as Header, with `Authorization` as key and the `Bearer token` as value. Don´t forget to also
prepend `Bearer` to the token (seperated by space).


```