from model.database import CustomPage, User
from model.authorization import has_permission


class CustomPageNotFound(Exception):
    status_code = 404

    def __init__(self, identifier):
        super().__init__()
        self.identifier = identifier


def get_custom_page_generator(identifier: str):
    return lambda cpage: cpage.identifier == identifier


def get_custom_page(identifier: str) -> CustomPage:
    cpage = CustomPage.select(
        get_custom_page_generator(identifier)
    ).first()

    if not cpage:
        raise CustomPageNotFound(identifier)

    return cpage


def create_custom_page(identifier: str):
    return CustomPage(identifier=identifier)


def delete_custom_page(identifier: str):
    get_custom_page(identifier).delete()


def can_edit_custom_page(user: User):
    return has_permission(user, "edit_custom_pages")
