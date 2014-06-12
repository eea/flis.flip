
from django_assets import Bundle, register


CSS_ASSETS = (
    'css/bootstrap.min.css',
    'css/style.css',
    'css/bootstrap-datetimepicker.css',
    'css/jquery.dataTables.css',
)


HOMEPAGE_CSS_ASSETS = (
    'css/home.css',
)


JS_ASSETS = (
    'js/lib/jquery.min.js',
    'js/lib/bootstrap.min.js',
    'js/lib/moment.js',
    'js/lib/bootstrap-datetimepicker.min.js',
    'js/lib/jquery.dataTables.min.js',
    'js/main.js',
)


css = Bundle(*CSS_ASSETS, filters='cssmin', output='packed.css')
home_css = Bundle(*HOMEPAGE_CSS_ASSETS, filters='cssmin',
                  output='homepacked.css')
js = Bundle(*JS_ASSETS, filters='jsmin', output='packed.js')
register('css', css)
register('home_css', home_css)
register('js', js)
