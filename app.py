import os

from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/<string:project>")
def home(project=None):
    project = project.lower() if project else ""
    projects_availables = [p.lower() for p in os.listdir("static/img/projects")] or []
    project_selected = project if project in projects_availables else projects_availables[0]
    images_availables = os.listdir(f"static/img/projects/{ project_selected }") or []

    return render_template("index.html",
                           projects=projects_availables,
                           project_selected=project_selected,
                           images_availables=images_availables)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 302