from flask import Flask, render_template, request, make_response, jsonify, send_file
import os, glob
from PIL import Image

upload_path = './static/img'
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	file.save(os.path.join(upload_path, file.filename))
	return ""

@app.route('/getPatch', methods=['GET'])
def getPatch():
	filename = request.args.get('name')
	return send_file(os.path.join(upload_path, filename))

@app.route('/getImageNames')
def getImageNames():
	images = glob.glob(os.path.join(upload_path, '*'))
	ret = []
	for image in images:
		img = Image.open(image)
		width, height = img.size
		ret.append({'name': os.path.basename(image), 
			'width': width, 'height': height})

	return jsonify(ret)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8080)
