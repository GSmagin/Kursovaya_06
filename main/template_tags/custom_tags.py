from django.template.defaulttags import register
from config.settings import BASE_DIR


@register.inclusion_tag('main/pagination.html', name='pag_nav')
def button_navigation(paginator, page_obj):
    return {
        'paginator': paginator,
        'page_obj': page_obj
        }
