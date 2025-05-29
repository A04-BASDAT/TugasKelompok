from django import template
from supabase_utils import get_adopter_by_username

register = template.Library()

@register.filter
def get_adopter(username):

    return get_adopter_by_username(username) 