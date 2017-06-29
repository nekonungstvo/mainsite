from flask import Flask, render_template
from flask_login import LoginManager
from flaskext.markdown import Markdown
from pony.orm import db_session, desc

from blueprints.authorization import authorization_blueprint
from blueprints.character import character_blueprint
from blueprints.custom_page import custom_pages_blueprint
from blueprints.profile import profile_blueprint
from database import User, News
from model.forms import LoginForm

app = Flask(__name__)
app.secret_key = 'super secret string'
app.login_manager = LoginManager()
app.login_manager.init_app(app)
app.markdown = Markdown(
    app
)

app.register_blueprint(profile_blueprint)
app.register_blueprint(character_blueprint)
app.register_blueprint(custom_pages_blueprint)
app.register_blueprint(authorization_blueprint)


@app.context_processor
def inject_login_form():
    return dict(login_form=LoginForm())


@app.login_manager.user_loader
@db_session
def load_user(user_id):
    return User.select(
        lambda user: user.id == user_id
    ).first()


@app.route('/')
@db_session
def index_page():
    last_news = News.select().order_by(
        lambda news: desc(news.timestamp)
    ).first()

    return render_template(
        'index.jinja2',
        last_news=last_news
    )


if __name__ == '__main__':
    app.run()
