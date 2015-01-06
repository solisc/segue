import flask

import core
import api
import helpers
import errors

class NullApplication(flask.Flask):
    def __init__(self):
        super(NullApplication, self).__init__(__name__)

class Application(flask.Flask):
    def __init__(self, settings_override=None):
        super(Application, self).__init__(__name__)
        self._set_json_encoder()
        self._set_debug()
        self._load_configs(settings_override)
        self._register_blueprints()
        self._register_error_handlers()
        self._init_deps()

    def _register_error_handlers(self):
        def handler(e):
            return flask.jsonify(dict(errors=e.args)), getattr(e, 'code', 400)
        self.errorhandler(errors.SegueError)(handler)

    def _load_configs(self, settings_override):
        self.config.from_object('segue.settings')
        self.config.from_object(settings_override)

    def _set_debug(self):
        self.debug = True

    def _register_blueprints(self):
        for blueprint in api.blueprints:
            self.register_blueprint(blueprint)

    def _init_deps(self):
        core.db.init_app(self)

    def _set_json_encoder(self):
        self.json_encoder = helpers.JSONEncoder
