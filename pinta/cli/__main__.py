import click

from pinta.cli.jobs import get_jobs, get_job_by_id, create_job, exec, commit, cp
from pinta.cli.users import login


@click.group()
def main():
    pass


@main.group()
def get():
    pass


@main.group()
def create():
    pass


get.add_command(get_jobs)
get.add_command(get_job_by_id)

create.add_command(create_job)

main.add_command(login)
main.add_command(exec)
main.add_command(commit)
main.add_command(cp)


if __name__ == '__main__':
    main()
