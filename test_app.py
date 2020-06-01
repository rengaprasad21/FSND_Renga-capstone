import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from datetime import date

#----------------------------------------------------------------------------#
# Setup of Unittest cases
#----------------------------------------------------------------------------#

class CastAgencyTestCase(unittest.TestCase):
 
    def setUp(self):

                            
        # Retrieve from all environment variables
        self.assistant_auth_header= {'Authorization' : 'Bearer ' + os.environ['assistant_token']}
        self.director_auth_header = {'Authorization' : 'Bearer ' + os.environ['director_token']}
        self.producer_auth_header = {'Authorization' : 'Bearer ' + os.environ['producer_token']}
        self.database_path = os.environ['DATABASE_URL']

        #Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
      
        # All Test data defined here
        self.json_post_actor = {
            'name' : 'kamal',
            'age' : 25
        } 

        self.json_post_actor_without_name = {
            'age' : 25
        }

        self.json_patch_actor_with_new_age = {
            'age' : 30
        } 

        self.json_post_movie = {
            'title' : 'Anbe Sivam',
            'release_date' : date.today()
        }

        self.json_post_movie_without_title = {
            'release_date' : date.today()
        }

        self.json_patch_movie = {
            'release_date' : date.today()
        } 
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

 
    def tearDown(self):
        """Executed after reach test"""
        pass

#*************************************************************************
# Unit Tests for Endpoint /actor
#*************************************************************************

# Cases wrt GET method 
    #Positive case
    def test_get_actors(self):
        res = self.client().get('/actors?page=1', headers = self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    # Negative cases
    # GET actors w/o Authorization header
    def test_error_401_get_actors(self):
       
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

     # GET actors with invalid pgae number
    def test_error_404_get_actors(self):
        """Test Error GET all actors."""
        res = self.client().get('/actors?page=9999', headers = self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actors database is empty')

# Cases wrt POST method 
    #Positive case
    def test_post_new_actor(self):
        actors_before = Actor.query.all()

        res = self.client().post('/actors', json = self.json_post_actor, headers = self.director_auth_header)
        data = json.loads(res.data)

        actors_after = Actor.query.all()

        actor = Actor.query.filter_by(id=data['created']).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(actors_after) - len(actors_before) == 1)      
        self.assertIsNotNone(actor)
    
    # Negative cases
    # POST actors w/o Authorization header
    def test_error_401_new_actor(self):
      
        res = self.client().post('/actors', json = self.json_post_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # POST actors without column name
    def test_error_422_post_new_actor(self):
              
        res = self.client().post('/actors', json = self.json_post_actor_without_name, headers = self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'name is not provided.')


# Cases wrt DELETE method 
    #Positive case - DELETE existing actor by Creating new actor and Deleting the same actor
    def test_delete_actor(self):
       
        res = self.client().post('/actors', json = self.json_post_actor, headers = self.director_auth_header)
        data = json.loads(res.data)

        actor_id= data['created']
        res = self.client().delete('/actors/{}'.format(actor_id), headers = self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'],format(actor_id))

    # Negative cases
    # DELETE existing actor without appropriate permission
    def test_error_403_delete_actor(self):
        
        res = self.client().delete('/actors/1', headers = self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    # DELETE non existing actor
    def test_error_404_delete_actor(self):
 
        res = self.client().delete('/actors/15125', headers = self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor id 15125 not found in database.')

# Cases wrt PATCH method 
    #Positive case - Modify details(age) of existing actor 
    def test_patch_actor(self):
               
        res = self.client().patch('/actors/1', json = self.json_patch_actor_with_new_age, headers = self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 1)

    # Negative cases
    # PATCH without any inputs
    def test_error_400_patch_actor(self):
           

            res = self.client().patch('/actors/99999', headers = self.director_auth_header)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 400)
            self.assertFalse(data['success'])
            self.assertEqual(data['message'] , 'request does not contain a valid JSON body.')

    # PATCH with non valid id
    def test_error_404_patch_actor(self):
              
        res = self.client().patch('/actors/99999', json = self.json_patch_actor_with_new_age, headers = self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Actor id 99999 not found in database.')



#*************************************************************************
# Unit Tests for Endpoint /movie
#*************************************************************************

# Cases wrt GET method 
    #Positive case
    def test_get_movies(self):
        res = self.client().get('/movies?page=1', headers = self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    #Negative cases
    # GET  movies w/o Authorization.
    def test_error_401_get_movies(self):
      
        res = self.client().get('/movies?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # GET movies with invalid page number
    def test_error_404_get_movies(self):
       
        res = self.client().get('/movies?page=1234', headers = self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'no movies found in database.')


# Cases wrt POST method 
    #Positive case
    def test_post_new_movie(self):
        """Test POST new movie."""
        movies_before = Movie.query.all()
       
        res = self.client().post('/movies', json = self.json_post_movie, headers = self.producer_auth_header)
        data = json.loads(res.data)

        movies_after = Movie.query.all()
        movie = Actor.query.filter_by(id=data['created']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(movies_after) - len(movies_before) == 1)      
        self.assertIsNotNone(movie)

    #Negative case
    #POST movies without title
    def test_error_422_post_new_movie(self):
        """Test Error POST new movie."""

        res = self.client().post('/movies', json = self.json_post_movie_without_title, headers = self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'title is not provided.')

# Cases wrt DELETE method 
    #Positive case - DELETE existing movie by Creating new movie and Deleting the same movie 
    def test_delete_movie(self):
       
        res = self.client().post('/movies', json = self.json_post_movie, headers = self.producer_auth_header)
        data = json.loads(res.data)
        
        movie_id=data['created']

        res = self.client().delete('/movies/{}'.format(movie_id), headers = self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], format(movie_id))

    #Negative case
    # DELETE existing movie w/o Authorization
    def test_error_401_delete_movie(self):
    
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')


    #DELETE non existing movie_id
    def test_error_404_delete_movie(self):
     
        res = self.client().delete('/movies/9999', headers = self.producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie id 9999 not found in database.')

# Cases wrt PATCH method
    #Positive case -PATCH existing movies
    def test_patch_movie(self):
        
      
        res = self.client().patch('/movies/1', json = self.json_patch_movie, headers = self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)
        self.assertEqual(data['edited'], 1)
    
    #Negative case
    #  PATCH without any inputs(body)
    def test_error_400_patch_movie(self):

        res = self.client().patch('/movies/1', headers = self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'request does not contain a valid JSON body.')

    # PATCH with invalid movie_id
    def test_error_404_patch_movie(self):
        
      
        res = self.client().patch('/movies/9999', json = self.json_patch_movie, headers = self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Movie id 9999 not found in database.')



# run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()