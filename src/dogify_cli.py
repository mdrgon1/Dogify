from inspect import signature
import re


def echo(p):
    print(p)


def help():
    for fun in FUNCTIONS.keys():
        num_params = len(signature(FUNCTIONS[fun]).parameters)
        print(fun, ": takes", num_params, "parameters")


def quit():
    print("closing dogify cli")


# associate function names in the CLI with callables
FUNCTIONS = {
    "echo": echo,
    "help": help,
}


# pretty fucked up code to isolate quoted strings with spaces as single parameters
def parse_cmd(cmd):
    expressions = re.findall("('[^']*')|(\"[^\"]*\")|([^'\" ]+)", cmd)
    for i in range(len(expressions)):
        string_single_q, string_double_q, default = expressions[i]
        string_single_q = string_single_q[1:-1]
        string_double_q = string_double_q[1:-1]
        e = list(filter(lambda s: s, [string_single_q, string_double_q, default]))[0]
        e = e.replace("\\'", "\'")
        e = e.replace('\\\"', '\"')
        expressions[i] = e
    return expressions[0], expressions[1:]


def run_cli():
    print("Starting Dogify CLI")

    cmd = ""
    while cmd != "quit":
        cmd = input()
        if not cmd:
            continue

        fun, param = parse_cmd(cmd)
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
        except Exception as e:
            print("an error occurred when running function", fun)
            print(e)

    print("Closing Dogify CLI")


if __name__ == "__main__":
    run_cli()


def register_functions(name, fun, *d):
    FUNCTIONS[name] = fun
    if d:
        register_functions(*d)
