from . git import Git



class Application:

	@classmethod
	def Run(self, args):
		Git.Initialize()
		application = self(args.command, args)
		application.run()

	def __init__(self, command, args):
		self.command = command
		self.args = args

	def run(self):
		function = {
			'list': Git.List,
			'audit': Git.Audit,
			'push': Git.Push,
			'scan': Git.Scan,
			'url': lambda: Git.URL(self.args),
		}

		fn = function[self.command]
		fn()
