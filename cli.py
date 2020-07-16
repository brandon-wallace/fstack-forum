import click
from application import db, create_app


@click.group()
def cli():
    '''Click group'''

    pass


@cli.command()
def initdb():
    '''Initialize the database'''

    db.drop_all(app=create_app())
    db.create_all(app=create_app())
    click.echo('Initialized database')


@cli.command()
def dropdb():
    '''Delete database'''

    db.drop_all(app=create_app())
    click.echo('Dropped database')


cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == '__main__':
    cli()
