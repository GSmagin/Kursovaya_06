from django.template.defaulttags import register
from config.settings import BASE_DIR


@register.inclusion_tag(BASE_DIR / 'main/templates/main/pagination.html', name='pag_nav')
def button_navigation(paginator, page_obj):
    return {'paginator': paginator, 'page_obj': page_obj}


@register.filter
def get_name_or_email(user, default='Неизвестно'):
    if user:
        # return user.username or user.email or default
        return user.email or default
    return default


@register.filter()
def media_files(path):
    if path:
        return f"/media/{path}"
    return "/media/no_foto.jpg"


@register.filter
def truncate_chars(value, max_length):
    if len(value) > max_length:
        return value[:max_length] + '...'
    return value
