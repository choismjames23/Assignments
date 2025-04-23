from flask import request, jsonify
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Todo, User, db

todo_blp = Blueprint('todo', 'todo', url_prefix='/todo', description='Operations on todos')


@todo_blp.route('/', methods=['POST'])
@jwt_required()
def create_todo():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    title = request.json.get('title', None)

    if not title:
        return jsonify({"msg": "Missing title"}), 400

    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()

    new_todo = Todo(title=title, user_id=user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"msg": "Todo created", "id": new_todo.id}), 201

# Todo 조회 (GET)
@todo_blp.route('/', methods=['GET'])
@jwt_required()
def get_todos():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    todos = Todo.query.filter_by(user_id=user.id).all()
    return jsonify([{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos])

# Todo 수정 (PUT)
@todo_blp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    # 요청에서 제목을 가져옴
    title = request.json.get('title', None)
    completed = request.json.get('completed', None)

    if title:
        todo.title = title
    if completed is not None:
        todo.completed = completed

    db.session.commit()

    return jsonify({"msg": "Todo updated", "id": todo.id, "title": todo.title, "completed": todo.completed})



# Todo 완료 상태 변경 (PUT)
@todo_blp.route('/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    # 요청에서 completed 값을 가져옴
    completed = request.json.get('completed', None)

    if completed is not None:
        todo.completed = completed
        db.session.commit()
        return jsonify({"msg": "Todo updated", "id": todo.id})

    return jsonify({"msg": "Completed value is missing"}), 400

# Todo 삭제 (DELETE)
@todo_blp.route('/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"msg": "Todo deleted", "id": todo_id})