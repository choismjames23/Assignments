from flask import request, jsonify, render_template
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint(
        "posts",
        __name__,
        description="posts api",
        url_prefix='/posts'
    )

    @posts_blp.route('/', methods=['GET','POST'])
    def posts():
        cursor = mysql.connection.cursor()

        #게시글 조회 (GET)
        if request.method == 'GET':
            sql = "SELECT * FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            #API 요청이 아니라 HTML을 렌더링하는 경우   
            if request.accept_mimetypes.best_match(['application/json','text/html']) == 'text/html':
                post_list = [{'id': post[0], 'title':post[1], 'content': post[2]} for post in posts]
                return render_template('posts.html', posts=post_list)
            
            #JSON으로 변환 
            return jsonify([{'id': post[0], 'title':post[1], 'content': post[2]} for post in posts])
        
        #게시글 생성 (POST)
        elif request.method == 'POST':
            title = request.json.get("title")
            content = request.json.get("content")

            if not title or not content:
                abort(400, message="title 또는 content가 없습니다")

            sql = "INSERT INTO posts(title, content) VALUE(%s, %s)"
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({"message":"success"}), 201
    
    #게시글 상세 조회
    #게시글 수정 및 삭제
    @posts_blp.route("/<int:id>", methods=['GET','PUT','DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()

        if request.method == 'GET':
            sql = f'SELECT * FROM posts WHERE id={id}'
            cursor.execute(sql)
            post = cursor.fetchone()

            if not post:
                abort(404, message='해당 게시글이 없습니다.')
            return {
                'id': post[0],
                'title': post[1],
                'content': post[2],
            }
        
        #게시글 수정
        elif request.method == 'PUT':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message='title 또는 content가 없습니다.')

            sql = "SELECT * FROM posts WHERE id=%s"
            cursor.execute(sql, (id,))
            post = cursor.fetchone()

            if not post:
                abort(400, message='해당 게시글이 없습니다.')

            sql = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
            cursor.execute(sql, (title, content, id))
            mysql.connection.commit()

            return jsonify({'message': 'Successfully updated title & content'})
        
        #게시글 삭제
        elif request.method == 'DELETE':
            sql = "SELECT * FROM posts WHERE id=%s"
            cursor.execute(sql, (id,))
            post = cursor.fetchone()

            if not post:
                abort(400, message='해당 게시글이 없습니다.')

            sql = "DELETE FROM posts WHERE id=%s"
            cursor.execute(sql, (id,))
            cursor.connection.commit()

            return jsonify({'message': 'Successfully deleted post'})
        
    return posts_blp