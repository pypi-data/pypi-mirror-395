import git
import click
import pathlib



class Repository:

	@classmethod
	def Initialize(self):
		self.storage = []

	@classmethod
	def Store(self, repository):
		self.storage.append(repository)

	@classmethod
	def Process(self, method='process'):
		fn = getattr(Repository, method)
		for repository in self.storage:
			fn(repository)

	@classmethod
	def Clone(self, url, path):
		git.Repo.clone_from(url, path)
		return self(path)

	def __init__(self, path=None):
		self.path = path or pathlib.Path.cwd()
		self.instance = git.Repo(self.path)
		self.tags = set()

	def tag(self, name):
		self.tags.add(name)

	def url(self):
		remote = self.instance.remote(name="origin")
		return list(remote.urls)[0]

	def Print(self):
		message = click.style(self.path)
		click.echo(message)

	def push(self):
		origin = self.instance.remote(name="origin")
		origin.push(f'{self.branch.name}:{self.branch.name}')

	def pull(self):
		origin = self.instance.remotes.origin
		return origin.pull()

	def process(self):
		self.process_branch()
		self.process_remote()
		self.process_working_directory()

	def process_branch(self):
		branch = self.instance.active_branch
		if branch.name in ('production', 'development'):
			self.tag(f'branch:{branch.name}')
		else:
			self.tag('branch:other')

		self.branch = branch

	def process_remote(self):
		try:
			branch_remote = self.instance.remotes.origin.refs[self.branch.name]
		except:
			self.tag('remote:none')
			return

		if self.branch.commit == branch_remote.commit:
			self.tag('commit:remote')
		else:
			self.tag('commit:ahead')
			self.commits_pending = list(self.instance.iter_commits(f'{branch_remote.name}...{self.branch.name}'))
			self.commits_pending_count = len(self.commits_pending)

	def process_working_directory(self):
		if self.instance.is_dirty(untracked_files=True):
			self.tag('wd:dirty')
		else:
			self.tag('wd:clean')

	def __hash__(self):
		return hash(self.path)

	def __eq__(self, other):
		return self.path == other.path



def Repositories(*tags):
	tags = set(tags)
	return [_ for _ in Repository.storage if tags <= _.tags]
