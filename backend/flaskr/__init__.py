import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  formatted_questions = questions[start:end]

  return formatted_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r'/*': {'origins': '*'}})

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    return response

  '''
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.all()

      if len(categories) == 0:
        abort(404)

      # format categories as an array of category types (not id)
      formatted_categories = [c.format()['type'] for c in categories]

      return jsonify({
        'success': True,
        'categories': formatted_categories,
        'total_categories': len(formatted_categories)
      })
    except:
      abort(404)

  '''
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  # Handling both get and post requests for getting or creating questions
  @app.route('/questions', methods=['GET', 'POST'])
  def get_create_questions():

    # get paginated questions
    if request.method == 'GET':
      try:
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
          abort(404)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(selection),
          'categories': [c.format()['type'] for c in Category.query.all()]
        })
      except:
        abort(404)
    
      '''
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    # create new question
    if request.method == 'POST':
      body = request.get_json()
      new_question = body.get('question', None)
      new_answer = body.get('answer', None)
      new_difficulty = body.get('difficulty', None)
      new_category = int(body.get('category', None))+1

      try:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=str(new_category))
        
        # making sure the answer is not empty
        if question.answer == None:
          abort(422)

        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)


        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(selection),
          'categories': [c.format()['type'] for c in Category.query.all()]
        })

      except:
        abort(422)
      

  '''
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      # making sure the question is not none, before deletion
      if question is None:
        abort(422)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(selection),
        'categories': [c.format()['type'] for c in Category.query.all()]
      })

    except:
      abort(422)



  '''
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def get_filtered_questions():
    try:
      query = request.get_json().get('searchTerm', None)

      if query is None:
        abort(400)

      # filtering out the questions with ilike to account for case-insensitivity
      result = Question.query.filter(Question.question.ilike('%{}%'.format(query))).all()
      current_questions = paginate_questions(request, result)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(result),
        'categories': [c.format()['type'] for c in Category.query.all()]
      })
    except:
      abort(400)

  '''
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):

    try:
      # adding 1 to category_id as they start from 1 not 0, in the database
      selection = Question.query.filter(Question.category==str(category_id+1)).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)
      current_category = Category.query.filter(Category.id==category_id+1).one_or_none().format()

      # if len(current_questions) == 0:
      #   abort(404)

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(selection),
        'current_category': current_category,
        'categories': [c.format()['type'] for c in Category.query.all()]
      })

    except:
      abort(404)

  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    quiz_category = body.get('quiz_category', None)
    previous_questions = body.get('previous_questions', None)
    print(quiz_category)

    try:
      # if All is clicked instead of a specific category, to take the quiz with all questions from all categories
      if quiz_category['type'] == 'click':
        category_questions = Question.query.all()

      else:
        category_questions = Question.query.filter(Question.category == quiz_category['id']).all()

      formatted_questions = [q.format() for q in category_questions]
      num_questions = len(formatted_questions)

      # making sure the questions are chosen randomly, and without repeating 
      for i in random.sample(range(num_questions), num_questions):
        if formatted_questions[i]['id'] not in previous_questions:
          current_question = formatted_questions[i]
          break
      
      # the current_question is set to None if all questions were attempted to end the quiz (take care of questionsPerPlay/forceEnd in the front end)
      if num_questions == len(previous_questions):
        current_question = None


      return jsonify({
        'success': True,
        'question': current_question
      })

    except:
      abort(404)

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Resource not found"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': "Method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable request"
    }), 422
  



  return app

    