# Full Stack Trivia API Backend

## Introduction 

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a  regular basis and created a  web page to manage the trivia app and play the game.

The application has the following features:

1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

- **Base URI:** Currently, this application runs on a local host. The default URI is `http://127.0.0.1:5000/`. Also, this URI is set as a proxy in the front end configuration.
- **Authentication:** There is no authentication implemented whatsoever. However, it's expected to be implemented in a future version.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Error Handling

There are multiple errors handled in this application. The errors are raised and returned as JSON objects like follows:

`{`

` 		"success": False,`

` 	"error": 400, `

`	"message": "bad request"`

`}`

This application is implemented to account for four different error types according to the failing request:

- 400: Bad request
- 404: Resource not found
- 405: Method not allowed
- 422: Unprocessable request



## Endpoints 

##### GET /categories

- **General:** 
  - Returns a list of all available categories, number of categories, and a success value.
- **Sample:** `curl http://127.0.0.1:5000/categories`

```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "success": true, 
  "total_categories": 6
}
```

## 

##### GET /questions

- **General:** 
  - Returns a list of all  questions, number of questions, categories and a success value.
  - Results are paginated in groups of 10, including a request argument to specify the page number, starting from 1.
- **Sample:** `curl http://127.0.0.1:5000/questions?page=1`

```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, ...// 10 questions per page
  ], 
  "success": true, 
  "total_questions": 21
}

```

##### POST /questions

- **General:** 
  - Creates a new question, using the submitted question, answer, difficulty and category.
  - Returns the id of created question, questions, number of questions, categories and a success value.
  - Results are also paginated in groups of 10, including a request argument to specify the page number, starting from 1.
- **Sample:** `curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the number of bones in the skeleton of an adult human?", "answer": "206", "difficulty": "4", "category": "1"}' http://127.0.0.1:5000/questions`

```javascript
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "created": 57, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
 ...
  ], 
  "success": true, 
  "total_questions": 22
}
```



##### DELETE /questions/{question_id}

- **General:** 

  - Deletes the question with the given id if it exists.
  - Returns the id of deleted question, questions, number of questions, categories and a success value.

- **Sample:** 

  `curl -X DELETE http://127.0.0.1:5000/questions/10`



##### POST /questions/search

- **General:** 

  - Filters any questions for whom the search term is a substring of the question .

  - Returns the filtered questions, number of filtered questions, categories and a success value.

    

## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```