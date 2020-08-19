import click

from pinta.cli.jobs.crud import get_jobs, get_job_by_id, create_job, delete_job_by_id
from pinta.cli.jobs.exec import exec, ssh
from pinta.cli.jobs.commit import commit
from pinta.cli.jobs.cp import cp
from pinta.cli.jobs.logs import watch, log

from pinta.cli.volumes.crud import get_volumes, get_volume_by_id, create_volume, delete_volume_by_id

from pinta.cli.images.crud import get_images, get_image_by_id, delete_image_by_id

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


@main.group()
def delete():
    pass


get.add_command(get_jobs)
get.add_command(get_job_by_id)
get.add_command(get_volumes)
get.add_command(get_volume_by_id)
get.add_command(get_images)
get.add_command(get_image_by_id)

create.add_command(create_job)
create.add_command(create_volume)

delete.add_command(delete_job_by_id)
delete.add_command(delete_volume_by_id)
delete.add_command(delete_image_by_id)

main.add_command(login)
main.add_command(exec)
main.add_command(ssh)
main.add_command(commit)
main.add_command(cp)
main.add_command(log)
main.add_command(watch)


if __name__ == '__main__':
    main()
