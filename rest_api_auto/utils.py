
def url_parameter_conversion(**kwargs):
    app = kwargs.get('app')
    model = kwargs.get('model')
    name = '.'.join((app, model))
    return name, kwargs.get('pk')