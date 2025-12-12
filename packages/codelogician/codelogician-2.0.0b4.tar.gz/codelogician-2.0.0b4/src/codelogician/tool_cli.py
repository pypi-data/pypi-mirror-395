"""
CLI that only includes the eval and doc subcommands.

For dev-purposes mainly.
"""
#
#   Imandra Inc.
#
#   tool_cli.py
#

import typer

from codelogician.commands.cmd_doc import app as doc_app  # noqa: F401
from codelogician.commands.cmd_eval import app as eval_app

app = typer.Typer(name='CodeLogician', no_args_is_help=True)

# app.add_typer(doc_app, name='doc', help='Documentation, guides and ImandraX reference')
app.add_typer(eval_app, name='eval', help='Evaluate IML file via ImandraX API')


if __name__ == '__main__':
    app()
