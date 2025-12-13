import sys

match sys.argv.pop(1):
    case "tool":
        from phystool import phystool

        phystool()
    case "noob":
        from phystool import physnoob

        physnoob()
    case _:
        exit(1)
