from datetime import datetime

from flask import render_template, redirect, send_from_directory, make_response, Blueprint

from nmd_viewer import config
from nmd_viewer import utils

bp = Blueprint("main", __name__)

@bp.route("/about")
def about():
    return render_template(
        "index.html",
        project_selected="about",
        images_availables=[],
        **utils.get_template_context()
    )

@bp.route("/")
@bp.route("/<string:project>")
def home(project=None):
    default_project = utils.get_projects()[0] if utils.get_projects() else None
    project_selected = project or default_project

    return render_template(
        "index.html",
        project_selected=project_selected,
        images_availables=utils.get_images_metadata(project_selected=project_selected),
        **utils.get_template_context()
    )


@bp.route('/images/<path:project>/<path:image>')
def serve_project_image(project, image):
    return send_from_directory(f'{config.PROJECTS_PATH}/{project}', image), 200


@bp.route('/documents/<string:document>')
def serve_project_document(document):
    return send_from_directory(config.DOCUMENTS_PATH, document), 200


@bp.route('/sitemap.xml')
def sitemap():
    xml_template = render_template("sitemap.xml",
                                   dns=config.DNS,
                                   lastmod=f"{datetime.today().strftime('%Y')}-01-01",
                                   **utils.get_template_context())

    response = make_response(xml_template)
    response.headers['Content-Type'] = 'current_application/xml; charset=utf-8'

    return response


@bp.errorhandler(404)
def page_not_found(error):
    return redirect('/'), 302
