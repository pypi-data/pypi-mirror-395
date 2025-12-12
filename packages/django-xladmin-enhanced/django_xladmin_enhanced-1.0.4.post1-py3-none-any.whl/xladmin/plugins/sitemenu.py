
from xladmin.sites import site
from xladmin.views import BaseAdminPlugin, CommAdminView

BUILDIN_STYLES = {
    'default': 'xladmin/includes/sitemenu_default.html',
    'accordion': 'xladmin/includes/sitemenu_accordion.html',
}


class SiteMenuStylePlugin(BaseAdminPlugin):

    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.menu_style]
        return context

site.register_plugin(SiteMenuStylePlugin, CommAdminView)

