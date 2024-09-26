import json
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'it238project'
app.config['MYSQL_DB'] = 'guessit'
mysql = MySQL(app)

'''
employees = [ 
    { 'id': 1, 'name': 'Ashley' }, 
    { 'id': 2, 'name': 'Kate' }, 
    { 'id': 3, 'name': 'Joe' }
    ]

nextEmployeeId = 4


@app.route('/employees', methods=['GET'])

def get_employees():
    return jsonify(employees)


@app.route('/employees/<int:id>', methods=['GET'])

def get_employee_by_id(id: int):
    employee = get_employee(id)

    if employee is None:
        return jsonify({ 'error': 'Employee does not exist'}), 404
    return jsonify(employee)

def get_employee(id):
    return next((e for e in employees if e['id'] == id), None)


def employee_is_valid(employee):
    print(employee.keys())
    for key in employee.keys():
        print(key)
        if key != 'name':
            return False
    return True


@app.route('/employees', methods=['POST'])

def create_employee():
    global nextEmployeeId
    
    employee = json.loads(request.data)
    print(employee)
    
    if not employee_is_valid(employee):
        return jsonify({'error': 'Invalid employee properties'}), 400
    
    print(employee)
    employee['id'] = nextEmployeeId
    print(employee)
    nextEmployeeId += 1
    employees.append(employee)

    return '', 201, { 'location': f'/employees/{employee["id"]}' }


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({ 'error': 'Employee does not exist.' }), 404
    
    #print(employee)
    updated_employee = json.loads(request.data)
    print(updated_employee)
    if not employee_is_valid(updated_employee):
        return jsonify({ 'error', 'Invalid employee properties'}), 400
    
    #print(employee)
    employee.update(updated_employee)
    #print(employee)

    return jsonify(employee)

'''


@app.route('/questions', methods=['GET'])
def get_questions():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT a.questionCode as questionCode, a.questionDesc as questionDesc, 
                   a.categoryCode as categoryCode, b.categoryDesc,
                   a.difficultyCode as difficultyCode, c.difficultyDesc
                   FROM questions a 
                   INNER JOIN categories b ON a.categoryCode=b.categoryCode  
                   INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode
               ''')
    
    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    #data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/questions/<int:id>', methods=['GET'])
def get_questions_by_id(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT a.questionCode as questionCode, a.questionDesc as questionDesc, 
                   a.categoryCode as categoryCode, b.categoryDesc,
                   a.difficultyCode as difficultyCode, c.difficultyDesc
                   FROM questions a 
                   INNER JOIN categories b ON a.categoryCode=b.categoryCode  
                   INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode WHERE a.questionId = %s''', (id,))
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return jsonify(data)


@app.route('/search/question', methods=['GET'])
def get_question_by_category():

    args = request.args
    #print(args)
    categoryCode = args.get('categoryCode')

    if categoryCode is None:
        return jsonify({'error': 'category code query parameter is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute('''SELECT a.questionCode, a.questionDesc, 
                   b.answerCode, b.answerDesc, b.isCorrect, a.difficultyCode, c.timer,
                   a.seq as questionSeq, b.seq as answerSeq, d.categoryDesc, a.categoryCode
                   FROM questions a
                   INNER JOIN answers b ON a.questionCode=b.questionCode
                   INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode
                   INNER JOIN categories d ON a.categoryCode=d.categoryCode
                   WHERE a.categoryCode = %s
                   ORDER BY a.seq, b.seq ASC
                   ''', (categoryCode,))
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    return jsonify(data)


@app.route('/categories', methods=['GET'])
def get_categories():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT a.categoryId, a.categoryCode, a.categoryDesc
                   FROM categories a
                   ORDer BY a.seq
               ''')
    
    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    #data = cur.fetchall()
    cur.close()
    return jsonify(data)

    
if __name__ == '__main__':
    app.run(port=5000, debug=True)