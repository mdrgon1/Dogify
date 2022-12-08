from inspect import signature
import re


def echo(p):
    print(p)


def help():
    for cmd in CLI_CMDS.keys():
        num_params = len(signature(CLI_CMDS[cmd]).parameters)
        print(cmd, ": takes", num_params, "parameters")


def quit():
    print("closing dogify cli")


# associate function names in the CLI with callables
CLI_CMDS = {
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

        cmd, param = parse_cmd(cmd)
        # verify command exists
        if cmd not in CLI_CMDS.keys():
            print("command", cmd, "not found, use 'help' for a list of functions")
            continue

        # verify correct number of parameters
        num_params = len(signature(CLI_CMDS[cmd]).parameters)
        if num_params != len(param):
            print("command", cmd, "requires", num_params, "parameters, found", len(param))
            continue

        # execute the command
        try:
            print(CLI_CMDS[cmd](*param))
        except Exception as e:
            print("an error occurred when running command", cmd)
            print(e)

    print("Closing Dogify CLI")


if __name__ == "__main__":
    run_cli()


def register_cmds(name, fun, *d):
    CLI_CMDS[name] = fun
    if d:
        register_cmds(*d)
