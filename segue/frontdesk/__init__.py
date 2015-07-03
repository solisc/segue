import flask

from controllers import *
from responses import *

class FrontdeskPersonBlueprint(flask.Blueprint):
    def __init__(self):
        super(FrontdeskPersonBlueprint, self).__init__('fd.person', __name__, url_prefix='/fd/people')
        self.controller = PersonController()
        self.add_url_rule('',                        methods=['GET'],  view_func=self.controller.list)
        self.add_url_rule('',                        methods=['POST'], view_func=self.controller.create)
        self.add_url_rule('/<int:person_id>',        methods=['GET'],  view_func=self.controller.get_one)
        self.add_url_rule('/<int:person_id>',        methods=['PUT'],  view_func=self.controller.modify)
        self.add_url_rule('/<int:person_id>/promo',  methods=['POST'], view_func=self.controller.apply_promo)
        self.add_url_rule('/<int:person_id>/pay',    methods=['POST'], view_func=self.controller.make_payment)
        self.add_url_rule('/<int:person_id>/badges', methods=['GET'],  view_func=self.controller.get_badge)
        self.add_url_rule('/<int:person_id>/badges', methods=['POST'], view_func=self.controller.create_badge)

class FrontdeskBadgeBlueprint(flask.Blueprint):
    def __init__(self):
        super(FrontdeskBadgeBlueprint, self).__init__('fd.badge', __name__, url_prefix='/fd/badges')
        self.controller = BadgeController()
        self.add_url_rule('',                      methods=['GET'],  view_func=self.controller.get_one)
        self.add_url_rule('',                      methods=['POST'], view_func=self.controller.create)
        self.add_url_rule('/<int:badge_id>/move',  methods=['POST'], view_func=self.controller.move)
        self.add_url_rule('/<int:badge_id>/print', methods=['POST'], view_func=self.controller.issue)
        self.add_url_rule('/<int:badge_id>/give',  methods=['POST'], view_func=self.controller.give)
        self.add_url_rule('/<int:badge_id>/trash', methods=['POST'], view_func=self.controller.trash)

blueprints = [
    FrontdeskBadgeBlueprint(),
    FrontdeskPersonBlueprint()
]