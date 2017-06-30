from flask import Blueprint, render_template, request, url_for, redirect
from pony.orm import db_session

from model import custom_page as custom_page_model
from model.custom_page import CustomPageNotFound, can_edit_custom_page
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
    try:
        cpage = custom_page_model.get_custom_page(identifier)
    except CustomPageNotFound:
        cpage = None

    form = CustomPageForm(request.form, cpage)

    if request.form:
        if ("submit" in request.form) and form.validate():
            if not cpage:
                cpage = custom_page_model.create_custom_page(identifier)

            form.populate_obj(cpage)
            return redirect(
                url_for(
                    "custom_pages.custom_page",
                    identifier=form.identifier.data
                )
            )
        elif "delete" in request.form:
            custom_page_model.delete_custom_page(identifier)
            return redirect(
                url_for(
                    "custom_pages.custom_page",
                    identifier=identifier
                )
            )

    return render_template(
        'custom_page_edit.jinja2',
        custom_page=cpage,
        form=form
    )


@custom_pages_blueprint.errorhandler(CustomPageNotFound)
def handle_no_custom_page(error: CustomPageNotFound):
    return render_template(
        'custom_page_not_found.jinja2',
        identifier=error.identifier
    )


@custom_pages_blueprint.context_processor
def inject_auth_functions():
    return dict(
        can_edit_custom_page=can_edit_custom_page
    )
