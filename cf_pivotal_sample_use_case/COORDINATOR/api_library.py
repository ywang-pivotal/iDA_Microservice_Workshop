def build_api(url, funcMD, rootPath, downloadPath, filename, output_name_postfix, args):
	import requests
	import urllib
	import json
	arguments = {}
	for i,param in enumerate(funcMD['parameter']):
		arguments[param['name']] = args[i]
	files = {'file': open(rootPath + filename, 'rb')}
	outName = requests.get(url+'/savename/'+ filename).content
	savename = filename.split('.')[0] + output_name_postfix
	if funcMD['input_type'] == 'upload_first':
		upload = requests.post(url, files=files)
		process = requests.post(url+'/argv_input/'+outName, data=arguments)
	elif funcMD['input_type'] == 'auto':
		upload = requests.post(url, files=files, data=arguments)
	urllib.urlretrieve(url + "/download/" + outName,
	                   downloadPath + savename)
	return savename