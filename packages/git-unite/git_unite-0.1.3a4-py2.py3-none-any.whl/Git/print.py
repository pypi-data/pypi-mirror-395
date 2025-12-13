import click



def Print_Header(tag):
	header = {
		'wd:dirty': {'text': 'Working directory not clean', 'fg': 167,},
		'commit:ahead': {'text': 'Push pending', 'fg': 167,},
		'remote:none': {'text': 'No remote', 'fg': 202,},
		'branch:other': {'text': 'Branch: Other', 'fg': 70,},
		'branch:development': {'text': 'Branch: Development', 'fg': 70,},
	}

	message = click.style(**header[tag], bold=False)
	click.echo(message)


def Print_Section(text):
	click.echo(click.style(text, fg='yellow'))


def Print_Repository(instance, tag=None):
	message = click.style(f'\t{instance.path}')

	if tag == 'commit:ahead':
		message += click.style(f'+{instance.commits_pending_count}', fg='green')

	click.echo(message)


def Print_Path(instance):
	message = click.style(f'\t{instance}')
	click.echo(message)


def Print_Warning(text):
	message = click.style(text, fg='yellow')
	click.echo(message)

def Print_Info(text):
	click.echo(click.style(text, fg='green'))

def Print_Empty():
	click.echo('')

def Print_Action(action, item):
	message = click.style(action) + ' ' + click.style(item, fg='green')
	click.echo(message)
