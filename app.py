import os
import re

from flask import Flask, render_template, redirect, send_from_directory

app = Flask(__name__)

PROJECTS_PATH = os.environ["PROJECTS_PATH"]

@app.route("/")
@app.route("/<string:project>")
def home(project=None):
    project = project.lower() if project else ""
    projects_lst = [p.lower() for p in os.listdir(PROJECTS_PATH)] or []
    project_selected = project if project in projects_lst else projects_lst[0]

    images_lst = os.listdir(f"{ PROJECTS_PATH }/{ project_selected }") or []

    rgx = '\$(.*?)\$' # regex searched
    images_lst_dct = [{ "name": f"{i}", "mobile_align": f"{re.search(rgx, i).group(1)}%" if re.search(rgx, i) else None } for i in images_lst]

    return render_template("index.html",
                           projects=projects_lst,
                           project_selected=project_selected,
                           images_availables=images_lst_dct)

@app.route('/images/<path:project>/<path:image>')
def serve_project_image(project, image):
    return send_from_directory(f'{PROJECTS_PATH}/{project}', image), 200

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 302

if __name__ == "__main__":
    app.run(debug=True)