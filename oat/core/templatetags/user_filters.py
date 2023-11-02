from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def addstyle(field, css):
    return field.as_widget(attrs={'style': css})


@register.filter
def addclass_fc_sm(field):
    return field.as_widget(attrs={'class': 'form-control-sm'})


@register.filter
def addstyle_disable(field, css):
    return field.as_widget(attrs={'style': css, 'disabled': True})
