from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Логин:', [
        validators.Length(
            min=2, max=16,
            message="Логин должен иметь от 2 до 16 символов."
        ),
        validators.Regexp(
            regex="[A-Za-z0-9_\-]",
            message="Для пароля допускаются только англ. буквы, цифры, дефис, _."
        ),
        validators.DataRequired(
            message="Поле \"Логин\" быть заполнено."
        )
    ])

    password = PasswordField('Пароль:', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Пароли должны совпадать.')
    ])

    password_confirm = PasswordField('Пароль (ещё раз):', [
        validators.DataRequired('Нет ответа на вопрос капчи.')
    ])

    captcha_answer = StringField()


class LoginForm(Form):
    username = StringField('Логин')
    password = StringField('Пароль')
