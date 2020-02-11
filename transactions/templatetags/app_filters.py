from django import template


register = template.Library()


@register.filter(name='transaction_user')
def transaction_user(value):
    user = [v.user.username for v in value]
    return ','.join(user).title()
