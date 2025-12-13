import yaml
import hashlib
import pathlib



class Cache:

	@classmethod
	def Initialize(self):
		self.ROOT = pathlib.Path('~/.cache/Git').expanduser().resolve()
		if self.ROOT.exists():
			return

		self.ROOT.mkdir(parents=True, exist_ok=True)

	@classmethod
	def Path(self, key):
		return self.ROOT / hashlib.sha256(str(key).encode('utf-8')).hexdigest()

	@classmethod
	def Load(self, key):
		path = self.Path(key)
		if not path.exists():
			return None

		with open(path, "r") as f:
			data = yaml.load(f, Loader=yaml.CSafeLoader)

		if type(data) is not list:
			path.unlink()
			return None

		return [pathlib.Path(_) for _ in data]

	@classmethod
	def Store(self, key, data):
		path = self.Path(key)
		data = [str(_.path.relative_to(key)) for _ in data]
		if not data:
			return

		with open(path, "w") as f:
			yaml.dump(data, f, default_flow_style=False, Dumper=yaml.CSafeDumper)
