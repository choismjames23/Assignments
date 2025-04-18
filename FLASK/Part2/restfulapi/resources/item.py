from flask import request
from flask_restful import Resource

items = [] #DB의 임시 역할

class Item(Resource):
    # 특정 아이템 조회
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return item
        return {"msg":"Item Not Found"}, 404 #msg, response code

    # 아이템 생성
    def post(self, name):
        for item in items:
            if item['name'] == name:
                return {"msg":"Item Already Exists"}, 400
            
        data = request.get_json()
        new_item = {'name':data['name'],'price':data['price']}
        items.append(new_item)

        return new_item

    # 아이템 업데이트
    def put(self, name):
        data = request.get_json

        for item in items:
            if item['name'] == name:
                item['price'] = data['price']
                return item
            
        #만약 업데이트 하고자하는 아이템 데이터가 없다면 -> 추가한다
        new_item = {'name':data['name'],'price':data['price']}
        items.append(new_item)

        return new_item
    
    # 아이템 삭제
    def delete(self, name):
        global items

        itmes = [item for item in items if item['name']!=name]


        return {"msg": "Item Deleted"}