from flask import Flask, jsonify, request
from flask_cors import CORS

import database.db as db


app = Flask(__name__)
CORS(app)

@app.route('/tasks')
def get_tasks():
    tasks = db.get_all_tasks()
    return jsonify(tasks), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    task_data = request.json
    task_created = db.insert_task(task_data['task_name'])
    if not task_created:
        return jsonify('something wrong'), 400
    return jsonify(task_created), 200

@app.route('/tasks/<int:task_id>', methods=["PUT"])
def update_task_complete(task_id):
    task_updated = db.update_task_complete(task_id)
    if not task_updated:
        return jsonify("not found"), 404

@app.route('/')
def health():
    return {"status": "ok"}

def run():
    app.run(host='0.0.0.0', port=8000)
