from inspect import signature


def echo(p):
    print(p)


def help():
    for fun in FUNCTIONS.keys():
        num_params = len(signature(FUNCTIONS[fun]).parameters)
        print(fun, ": takes", num_params, "parameters")


# associate function names in the CLI with callables
FUNCTIONS = {
    "echo": echo,
    "help": help
}


def init():
    print("Starting Dogify CLI")

    cmd = ""
    while cmd != "quit":
        cmd = input()
        fun, param = cmd.split()[0], cmd.split()[1:]

        # verify function exists
        if fun not in FUNCTIONS.keys():
            print("function", fun, "not found, use 'help' for a list of functions")
            continue

        # verify correct number of parameters
        num_params = len(signature(FUNCTIONS[fun]).parameters)
        if num_params != len(param):
            print("function", fun, "requires", num_params, "parameters, found", len(param))
            continue

        # execute the function
        try:
            FUNCTIONS[fun](*param)
        except:
            print("an error occurred when running function", fun)

    print("Closing Dogify CLI")


if __name__ == "__main__":
    init()


def register_functions(name, fun, *d):
    FUNCTIONS[name] = fun
    if d:
        register_functions(*d)
