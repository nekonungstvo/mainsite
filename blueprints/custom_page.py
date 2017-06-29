from flask import Blueprint, render_template, request, url_for, redirect
from pony.orm import db_session

from model import custom_page as custom_page_model
from model.forms import CustomPageForm

custom_pages_blueprint = Blueprint(
    'custom_pages',
    __name__,
    template_folder='templates',
    url_prefix="/custom_pages"
)


@custom_pages_blueprint.route('/<identifier>')
@db_session
def custom_page(identifier):
    cpage = custom_page_model.get_custom_page(identifier)

    return render_template(
        'custom_page.jinja2',
        custom_page=cpage
    )


@custom_pages_blueprint.route('/<identifier>/edit', methods=["GET", "POST"])
@db_session
def custom_page_edit(identifier):
    cpage = custom_page_model.get_custom_page(identifier)
    form = CustomPageForm(request.form, cpage)

    if request.form:
        if ("submit" in request.form) and form.validate():
            form.populate_obj(cpage)
            return redirect(
                url_for(
                    "custom_pages.custom_page",
                    identifier=form.identifier.data
                )
            )
            pass
        elif "delete" in request.form:
            custom_page_model.delete_custom_page(identifier)

    return render_template(
        'custom_page_edit.jinja2',
        custom_page=cpage,
        form=form
    )
