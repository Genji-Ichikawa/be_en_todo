from django import template

register = template.Library()


@register.filter
def in_list(value, arg):
    """テンプレート内で value が arg のリストに含まれるかを判定"""
    return value in arg.split(",")
