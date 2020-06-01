from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Actor, Movie

ROWS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app  
  app = Flask(__name__)
  setup_db(app)

  # CORS (API configuration)
  CORS(app)

  # CORS Headers 
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response


  # Pagination concept
  def paginate_results(request, selection):
 
    # Get page from request. If not given, default to 1
    page = request.args.get('page', 1, type=int) 
    start =  (page - 1) * ROWS_PER_PAGE
    end = start + ROWS_PER_PAGE

    # Format the selection into list of dicts 
    rows_formatted = [rows.format() for rows in selection]
    return rows_formatted[start:end]

  
  #***************************************************************************************************
  # API Endpoints:  #  For explanation of each  endpoints, please have look at the README file . 
  #***************************************************************************************************

  #***************************************************************************************************
  # Basic endpoint url
  #***************************************************************************************************
  @app.route('/')
  def welcome():        
     return ('Welcome to Renga Casting agency')

  #***************************************************************************************************
  # Endpoint for '/actors' with all methods GET/POST/DELETE/PATCH.   
  #***************************************************************************************************
  
  # GET method
  @app.route('/actors', methods=['GET'])
  @requires_auth('view:actors')
  def get_actors(payload):
    #Returns paginated actors object

    selection = Actor.query.order_by(Actor.id).all()
    actors_paginated = paginate_results(request, selection)

    if len(actors_paginated) == 0:
      abort(404, {'message': 'Actors database is empty'})

    return jsonify({
      'success': True,
      'actors': actors_paginated,
      'total_actors': len(selection)
    })

  # POST method
  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actors')
  def insert_actors(payload):
 
    # Get request json
    body = request.get_json()

    if not body:
          abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Extract name and age value and gender from request body, if not present set default values
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', 'Other')

    # abort if one of these are missing with appropiate error message
    if (name is None):
      abort(422, {'message': 'name is not provided.'})

    if (age is None):
      abort(422, {'message': 'age is not provided.'})

    # Create new instance of Actor & Insert it and display the id of the inserted actor
    new_actor = (Actor(
          name = name, 
          age = age,
          gender = gender
          ))
    new_actor.insert()

    return jsonify({
      'success': True,
      'created': new_actor.id
    })

  # DELETE method
  @app.route('/actors/<actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, actor_id):
 
    # Abort if no actor_id has been provided
    if not actor_id:
      abort(400, {'message': ' actor id not provided in the request url.'})
  
    # Fetch the actor which should be deleted by id
    actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

    # If no actor with given id could found, abort 404
    if actor_to_delete is None:
        abort(404, {'message': 'Actor id {} not found in database.'.format(actor_id)})
    
    # Delete actor from database . Return success and id of the deleted actor
    actor_to_delete.delete()    
    
    return jsonify({
      'success': True,
      'deleted': actor_id
    })

  # PATCH method
  @app.route('/actors/<actor_id>', methods=['PATCH'])
  @requires_auth('modify:actors')
  def edit_actors(payload, actor_id):

    # Get request json
    body = request.get_json()

    # Abort if no actor_id or body has been provided
    if not actor_id:
      abort(400, {'message': 'please provide actor id in the request url.'})

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Fetch the actor which should be updated based on its id
    update_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    # Abort 404 if no actor with this id exists
    if update_actor is None:
      abort(404, {'message': 'Actor id {} not found in database.'.format(actor_id)})

    # Update only the given fields and retain the remaining fields
    name = body.get('name', update_actor.name)
    age = body.get('age', update_actor.age)
    gender = body.get('gender', update_actor.gender)

    # Set new field values and update actor with new values
    update_actor.name = name
    update_actor.age = age
    update_actor.gender = gender
    update_actor.update()

    # Return success, updated actor id and updated actor as formatted list
    return jsonify({
      'success': True,
      'updated': update_actor.id,
      'actor' : [update_actor.format()]
    })

  #***************************************************************************************************
  # Endpoint /movies for all methods GET/POST/DELETE/PATCH
  #***************************************************************************************************
  
  # GET method
  @app.route('/movies', methods=['GET'])
  @requires_auth('view:movies')
  def get_movies(payload):
 
    selection = Movie.query.order_by(Movie.id).all()
    movies_paginated = paginate_results(request, selection)

    if len(movies_paginated) == 0:
      abort(404, {'message': 'no movies found in database.'})

    return jsonify({
      'success': True,
      'movies': movies_paginated,
      'total_movies': len(selection)
    })

  # POST method
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movies')
  def insert_movies(payload):
 
    # Get request json
    body = request.get_json()

    if not body:
          abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Extract title and release_date value from request body
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    # abort if one of these are missing with appropiate error message
    if title is None:
      abort(422, {'message': 'title is not provided.'})

    if release_date is None:
      abort(422, {'message': 'release_date is not provided.'})

    # Create new instance of movie & insert it.
    new_movie = (Movie(
          title = title, 
          release_date = release_date
          ))
    new_movie.insert()

    return jsonify({
      'success': True,
      'created': new_movie.id      
    })
  
  # DELETE method
  @app.route('/movies/<movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, movie_id):
  
    # Abort if no movie_id has been provided
    if not movie_id:
      abort(400, {'message': 'please provide movie id to the request url.'})
  
    # Fetch the movie which should be deleted by id
    movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

    # If no movie with given id could found, abort 404
    if not movie_to_delete:
        abort(404, {'message': 'Movie id {} not found in database.'.format(movie_id)})
    
    # Delete movie from database
    movie_to_delete.delete()
    
    # Return success and id from deleted movie
    return jsonify({
      'success': True,
      'deleted': movie_id
    })

  # PATCH method
  @app.route('/movies/<movie_id>', methods=['PATCH'])
  @requires_auth('modify:movies')
  def edit_movies(payload, movie_id):

    # Get request json
    body = request.get_json()

    # Abort if no movie_id or body has been provided
    if not movie_id:
      abort(400, {'message': 'please provide movie id in the request url.'})

    if not body:
      abort(400, {'message': 'request does not contain a valid JSON body.'})

    # Fetch the movie which should be updated by based on its id
    movie_to_update = Movie.query.filter(Movie.id == movie_id).one_or_none()

    # Abort 404 if no movie with this id exists
    if not movie_to_update:
      abort(404, {'message': 'Movie id {} not found in database.'.format(movie_id)})

    # Extract title and age value from request body
    # If not given, set existing field values, so no update will happen
    title = body.get('title', movie_to_update.title)
    release_date = body.get('release_date', movie_to_update.release_date)

    # Set new field values
    movie_to_update.title = title
    movie_to_update.release_date = release_date

    # Delete movie with new values
    movie_to_update.update()

    # Return success, updated movie id and updated movie as formatted list
    return jsonify({
      'success': True,
      'edited': movie_to_update.id,
      'movie' : [movie_to_update.format()]
    })
  
  
  #***************************************************************************************************
  # Error Handlers
  #***************************************************************************************************
  # Error message processing concept(Generated message or default message)
  def get_error_message(error, default_text): 
    try:
        # Return message contained in error, if possible
        return error.description['message']
    except:
        # otherwise, return given default text
        return default_text 

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": get_error_message(error, "bad request")
                      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message":  get_error_message(error, "resource not found")
                      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": get_error_message(error,"unprocessable")
                      }), 422

  @app.errorhandler(AuthError)

  def authentification_failed(AuthError): 
      return jsonify({
                      "success": False, 
                      "error": AuthError.status_code,
                      "message": AuthError.error['description']
                      }), AuthError.status_code


  #  return app
  return app

app = create_app()

if __name__ == '__main__':
    app.run()