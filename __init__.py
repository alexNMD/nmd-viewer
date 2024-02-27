import os
import re

from flask import Flask, render_template, redirect

app = Flask(__name__)

projects_path = "C:/Users/user/Documents/DEVs/nmd_viewer/static/img/projects"

@app.route("/")
@app.route("/<string:project>")
def home(project=None):
    project = project.lower() if project else ""
    projects_lst = [p.lower() for p in os.listdir(projects_path)] or []
    project_selected = project if project in projects_lst else projects_lst[0]

    images_lst = os.listdir(f"{ projects_path }/{ project_selected }") or []

    rgx = '\$(.*?)\$' # regex searched
    images_lst_dct = [{ "name": i, "mobile_align": f"{re.search(rgx, i).group(1)}%" if re.search(rgx, i) else None } for i in images_lst]

    return render_template("index.html",
                           projects=projects_lst,
                           project_selected=project_selected,
                           images_availables=images_lst_dct)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 302

if __name__ == "__main__":
    app.run(debug=True)