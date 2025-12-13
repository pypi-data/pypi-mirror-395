import sys
import pathlib
import logging
from urllib.parse import urlparse

from . print import *
from . cache import Cache
from . repository import Repository, Repositories



class Git:

	@classmethod
	def Initialize(self, path=None, cached=True):
		Cache.Initialize()
		Repository.Initialize()
		self.Load(path)

	@classmethod
	def Load(self, path=None, cached=True):
		root = pathlib.Path.cwd() if path is None else pathlib.Path(path)
		data = Cache.Load(root) if cached else None
		self.cached_data = data

		self.cached_now = data is None
		if self.cached_now:
			self.Load_List(root)
			Cache.Store(root, Repository.storage)
		else:
			self.Load_Cache(root)

	@classmethod
	def Load_List(self, path):

		def filter_out(entry):
			if not entry.is_dir():
				return False
			if entry.name == '.git' or '.git' in entry.parts:
				return False
			return True

		entries = [_ for _ in path.glob('**/*') if filter_out(_)]
		entries = sorted(entries, key=lambda p: (len(p.parts), p))

		found = {}

		def filter_out_subdirectories(entry):
			for i in range(len(entry.parts) + 1):
				if pathlib.Path(*entry.parts[:i]) in found:
					return True
			return False

		for entry in entries:

			if filter_out_subdirectories(entry):
				continue

			try:
				repository = Repository(entry)
			except:
				continue

			Repository.Store(repository)
			found[entry] = None

	@classmethod
	def Load_Cache(self, path):
		for entry in self.cached_data:
			try:
				repository = Repository(path / entry)
			except:
				continue

			Repository.Store(repository)

	@classmethod
	def List(self):
		repositories = Repositories()

		if not repositories:
			Print_Warning(f'No repositories found in {pathlib.Path.cwd()}')
			return

		for repository in repositories:
			repository.Print()

	@classmethod
	def Audit(self):
		Repository.Process()

		tags = ['commit:ahead', 'wd:dirty', 'remote:none', 'branch:development', 'branch:other']

		for tag in tags:
			repositories = Repositories(tag)
			if not repositories:
				continue

			Print_Header(tag)
			for repository in repositories:
				Print_Repository(repository, tag)
			Print_Empty()

	@classmethod
	def Push(self):
		Repository.Process()

		repositories = Repositories('commit:ahead')
		if not repositories:
			Print_Warning('Nothing to push')
			return

		for repository in repositories:
			Print_Action('Pushing', repository.path)
			repository.push()

	@classmethod
	def URL(self, args):
		try:
			repository = Repository()
			url = repository.url()
			url = urlparse(url)
			hostname = url.hostname
			netloc = url.netloc.split('@')[-1]
			path = url.path

		except Exception as e:
			logging.error(e)
			sys.exit(1)

		if hostname is None:
			logging.error('Hostname not found')
			sys.exit(1)

		if args.namespace is not None:
			n = f'/{args.namespace}/'
			if not path.startswith(n):
				logging.error(f'Namespace check failed. {path}')
				sys.exit(1)

		if args.gitlab:
			if hostname != 'gitlab.com':
				logging.error('Not a gitlab.com repository')
				sys.exit(1)

		if args.registry:
			netloc = f'registry.{hostname}'
			path = path.removesuffix('.git')

		print(f"{netloc}{path}")

	@classmethod
	def Scan(self):
		root = pathlib.Path.cwd()

		Repository.storage = []
		if self.cached_now:
			self.cached_data = []
		self.Load_List(root)
		r_new = Repository.storage
		r_new_paths = [_.path.relative_to(root) for _ in r_new]

		r_changes_added = [_ for _ in r_new if _.path.relative_to(root) not in self.cached_data]
		r_changes_removed = [_ for _ in self.cached_data if _ not in r_new_paths]

		if not r_changes_added and not r_changes_removed:
			Print_Info('No changes')
			return

		if r_changes_added:
			Print_Section('Added')
			for _ in r_changes_added:
				Print_Repository(_)

		if r_changes_removed:
			Print_Section('Removed')
			for _ in r_changes_removed:
				Print_Path(_)

		Cache.Store(root, Repository.storage)
