from jinja2 import Environment

def apply_template(prompt_template: str, **kwargs):
    env = Environment()
    template = env.from_string(prompt_template)
    return template.render(**kwargs)