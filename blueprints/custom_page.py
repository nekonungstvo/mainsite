from flask import Blueprint, abort, render_template
from pony.orm import db_session

from database import CustomPages

custom_pages_blueprint = Blueprint('custom_pages', __name__, template_folder='templates')


@custom_pages_blueprint.route('/<identifier>')
@db_session
def custom_page(identifier):
    cpage = CustomPages.select(
        lambda page: page.identifier == identifier
    ).first()

    if not cpage:
        return abort(404)

    return render_template(
        'custom.jinja2',
        custom_page=cpage
    )
