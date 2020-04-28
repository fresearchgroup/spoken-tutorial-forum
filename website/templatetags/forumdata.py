from django import template
from website.sortable import get_sortable_header
register = template.Library()


@register.filter
def sort_by(queryset, order):
    return queryset.filter(visible__exact=1).order_by('position')


''' includes: will include include's values '''


def reset_get_values(getValue, includes=['page']):
    values = ''
    for k, v in list(getValue.items()):
        if k in includes:
            values += k+'='+v+'&'
    return values


''' includes: will include include's values '''


def reset_get_value(getValue, exclude_key=None):
    values = ''
    for k, v in list(getValue.items()):
        if k != exclude_key:
            if values:
                values += '&'
            values += k + '=' + v
    return values


''' excludes: will exclude excludes's values '''
def combine_get_values(getValue, excludes = ['page']):
    values = ''
    for k,v in list(getValue.items()):
        if k not in excludes:
            values += k+'='+v+'&'
    return values

def paginator_page_cutter(page_range, current_page):
    page_count = len(page_range)
    if page_count <= 11:
        return page_range
    start_page = current_page - 5
    end_page = current_page + 5
    if current_page <= 11:
        if current_page < 6:
            start_page = 1
            end_page = 11
        else:
            tmp = current_page - 5
            start_page = tmp
            end_page = current_page + 5
    if page_count < end_page:
        end_page = page_count
        tmp = end_page - current_page
        start_page =  start_page - (5 - tmp)
    return list(range(start_page, end_page+1))

register.filter('reset_get_values', reset_get_values)
register.filter('reset_get_value', reset_get_value)
register.inclusion_tag('website/templates/sortable_header.html')(get_sortable_header)
register.filter('combine_get_values', combine_get_values)
register.filter('paginator_page_cutter', paginator_page_cutter)
