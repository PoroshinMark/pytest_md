from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def _read_template(search_paths, template_name="report.template.jinja2"):
    env = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=select_autoescape(
            enabled_extensions=("jinja2",),
        ),
    )
    return env.get_template(template_name)