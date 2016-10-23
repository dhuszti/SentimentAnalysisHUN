# Flask was used as REST API framework http://flask.pocoo.org/docs/0.11/
# Tutorial followed https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
from flask import Flask, jsonify, abort, make_response, request, url_for
import netifaces, logging
from sklearn.externals import joblib

# Logging initialization
logger = logging.getLogger('SentimentAnalysisHUN')
filehandler = logging.FileHandler('/var/tmp/SentimentAnalysisHUN.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
logger.addHandler(streamhandler)
logger.setLevel(logging.WARNING)

# Usage of logger with 
# logger.error('Sentiment corpus may not exist or at wrong place. Please doublecheck it!')

# Load ML model file
ML_model = joblib.load(open('SentAnalysisModel.pkl'))
print ML_model.predict(["szar vacak teszt"])


# Flask REST API
app = Flask(__name__)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'sentence' in request.json:
        abort(400)

    task = {
        'sentence': request.json['sentence'],
        'entity': 'Sando Chan',
	# use this form as input for SentimentAnalysis tool
	'description': request.json.get('description', ""),
        'sentiment': 'positive',
        'score': 0.75
    }
  
    return jsonify({'task': task}), 201





if __name__ == '__main__':
	# http://stackoverflow.com/questions/11735821/python-get-localhost-ip
	interfaces = netifaces.interfaces()
	for i in interfaces:
	    if i == 'lo':
		continue
	    iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
	    if iface != None:
		for j in iface:
		    ip_addr = j['addr']

    	app.run(host=ip_addr, port=5000)
