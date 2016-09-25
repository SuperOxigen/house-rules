
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, title: str, page_name: str, header, footer,
                   baseUrl=None, metas=None):
        self._title = title
        self._page_name = page_name
        self._footerData = footer.copy()
        self._headerData = header.copy()
        # self._globalData = globalv.copy()

        for link in self.headerData.links:
            if link.name == page_name:
                link.active = True
            else:
                link.active = False

        self._baseUrl = baseUrl

    @property
    def footerData(self) -> str:
        return self._footerData

    @property
    def headerData(self) -> str:
        return self._headerData

    @property
    def baseUrl(self) -> str:
        return self._baseUrl

    @property
    def title(self) -> str:
        return self._title

    @property
    def pageName(self) -> str:
        return self._page_name

    # def prepare(self):
    #     pass

    # def on_finish(self):
    #     pass

    def render(self, template_name, **kwargs):
        super().render("layouts/main.tt", bodyTemplate=template_name,
                       headerKwargs=self.headerData.dictify(),
                       bodyKwargs=kwargs,
                       footerKwargs=self.footerData.dictify(),
                    #    globalKwargs=self.globalData,
                       **self.layoutData())

    def layoutData(self) -> dict:
        data = dict()
        data["title"] = self.title
        data["baseUrl"] = self.baseUrl
        return data
