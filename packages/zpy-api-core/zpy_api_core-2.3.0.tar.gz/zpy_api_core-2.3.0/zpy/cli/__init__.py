import os
from typing import List, Dict
from zpy.utils.files import get_files_in, file_content_updater
from zpy.cli.agregations import add_config, add_context, add_use_case, add_route_event_manager
from zpy.cli.scaffolding import scaffolding_dispatcher

import click


@click.group()
def cli():
    """This is an example script to learn Click."""
    ...


@cli.command()
@click.option('--project', '-p', required=True, type=str, help='Project name')
@click.option('--verbose', '-v', required=False, is_flag=True, default=False, help='Show logs')
@click.option('--description', '-d', required=False, type=str, help='Project description',
              default="This is very boring haha xd...")
@click.option('--developer', '-dev', required=False, type=str, help='Author', default="Zurck'z 2022")
@click.option('--context', '-c', required=False, type=str, help='Context name', default="Users")
@click.option('--use_case', '-uc', required=False, type=str, help='Use Case Name', default="GetUser")
@click.option('--developer_url', '-dev-url', required=False, type=str, help='Author url',
              default="https://www.linkedin.com/in/zurckz/")
@click.option('--open_project', '-op', required=False, is_flag=True, default=False, help='Open project')
@click.option('--only_content', '-oc', required=False, is_flag=True, default=False,
              help='Create only structure project')
def make(project, verbose, description, developer, context, use_case, developer_url, open_project,
         only_content):
    """
    Create new project
    \f
    @param project:
    @param verbose:
    @param description:
    @param developer:
    @param context:
    @param use_case:
    @param developer_url:
    @param open_project:
    @param only_content:
    @return:
    """
    in_data: List[Dict[str, str]] = [{"value": project, "title": "Project name:"},
                                     {"value": description, "title": "Project description:"},
                                     {"value": developer, "title": "Author:"},
                                     {"value": developer_url, "title": "Url Author:"},
                                     {"value": context.lower(), "title": "Context:"},
                                     {"value": use_case, "title": "Use Case:"},
                                     {"value": context.title(), "title": "Repository"},
                                     {"value": open_project, "title": "Open Project?:"},
                                     {"value": only_content, "title": "Only Content?:"},
                                     None
                                     ]
    if verbose is True:
        click.echo(f'\N{grinning face} - Initializing for create new project...')
        for data in in_data:
            if data is not None:
                click.echo(f'\N{grinning face} - With {data["title"]} {data["value"]}')

    scaffolding_dispatcher(in_data, verbose, click)


@cli.group()
def add():
    """
    Add new context, case or event mappers
    \f
    @return:
    """
    ...


@add.command()
@click.option('--name', '-n', required=True, type=str, is_flag=False, help='Bounded Context name')
@click.option('--use_case', '-uc', required=False, type=str, help='Use Case Name', default="GetUser")
@click.option('--force', '-f', required=False, type=bool, is_flag=True, help='Force creation, skipping project',
              default=False)
def context(name: str, use_case: str, force: bool):
    """
    Add new context to project.
    \f
    @param name:
    @param use_case:
    @param force:
    @return:
    """
    add_context(name, use_case, force)


@add.command()
@click.option('--name', '-n', required=True, type=str, is_flag=False, help='Use case name')
@click.option('--context', '-c', required=True, type=str, is_flag=False,
              help='Context name where use case will be created')
# @click.option('--repository', '-r', required=False, type=str, help='Repository dependency', default="AwesomeRepository")
def case(name: str, context: str):
    """
    Add new use case for specific context
    \f
    @param name:
    @param context:
    @return:
    """
    add_use_case(name, context)


@add.command(name='event-mapper')
@click.option('--force', '-f', required=False, type=bool, is_flag=True,
              help='Force creation, if exist the file will be replaced',
              default=False)
def event_mapper_manager(force: bool):
    """
    Create basic event mapper manager configuration
    \f
    @param force:
    @param name:
    @param context:
    @return:
    """
    add_route_event_manager(force)


@add.command()
@click.option('--database', '-db', required=True, type=bool, is_flag=True, help='Database configuration')
def config(database: bool):
    """
    Add basic database configuration
    \f
    @param database:
    @return:
    """
    add_config(database)


@cli.command()
def drop():
    """
    Not available yet.
    \f
    @return:
    """
    click.echo('Dropping...')


@cli.command()
@click.option('--directory', '-d', required=False, type=str, is_flag=False, help='Directory', default='.')
@click.option('--extension', '-ex', required=True, type=str, help='File type')
@click.option('--find', '-fs', required=True, type=str, help='Find substring for replace')
@click.option('--new', '-ns', required=False, type=str, help='New substring. Use: [@EMPTY] for empty str',
              default="[@EMPTY]")
def content_replace(directory: str, extension: str, find: str, new: str = '[@EMPTY]'):
    """
    Replace specific string in files with provided extension
    \f
    @param directory:
    @param extension:
    @param find:
    @param new:
    @return:
    """
    if directory == '.':
        directory = os.getcwd()
    if new in ['[@EMPTY]']:
        new = ''
    click.echo('Starting files content replacement...')
    click.echo(f'Directory: {directory}')
    click.echo(f'File Filtered by: {extension}')
    click.echo(f'Value to replace: \'{find}\'')
    click.echo(f'New value: \'{new}\'')

    def custom_mutator(line: str) -> str:
        if line and "from" in line and "src." in line:
            return line.replace(find, new)
        return line

    for file in get_files_in(directory, extension, True):
        file_content_updater(file, find=find, replaced=new)
