from flask import Flask, render_template, request, make_response, jsonify, send_file
import os, glob
import PIL
from PIL import Image

PIL.Image.MAX_IMAGE_PIXELS = 100000 * 100000

upload_path = './static/img'
working_path = './static/patch'
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * (2 ** 30)

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
	level = int(request.args.get('level'))
	scale = int(request.args.get('scale'))
	row = int(request.args.get('row'))
	col = int(request.args.get('col'))

	fname, ext = os.path.splitext(filename)
	patch_name = fname + ('_l%d_s%d_r%d_c%d' % (level, scale, row, col)) + ext

	if not os.path.exists(os.path.join(working_path, patch_name)):
		img = Image.open(os.path.join(upload_path, filename))
		img_crop = img.crop((
			col * img.size[0] / (2 ** (scale - 1)), 
			row * img.size[1] / (2 ** (scale - 1)), 
			(col + 1) * img.size[0] / (2 ** (scale - 1)),
			(row + 1) * img.size[1] / (2 ** (scale - 1)),
		))
		img_resize = img_crop.resize((img_crop.size[0] // (2 ** (level - scale)), img_crop.size[1] // (2 ** (level - scale))))
		img_resize.save(os.path.join(working_path, patch_name))

	return send_file(os.path.join(working_path, patch_name))

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
