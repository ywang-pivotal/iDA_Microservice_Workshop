def build_app(funcMD, service, port_number, web_debug, output_name_postfix):
    import os
    from flask import Flask, request, redirect, url_for, send_from_directory, render_template
    from werkzeug import secure_filename
    from flaskext.uploads import UploadSet
    import csv
    import json

    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = set(funcMD['supported_file_type'])
    files = UploadSet(extensions = tuple(ALLOWED_EXTENSIONS))
     
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ARGV_LIST = None

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
                if funcMD['input_type'] == 'upload_first':
                    return redirect(url_for('argv_input', filename = filename))
                elif funcMD['input_type'] == 'auto':
                    argv_list = get_argv()
                    return redirect(url_for('uploaded_file',
                                        filename = filename, argv_list = argv_list))
            else:
                return "Unsupported file extension or no file selected"
        if funcMD['input_type'] == 'upload_first':
            return render_template("upload_file.html", allowed = ALLOWED_EXTENSIONS, 
                type = 'upload', data = funcMD)
        elif funcMD['input_type'] == 'auto':
            return render_template("upload_file.html", allowed = ALLOWED_EXTENSIONS,
                type = 'auto', data = funcMD)

    @app.route('/argv_input/<filename>', methods=['GET', 'POST'])
    def argv_input(filename):
        if request.method == 'POST':
            argv_list = get_argv()
            return redirect(url_for('uploaded_file', filename = filename, argv_list = argv_list))
        columns = []
        with open(UPLOAD_FOLDER + filename) as f:
            reader = csv.reader(f)
            columns = list(reader.next())        
        return render_template("upload_file.html", columns = columns, type = 'process', data = funcMD)

    @app.route('/uploads/<filename>')    
    @app.route('/uploads/<filename>/<argv_list>')
    def uploaded_file(filename, argv_list=None):
        inputFile = UPLOAD_FOLDER + filename
        input_argv = []
        for argv in json.loads(argv_list):
            if argv[1] == 'string':
                input_argv.append(str(argv[0]))
            elif argv[1] == 'integer':
                input_argv.append(int(argv[0]))
        inputFile = service.main(inputFile, input_argv)
        return download(filename)

    @app.route('/savename/<original_filename>')
    def resolve(original_filename):
        name = files.resolve_conflict(UPLOAD_FOLDER, secure_filename(original_filename))
        return name

    def get_argv():
        argv_list = []
        for param in funcMD['parameter']:
            argv_list.append((request.form[param['name']], param['type']))
        argv_list = json.dumps(argv_list)
        global ARGV_LIST
        ARGV_LIST = argv_list
        return argv_list

    @app.route('/download/<filename>')
    def download(filename):
        filename = filename.split('.')[0]+output_name_postfix
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename, as_attachment = True, attachment_filename = filename)

    app.run(port=port_number, host='0.0.0.0',debug = web_debug)