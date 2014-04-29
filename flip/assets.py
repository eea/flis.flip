
from django_assets import Bundle, register


CSS_ASSETS = (
    'css/style.css',
)


css = Bundle(*CSS_ASSETS, filters='cssmin', output='packed.css')
register('css', css)
