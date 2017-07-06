from wtforms import StringField, validators


class LoginField(StringField):
    """
    Custom field for login as it's used for character and registration
    """

    def __init__(self, *args, **kwargs):
        kwargs = {
            **kwargs,
            "validators":
                [
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
                ] + kwargs.get("validators", []),
            "render_kw": dict(
                size=10,
                maxlength=20,
                placeholder="Англ. буквы, цифры, дефис, _ до 16 символов",
                pattern="[A-Za-z0-9_\-]{2,16}",
                required=True,
                **kwargs.get("render_kw", {})
            ),
        }

        super().__init__(
            *args,
            **kwargs,
        )
