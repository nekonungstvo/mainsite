from wtforms import Form, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea

from model.forms.fields import LoginField
from model.forms.validators import UserUnique, CharacterUnique, CheckCaptcha


class RegistrationForm(Form):
    """
    Form for registration
    """
    username = LoginField(
        label='Логин:',
        validators=[UserUnique('Имя пользователя уже занято')]
    )

    password = PasswordField(
        label='Пароль:',
        validators=[
            DataRequired(),
            EqualTo('password_confirm', message='Пароли должны совпадать.')
        ],
        render_kw=dict(
            size=10,
            maxlength=255,
            placeholder="Не забывайте его",
            required=True
        )
    )

    password_confirm = PasswordField(
        label='Пароль (ещё раз):',
        validators=[
            DataRequired('Нет ответа на вопрос капчи.')
        ],
        render_kw=dict(
            size=10,
            maxlength=255,
            placeholder="Пароли должны совпадать",
            required=True
        )
    )

    captcha_answer = StringField(
        validators=[CheckCaptcha()],
        render_kw=dict(
            size=10,
            maxlength=20,
            placeholder="Ответ на простой вопрос капчи",
            required=True
        )
    )

    def set_captcha(self, captcha):
        self.captcha_answer.data = ""
        self.captcha_answer.label.text = captcha

class CharacterForm(Form):
    """
    Form for character edit and creation
    """
    login = LoginField(
        label='Логин персонажа:',
        validators=[CharacterUnique("Такой логин уже занят")]
    )

    name = StringField(label='Имя персонажа:')

    appearance = StringField(
        label='Внешность персонажа:',
        widget=TextArea()
    )

    story = StringField(
        label='История и характер персонажа:',
        widget=TextArea()
    )

    ready = BooleanField(label='Проверка:')


class LoginForm(Form):
    username = StringField(
        label='Логин',
        render_kw=dict(
            maxlength=20,
            placeholder="login",
            required=True
        )
    )

    password = PasswordField(
        label='Пароль',
        render_kw=dict(
            maxlength=255,
            placeholder="password",
            required=True
        )
    )


class AboutForm(Form):
    """
    Profile edit form
    """
    about_text = StringField(
        label='Обо мне:',
        widget=TextArea()
    )


class CustomPageForm(Form):
    """
    Form for custom page edit
    """
    identifier = StringField(label="Идентификатор")
    title = StringField(label="Заголовок страницы:")
    content = StringField(
        label='Содержимое страницы (markdown):',
        widget=TextArea()
    )
