from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("app/templates"))

template = env.get_template("email.html")


def render_email(body: str, tracking_url: str):
    return template.render(
        body=body,
        tracking_url=tracking_url
    )