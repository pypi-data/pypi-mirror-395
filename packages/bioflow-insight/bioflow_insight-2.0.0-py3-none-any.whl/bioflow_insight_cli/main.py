import click

import src as bioflow_insight_src
from src.workflow import Workflow

import sys

sys.setrecursionlimit(5000)


@click.command()
@click.version_option(bioflow_insight_src.__version__)
@click.argument('main_workflow_path')
@click.option(
    '--output-dir',
    default='./results',
    help='Where the results will be written.',
)
@click.option(
    '--duplicate',
    'duplicate',
    required=False,
    default=True,
    is_flag=True,
    help=''
    'When processes and subworkflows are duplicated in the workflow by the \'include as\' option, '
    'this option will duplicate the task in the graph output.',
)
@click.option(
    '--no-render-graphs',
    'render_graphs',
    required=False,
    default=True,
    is_flag=True,
    help='Don\'t generate the graphs output in png format using graphviz (faster),'
    'the mermaid and dot formats are always generated.',
)
@click.option(
    '--engines',
    "engines",
    type=click.STRING,
    required=False,
    multiple=True,
    help='todo',
    default=['nls', 'bioflow'],
)
@click.option(
    '--name',
    'name',
    required=False,
    help='Workflow name, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--authors',
    'authors',
    required=False,
    help='Authors of workflow (format "author1, author2, ..."), extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--keywords',
    'keywords',
    required=False,
    help='Keywords of workflow (fomat "keyword1, keyword2, ..."), extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--description',
    'description',
    required=False,
    help='Description of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--date-published',
    'datePublished',
    required=False,
    help='Publication date (format "yyyy-mm-dd"), extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--license',
    'license',
    required=False,
    help='License of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--creative-work-status',
    'creativeWorkStatus',
    required=False,
    help='Creative work status of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--version',
    'version',
    required=False,
    help='Version of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--producer',
    'producer',
    required=False,
    help='Producer of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--publisher',
    'publisher',
    required=False,
    help='Publisher of workflow, extracted otherwise (in the case of a Git repo).',
)
@click.option(
    '--display-info',
    'display_info',
    required=False,
    default=True,
    is_flag=True,
    help='Option to show a visual summary of the analysis.',
)
def cli_command(main_workflow_path, **kwargs):
    return cli(main_workflow_path, **kwargs)


def cli(main_workflow_path, render_graphs: bool, **kwargs):
    """
    The path to main file, subworkflows and modules must be in direct subdir of this file,
    in folders with eponymous names.
    """

    w = Workflow(file=main_workflow_path, **kwargs)
    w.initialise()
    w.generate_specification_graph()
    w.generate_process_dependency_graph()
    w.get_metro_map_json(render_dot=True)
    if w.is_initialised_with_bioflow():
        w.get_rocrate()


if __name__ == '__main__':
    cli_command()
