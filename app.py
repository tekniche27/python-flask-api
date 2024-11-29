
import string
import random
import mariadb
from flask import Flask, jsonify, request
from flask_socketio import SocketIO,emit
from flask_cors import CORS


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")


# configuration used to connect to MariaDB
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootpass1234',
    'database': 'guessit'
}

@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)



@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)




@app.route('/questions', methods=['GET'])
def get_questions():
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
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
    conn.close()
    return jsonify(data)

@app.route('/questions/<int:id>', methods=['GET'])
def get_questions_by_id(id):
     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute('''SELECT a.questionCode as questionCode, a.questionDesc as questionDesc, 
                   a.categoryCode as categoryCode, b.categoryDesc,
                   a.difficultyCode as difficultyCode, c.difficultyDesc
                   FROM questions a 
                   INNER JOIN categories b ON a.categoryCode=b.categoryCode  
                   INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode WHERE a.questionId = %s''', (id,))
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)


@app.route('/search/question', methods=['GET'])
def get_question_by_category():

    args = request.args
    #print(args)
    categoryCode = args.get('categoryCode')

    if categoryCode is None:
        return jsonify({'error': 'category code query parameter is required'}), 400

     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
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
    conn.close()
    return jsonify(data)


@app.route('/categories', methods=['GET'])
def get_categories():
     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute('''SELECT a.categoryId, a.categoryCode, a.categoryDesc
                   FROM categories a
                   WHERE EXISTS(select 1 FROM questions b INNER JOIN answers c ON b.questionCode=c.questionCode WHERE a.categoryCode=b.categoryCode LIMIT 1)
                   ORDER BY a.seq
               ''')
    
    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    #data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/rooms', methods=['POST'])
def post_rooms():

    # using random.choices() generating random strings
    roomCode = ''.join(random.choices(string.ascii_letters, k=5)) # initializing size of string
    categoryCode = request.json['categoryCode']

    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO 
            guessit.rooms (
                roomCode,
                roomDesc,
                categoryCode)
        VALUES (%s,%s,%s)""", (roomCode, roomCode, categoryCode))
    
    #data = f"{cur.rowcount} details inserted"
    data = roomCode
    
    
    conn.commit() 
    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/rooms', methods=['GET'])
def get_room_by_roomCode():

    args = request.args
    roomCode = args.get('roomCode')

    if roomCode is None:
        return jsonify({'error': 'room code query parameter is required'}), 400

     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute('''SELECT a.roomCode, a.categoryCode 
                   FROM rooms a
                   WHERE a.roomCode = %s AND isActive=1
                   ''', (roomCode,))
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)


@app.route('/games', methods=['POST'])
def post_games():

    roomCode     = request.json['roomCode'] 
    clientId     = request.json['clientId']
    nickname     = request.json['nickname']

    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO 
            guessit.games (
                roomCode,
                clientId,
                nickname)
        VALUES (%s,%s,%s)""", (roomCode, clientId, nickname))
    
    #data = f"{cur.rowcount} details inserted"
    data = roomCode
    
    
    conn.commit() 
    cur.close()
    conn.close()

    return jsonify(data)


@app.route('/games', methods=['GET'])
def get_game_by_roomCode():

    args = request.args
    roomCode = args.get('roomCode')

    if roomCode is None:
        return jsonify({'error': 'room code query parameter is required'}), 400

     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute('''SELECT a.roomCode, a.clientId, a.nickname
                   FROM games a
                   INNER JOIN rooms b 
                   ON a.roomCode=b.roomCode
                   WHERE a.roomCode = %s AND isActive=1
                   ''', (roomCode,))
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)
    

@app.route('/room/questions', methods=['GET'])
def get_questions_by_roomCode():

    args = request.args
    roomCode = args.get('roomCode')

    if roomCode is None:
        return jsonify({'error': 'room code query parameter is required'}), 400

     # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # cur.execute('''SELECT a.questionDesc, 
    #                b.answerCode, b.answerDesc, b.isCorrect, a.difficultyCode, c.timer,
    #                a.seq as questionSeq, b.seq as answerSeq
    #                FROM questions a
    #                INNER JOIN answers b ON a.questionCode=b.questionCode
    #                INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode
    #                INNER JOIN categories d ON a.categoryCode=d.categoryCode
    #                LEFT JOIN rooms e ON a.categoryCode=e.categoryCode
    #                WHERE e.roomCode=%s
    #                ORDER BY a.seq, b.seq ASC
    #                ''', (roomCode,))
    
    #data = cur.fetchall()

    cur.execute('''SELECT DISTINCT
                    a.questionDesc, 
                    a.difficultyCode, d.categoryDesc, c.timer,
                    (select json_arrayagg(b.answerDesc)
                                 FROM answers b
                                 WHERE a.questionCode=b.questionCode
                                 ORDER BY b.seq ASC) as answerOptions,
                    (select f.answerDesc FROM answers f WHERE a.questionCode=f.questionCode and isCorrect=1) as answer
                    FROM questions a
                    INNER JOIN difficulties c ON a.difficultyCode=c.difficultyCode
                    INNER JOIN categories d ON a.categoryCode=d.categoryCode
                    LEFT JOIN rooms e ON a.categoryCode=e.categoryCode
                    WHERE e.roomCode=%s
                    ORDER BY a.seq ASC
                ''', (roomCode,))
    
    #data = cur.fetchall()

    data = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.close()
    conn.close()

    return jsonify(data)

@app.route('/games', methods=['PUT'])
def update_games():

    args = request.args
    roomCode = args.get('roomCode')
    clientId = args.get('clientId')
    score    = args.get('score')

    if roomCode is None:
        return jsonify({'error': 'room code query parameter is required'}), 400

    if clientId is None:
        return jsonify({'error': 'client id query parameter is required'}), 400

    if score is None:
        return jsonify({'error': 'score query parameter is required'}), 400

    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    cur.execute('''UPDATE games
                   SET score=%s
                   WHERE roomCode = %s AND clientId = %s
                   ''', (score,roomCode,clientId,))

    data = [{"result": str(cur.rowcount) + " record(s) affected."}]

    conn.commit()
    cur.close()
    conn.close()
    return jsonify(data)
    
 

if __name__ == '__main__':
    #app.run(port=5000, debug=True)
    socketio.run(app, debug=True,port=5001)