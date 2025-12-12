import os
from pathlib import Path
from typing import Optional, Iterable
from flask import Flask, request, render_template, send_file
from hrenpack.framework.flask.mixins import MultiTemplateAndStaticMixin


class App(MultiTemplateAndStaticMixin, Flask):
    def __init__(
            self, *args,
            port: int = 8000, db,
            model_class, form_class,
            database_url: str = 'sqlite:///db.sqlite3',
            title: str = "Создание нового объекта",
            notification_text: str = "Объект создан",
            index_template: str = 'dbwebform/index.html',
            model_fields: Optional[Iterable[str]] = None,
            **kwargs):
        self._init_kwargs(kwargs)
        super().__init__(*args, **kwargs)
        self.port = port
        self.db = db
        self.ModelClass = model_class
        self.FormClass = form_class
        self.title = title
        self.index_template = index_template
        self.model_fields = model_fields
        self.notification_text = notification_text
        self.index = self.route('/', methods=['GET', 'POST'])(self.index)
        self.favicon = self.route('/favicon.ico')(self.favicon)
        self._init_db(database_url)

    def _init_db(self, database_url: str = 'sqlite:///db.sqlite3'):
        self.config['SQLALCHEMY_DATABASE_URI'] = database_url
        self.db.init_app(self)
        with self.app_context():
            self.db.create_all()

    @staticmethod
    def _init_kwargs(kwargs):
        folder = Path(__file__).parent.absolute()
        if 'template_folder' not in kwargs:
            kwargs['template_folder'] = str(folder / 'templates')
        if 'static_folder' not in kwargs:
            kwargs['static_folder'] = str(folder / 'static')

    def _get_form_model_data(self, form) -> dict:
        data = dict()
        if self.model_fields is None:
            return form.data
        for key, value in form.data.items():
            if key in self.model_fields:
                data[key] = value
        return data

    def _create_new_object(self, form):
        obj = self.ModelClass(**self._get_form_model_data(form))
        self.db.session.add(obj)
        self.db.session.commit()
        return obj

    def index(self):
        form = self.FormClass()
        if request.method == 'POST':
            if form.validate_on_submit():
                self._create_new_object(form)
        return render_template(self.index_template, form=form, title=self.title,
                               notification_text=self.notification_text)

    @staticmethod
    def favicon():
        # Используется иконка с https://icon8.ru
        # Ссылка на конкретную иконку: https://icons8.ru/icon/Wy3XKG1CjyKf/database
        return send_file(Path(__file__).parent.absolute() / 'favicon.ico', mimetype='image/x-icon')

    def run(self, *args, **kwargs):
        if 'port' in kwargs:
            super().run(*args, **kwargs)
        super().run(*args, **kwargs, port=self.port)

