import controllers.base

class HomeController(controllers.base.BaseHandler):
    def initialize(self, **kwargs):
        super().initialize(title="House Rules",
                           page_name="Home",
                           **kwargs)

    def get(self):
        self.render("home.tt")
