import click

from pinta.cli.jobs.crud import get_jobs, get_job_by_id, create_job
from pinta.cli.jobs.exec import exec, ssh
from pinta.cli.jobs.commit import commit
from pinta.cli.jobs.cp import cp
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
main.add_command(ssh)
main.add_command(commit)
main.add_command(cp)


if __name__ == '__main__':
    main()
