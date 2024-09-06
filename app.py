import os
import re

from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, render_template, redirect, send_from_directory, request, make_response

import config

app = Flask(__name__)

PROJECTS_PATH = config.PROJECTS_PATH

@app.route("/")
@app.route("/<string:project>")
def home(project=None):
    project = project.lower() if project else ""
    projects_lst = [p.lower() for p in os.listdir(PROJECTS_PATH)] or []
    project_selected = project if project in projects_lst else projects_lst[0]

    images_lst = os.listdir(f"{ PROJECTS_PATH }/{ project_selected }") or []

    rgx = '\$(.*?)\$' # regex searched
    images_lst_dct = [{ "name": f"{i}", "mobile_align": f"{re.search(rgx, i).group(1)}%" if re.search(rgx, i) else None } for i in images_lst]

    return render_template(
        "index.html",
        projects=projects_lst,
        project_selected=project_selected,
        images_availables=images_lst_dct,
        instagram_url=config.INSTAGRAM_URL,
        linkedin_url=config.LINKEDIN_URL
    )


@app.route('/images/<path:project>/<path:image>')
def serve_project_image(project, image):
    return send_from_directory(f'{PROJECTS_PATH}/{project}', image), 200


@app.route('/sitemap.xml')
def sitemap():
    host = urlparse(request.base_url).hostname
    protocol = urlparse(request.base_url).scheme
    projects_lst = [p.lower() for p in os.listdir(PROJECTS_PATH)] or []
    xml_template =  render_template("sitemap.xml",
                           dns=config.DNS,
                           projects=projects_lst,
                           lastmod=f"{datetime.today().strftime('%Y')}-01-01"
            )

    response = make_response(xml_template)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'

    return response

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/'), 302

if __name__ == "__main__":
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')