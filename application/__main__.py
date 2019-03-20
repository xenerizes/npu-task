import sys
from .app import Application


def main(args):
    app = Application(args)
    return app.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
