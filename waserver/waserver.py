from stack import YowsupSendStack
import sys
import config

# CREDENTIALS = ("49722360368", "bO6GnxXW8iPSGYoFGhjLVQE0dFE=")
# CREDENTIALS = ("4915204295777", "IcQWRVBd7l9s7F8ZG+qBkkb1/CU=")
def main():
    stack = YowsupSendStack(config.CREDENTIALS, True)
    stack.start()
    if 'noconn' in sys.argv:
        sys.exit(0)

if __name__ == "__main__":
    main()
