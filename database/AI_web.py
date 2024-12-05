from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from Trans import trans_to_chinese,trans_to_english

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/Code/Python/data.db'#data.db存储位置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #优化
db = SQLAlchemy(app)

#db 中每行都有id(唯一) ,key, (可选)start_time,end_time,description,added_message
class KeyValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    description = db.Column(db.String(120))
    added_message = db.Column(db.String(120))
    def to_dict(self):
        return {
            'id':self.id,
            'value':[self.key,self.start_time,self.end_time,self.description,self.added_message]
        }

with app.app_context():
    db.create_all()

# 添加值
@app.route('/', methods=['POST'])
def add():
    value = request.json['value'] 
    '''
        value is a List of [key,start_time(),end_time,Description,added message] len(value)==5
        E.g value=['成绩','20240905','20240905','94','English']
        all in string form
    '''
    if not value:
        return jsonify({'error': 'value are required'}), 400
    if len(value) != 5:
        return jsonify({'error': 'Value must be a list of 5 elements'}), 400
    key=trans_to_english(value[0]) #将key翻译为英文
    key=key.replace(' ','_') #去除空格
    kv = KeyValue(
        key=key,
        start_time=value[1],
        end_time=value[2],
        description=value[3],
        added_message=value[4]
    )
    db.session.add(kv)
    db.session.commit()
    return jsonify(kv.to_dict()), 201

#根据string key获取所有该类型的值
@app.route('/by_key/<string:key>', methods=['GET'])
def get_by_key(key):
    key=trans_to_english(key)
    key=key.replace(' ','_')
    kv = KeyValue.query.filter_by(key=key).all()
    if kv:
        return jsonify([i.to_dict() for i in kv])
    return jsonify({'error': 'Key not found'}), 404

#根据int id获取值
@app.route('/by_id/<int:id>', methods=['GET'])
def get_by_id(id):
    kv = KeyValue.query.filter_by(id=id).first()
    if kv:
        return jsonify(kv.to_dict())
    return jsonify({'error': 'Key not found'}), 404

# 根据唯一的id更新键值对
@app.route('/put/<int:id>', methods=['PUT'])
def update(id):
    value = request.json['value']
    if not value:
        return jsonify({'error': 'value are required'}), 400
    if len(value) != 5:
        return jsonify({'error': 'Value must be a list of 5 elements'}), 400
    kv = KeyValue.query.filter_by(id=id).first()
    if not kv:
        return jsonify({'error': 'id not found'}), 404
    kv.key=trans_to_english(value[0]).replace(' ','_')
    kv.start_time = value[1]
    kv.end_time = value[2]
    kv.description = value[3]
    kv.added_message = value[4]
    db.session.commit()
    return jsonify(kv.to_dict())

# 删除键值对
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_kv(id):
    kv = KeyValue.query.filter_by(id=id).first()
    if not kv:
        return jsonify({'error': 'Key not found'}), 404
    db.session.delete(kv)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)