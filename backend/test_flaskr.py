import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.username = ''
        self.password = ''
        self.url = ''
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.username, self.password, self.url, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()


        # sample question to create
        self.new_question = {
            'question': 'What is the number of bones in the skeleton of an adult human?',
            'answer': '206',
            'difficulty': '4',
            'category': '1'
        }

        # sample qustion without answer that raises an error
        self.new_question_without_answer = {
            'question': 'What is the number of bones in the skeleton of an adult human?',
            'answer': None,
            'difficulty': '4',
            'category': '1'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET QUESTIONS
    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_invalid_page(self):
        result = self.client().get('/questions?page=50000')
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')

    # GET QUESTIONS BY CATEGORY
    def test_get_questions_by_category(self):
        result = self.client().get('/categories/3/questions') # make sure the category_id = 3 exists
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_invalid_category(self):
        result = self.client().get('/categories/599/questions') # make sure the category_id = 599 doesn't exist
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')
        

    # GET CATEGORIES
    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_requesting_specific_category(self):
        result = self.client().get('/categories/1') # test for an endpoint that doesn't exist
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')

    # CREATE QUESTIONS
    def test_create_new_question(self):
        result = self.client().post('/questions', json=self.new_question)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_422_create_question_without_answer(self):
        result = self.client().post('/questions', json=self.new_question_without_answer)
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable request')

    # DELETE QUESTIONS
    def test_delete_question(self):
        result = self.client().delete('/questions/11') # make sure the question_id = 11 exists in the database. Also, this test can be run once, after that the id should be changed to match an existing one
        data = json.loads(result.data)
        question = Question.query.filter(Question.id == 11).one_or_none()

        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], 11)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertIsNone(question)

    def test_422_delete_question_not_exist(self):
        result = self.client().delete('/questions/9999')
        data = json.loads(result.data)

        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable request')

    # SEARCH QUESTIONS
    def test_search_questions(self):
        result = self.client().post('/questions/search', json={'searchTerm': 'what'})
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))

    def test_400_search_with_empty_term(self):
        result = self.client().post('/questions/search', json={'searchTerm': None})
        data = json.loads(result.data)
        self.assertFalse(data['success'])
        self.assertEqual(result.status_code, 400)
        self.assertEqual(data['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()