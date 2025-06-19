import os
from pathlib import Path
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


def _read_template(search_paths, template_name="report.template.jinja2"):
    # First try the provided search paths
    for search_path in search_paths:
        if os.path.exists(os.path.join(search_path, template_name)):
            env = Environment(
                loader=FileSystemLoader(search_paths),
                autoescape=False,
            )
            return env.get_template(template_name)
    
    # Fallback: try to load from package resources
    try:
        import importlib.resources as pkg_resources
        template_content = pkg_resources.read_text("pytest_md.res", template_name)
        
        # Create environment with string loader
        from jinja2 import Template
        return Template(template_content)
    except (ImportError, FileNotFoundError):
        # Final fallback: try relative to current file
        current_dir = Path(__file__).parent
        res_dir = current_dir / "res"
        if res_dir.exists() and (res_dir / template_name).exists():
            env = Environment(
                loader=FileSystemLoader([str(res_dir)]),
                autoescape=False,
            )
            return env.get_template(template_name)
    
    raise FileNotFoundError(f"Template '{template_name}' not found in any of the search paths: {search_paths}")