from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yaml

def read_config(file_path):
    """读取配置文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

app = Flask(__name__)
config = read_config('Python/AI-Introduction-Project/database/config.yaml')
path = 'sqlite:///'+ config
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class KeyValue(db.Model):
    tablename = db.Column(db.String(120), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    description = db.Column(db.String(120))
    added_message = db.Column(db.String(120))

    def to_dict(self):
        """将对象转换为字典"""
        tmp={
            'table': self.tablename,
            'key': self.key,
            'value': []
        }
        if self.name:
            tmp['value'].append(self.name)
        if self.start_time:
            tmp['value'].append(self.start_time)
        if self.end_time:
            tmp['value'].append(self.end_time)
        if self.description:
            tmp['value'].append(self.description)
        if self.added_message:
            tmp['value'].append(self.added_message)
        return tmp

with app.app_context():
    db.create_all()

@app.route('/<string:tablename>', methods=['POST'])
def add(tablename):
    """添加值"""
    key = request.json.get('key')
    value = request.json.get('value', [])
    if not value or len(value) > 5:
        return jsonify({'error': 'Value is a list of max 5 elements'}), 400
    
    kv = KeyValue.query.filter_by(key=key,tablename=tablename).first()
    if kv != None:
        return jsonify({'error': 'Key is already existed'}), 400
    kv = KeyValue(
        tablename=tablename,
        key=key,
        name=value[0],
        start_time=value[1],
        end_time=value[2],
        description=value[3],
        added_message=value[4]
    )
    db.session.add(kv)
    db.session.commit()
    return jsonify(kv.to_dict()), 201

@app.route('/by_table/<string:table>', methods=['GET'])
def get_by_table(table):
    """根据table获取所有该类型的值"""
    kv = KeyValue.query.filter_by(tablename=table).all()
    if kv:
        return jsonify([i.to_dict() for i in kv])
    return jsonify({'error': 'Table not found'}), 404

@app.route('/by_key/<string:table>/<string:key>', methods=['GET'])
def get_by_id(table,key):
    """根据table和key获取值"""
    kv = KeyValue.query.filter_by(key=key,tablename=table).first()
    if kv:
        return jsonify(kv.to_dict())
    return jsonify({'error': 'Table or Key not found'}), 404

@app.route('/put/<string:table>/<string:key>', methods=['PUT'])
def update(table,key):
    """根据Table和唯一的key更新"""
    value = request.json.get('value', [])
    if not value or len(value) > 5:
        return jsonify({'error': 'Value is a list of max 5 elements'}), 400
    kv = KeyValue.query.filter_by(key=key,tablename=table).first()
    if not kv:
        return jsonify({'error': 'Table or Key not found'}), 404
    
    while(len(value)<5):
        value.append()
    kv.name = value[0]
    kv.start_time = value[1]
    kv.end_time = value[2]
    kv.description = value[3]
    kv.added_message = value[4]
    db.session.commit()
    return jsonify(kv.to_dict())

@app.route('/delete/<string:table>/<string:key>', methods=['DELETE'])
def delete_kv(table,key):
    """根据Table和唯一的key删除"""
    kv = KeyValue.query.filter_by(key=key,tablename=table).first()
    if not kv:
        return jsonify({'error': 'Table or Key not found'}), 404
    db.session.delete(kv)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)