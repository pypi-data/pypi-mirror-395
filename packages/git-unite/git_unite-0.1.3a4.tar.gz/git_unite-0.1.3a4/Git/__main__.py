import argparse
from . application import Application



def parse_args():
	parser = argparse.ArgumentParser(prog="Git", description="Invoke git on repository groups")
	subparsers = parser.add_subparsers(dest="command")

	list_parser = subparsers.add_parser("list", help="List all repositories")
	audit_parser = subparsers.add_parser("audit", help="Audit all repositories")
	push_parser = subparsers.add_parser("push", help="Push pending")
	scan_parser = subparsers.add_parser("scan", help="Scan current directory")
	url_parser = subparsers.add_parser("url", help="Find the url of the repository")
	url_parser.add_argument("--gitlab", help="Match hostname to gitlab.com", action="store_true")
	url_parser.add_argument("--registry", help="Print the container registry name", action="store_true")
	url_parser.add_argument("--namespace", help="Check if the path points to the correct namespace", default=None)

	args = parser.parse_args()
	if args.command is None:
		parser.print_help()
		return

	return args

def main():
	args = parse_args()
	if args is None:
		return

	Application.Run(args)

if __name__ == '__main__':
	main()
