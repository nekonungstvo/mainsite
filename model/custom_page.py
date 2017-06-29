from database import CustomPage


def get_custom_page_generator(identifier: str):
    return lambda cpage: cpage.identifier == identifier


def get_custom_page(identifier: str) -> CustomPage:
    cpage = CustomPage.select(
        get_custom_page_generator(identifier)
    ).first()

    if not cpage:
        raise Exception("USER NOT FOUND")

    return cpage


def delete_custom_page(identifier: str):
    get_custom_page(identifier).delete()
