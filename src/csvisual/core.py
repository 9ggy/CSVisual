from flask import render_template, request, Blueprint
from werkzeug.utils import secure_filename
import pandas as pd  
import os
from hashlib import sha256
from random import choice
from csvisual.dataframe_parsing import * # i knows it's bad practice but it makes things so much easier.
import logging


# Config
logging.basicConfig(filename='csvisual/logs.log', filemode='w', format='%(levelname)s | "%(message)s"')
core = Blueprint("core", __name__)
UPLOAD_FOLDER = 'csvisual/static/userFilesTemp'



@core.route("/")
@core.route("/home")
def home() -> str:
	return render_template("core/home.html")


@core.route('/upload', methods=["GET", "POST"])
def upload_file() -> str:
    if request.method == 'POST':

        original_file = request.files['file']

        if original_file.content_type == "text/csv":

            uploaded_filename = sha256(secure_filename(original_file.filename).replace(".csv", "".join([choice([i for i in "absdefghijklmnopqrstuvwxyz1234567890"]) for _ in range(15)])).encode('utf-8')).hexdigest() + ".csv" # hash the name of the files , i thought it was cool
            
            original_file.save(os.path.join(f"{UPLOAD_FOLDER}", uploaded_filename))
            try:
                #create the dataframe
                df = pd.read_csv(f"{UPLOAD_FOLDER}/{uploaded_filename}")
                columns_html, row_html = generate_html(df)

            except Exception as e: 
                logging.error(f"Error parsing CSV: {e}")

                return render_template(
					'core/upload.html', 
					error=render_template("core/snippets/parsing_error.html")
				)


            os.remove(f"{UPLOAD_FOLDER}/{uploaded_filename}")


            return render_template(
                "core/visualize.html", 
				filename = original_file.filename,
                columns = columns_html, 
                rows = row_html, 
                rows_amt = len(df.axes[0]), 
                columns_amt = len(df.axes[1]),
				total = (len(df.axes[0]) * len(df.axes[1]))
            )

        return render_template(
			'core/upload.html', 
			error=render_template("core/snippets/filetype_error.html")
		)

    else:

        return render_template('core/upload.html')
