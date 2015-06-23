funcMD_list = [{
    "name": "Address to Postal Code",
    "supported_file_type": ["csv"],
    "input_type": "upload_first",
    "output_type": "auto",
    "description": "For a csv file, given the name of the column \
    containing the address, this function append a new column \
    containing the corresponding postal code",
    "parameter": [{
        "name": "address_colname",
        "description": "Name of the column containing address",
        "type": "string",
        "source": "search_column",
        "range": None,
        "default": None,
        "new_column": None
    },{
        "name": "postcode_colname",
        "description": "Name of the appended postcode column",
        "type": "string",
        "source": "user_input",
        "range": None,
        "default": "Postal Code",
        "new_column": True
    }]
},{
	"name": "Postcode to LatLon",
	"supported_file_type": ["csv"],
	"input_type": "upload_first",
	"output_type": "auto",
	"description": "For a csv file, given the name of the column \
	containing the postal code, this function append two new columns \
	containing the corresponding latitude and longitude",
	"parameter": [{
		"name": "postcode_colname",
		"description": "Name of the column containg postal code",
		"type": "string",
		"source": "search_column",
		"range": None,
		"default": None,
        "new_column": None
	}]
},{
	"name": "Region Appender",
	"supported_file_type": ['csv'], 
	"input_type": "auto", 
	"output_type": "'auto",
	"description": "For a csv file, this function will search \
	for the latlon pair columns and append the corresponding Region Info", 
	"parameter": [{
		"name": "ura_type",
		"description": "Type of region to be appended",
		"type": "string", 
		"source": "from_options",
		"range": ('region','planning','subzone'),
		"default": None,
        "new_column": None
	},{
		"name": "num_run",
		"description": "Number of runs (number of latlon pairs)",
		"type": "integer",
		"source": "user_input",
		"range": None,
		"default": 1,
        "new_column": None
	}]
},]

url_data = {
	"Address to Postal Code": "http://127.0.0.1:1010",
	"Postcode to LatLon": "http://127.0.0.1:1020",
	"Region Appender": "http://127.0.0.1:1030"
}

import os
import json
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug import secure_filename
from flaskext.uploads import UploadSet
import csv
import urllib
import requests
from api_library import build_api

app = Flask(__name__)
FUNCTION_LIST = None
UPLOAD_FOLDER = 'uploads_coordinator/'
ALLOWED_EXTENSIONS = set(['csv'])
files = UploadSet(extensions = tuple(ALLOWED_EXTENSIONS))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		if f and allowed_file(f.filename):
			filename = resolve(f.filename)
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('process_file', filename = filename))
		else:
			return "Unsupported file extension"
	return render_template("coordinator_home.html", allowed = ALLOWED_EXTENSIONS, data = json.dumps(funcMD_list))

@app.route('/<filename>', methods=['GET', 'POST'])
def process_file(filename):
	if request.method == 'POST':
		str_FUNCTION_LIST = unicode_to_string(FUNCTION_LIST)
		curr_filename = filename
		for func in str_FUNCTION_LIST:
			svrc_url = url_data[func.keys()[0]]
			output_name_postfix = str(hash(func.keys()[0])) + ".csv"
			svrcMD = None
			for elem in funcMD_list:
				if elem['name'] == func.keys()[0]:
					svrcMD = elem
			rootPath = UPLOAD_FOLDER
			downloadPath = UPLOAD_FOLDER
			args = []
			for elem in func[func.keys()[0]]:
				args.append(request.form[elem])
			curr_filename = build_api(svrc_url, svrcMD, rootPath, downloadPath, 
				curr_filename, output_name_postfix, args)
		return send_from_directory(app.config['UPLOAD_FOLDER'], curr_filename, 
			as_attachment = True, attachment_filename = filename)	
	columns = []
	head_rows = []
	with open(UPLOAD_FOLDER + filename) as f:
		reader = csv.reader(f)
		columns = list(reader.next())
		head_rows.append(columns)
		for i in range(5):
			head_rows.append(list(reader.next()))
	return render_template("coordinator_process.html", columns=columns, 
		head_rows=head_rows, data = json.dumps(funcMD_list))

def resolve(original_filename):
    name = files.resolve_conflict(UPLOAD_FOLDER, secure_filename(original_filename))
    return name

@app.route('/_processes')
def array2python():
	global FUNCTION_LIST
	FUNCTION_LIST = request.args.get('track_func_list', [])
	return jsonify(result=FUNCTION_LIST)

def unicode_to_string(unicode_line):
    result = []
    first_layer = json.loads(unicode_line)
    for elem in first_layer:
        temp = {}
        curr = json.loads(elem)
        for key in curr.keys():
            str_key = str(key)
            str_argv = []
            for argv in curr[str_key]:
                str_argv.append(str(argv))
            temp[str_key] = str_argv
        result.append(temp)
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000, debug = True)
