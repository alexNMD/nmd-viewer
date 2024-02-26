import os

from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/<string:project>")
def home(project=None):
    local_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
    projects_path = f"{ local_path }/static/img/projects"
    project = project.lower() if project else ""
    projects_availables = [p.lower() for p in os.listdir(projects_path)] or []
    project_selected = project if project in projects_availables else projects_availables[0]
    images_availables = os.listdir(f"{ local_path }/static/img/projects/{ project_selected }") or []

    return render_template("index.html",
                           projects=projects_availables,
                           project_selected=project_selected,
                           images_availables=images_availables)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/'), 302

if __name__ == "__main__":
    app.run(debug=True)