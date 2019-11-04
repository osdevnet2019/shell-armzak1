import os

def cd(path):
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("cd: no such file or directory: {}".format(path))
    return 1

def exit():
    return 0

def shell_launch(arguments):
    pid = os.fork()
    status = 0
    if pid == 0:
        try:
            res = os.execvp(arguments[0], arguments)
            if res == -1:
                print(os.error().strerror())
        except FileNotFoundError:
            print("%s not found in path" % arguments[0])
        
    elif pid < 0:
        print(os.error().strerror())
    else:
        while True:
            _, status = os.waitpid(pid, status)
            if os.WIFEXITED(status) or os.WIFSIGNALED(status):
                break
    return 1

def shell_launch_bg(arguments):
    pid = os.fork()
    if pid == 0:
        print(os.getpid())
        os.setpgid(0,0)
        try:
            res = os.execvp(arguments[0], arguments)
            if res == -1:
                print(os.error().strerror())
        except FileNotFoundError:
            print("%s not found in path" % arguments[0])
    elif pid < 0:
        print(os.error().strerror())
    return 1
    
def shell_execute(arguments):
    if arguments[0] == '':
        return 1
    if arguments[0] == 'cd':
        return cd(arguments[1])
    elif arguments[0] == 'exit':
        return exit()
    else:
        if arguments[-1] == '&':
            return shell_launch_bg(arguments[:-1])
        return shell_launch(arguments)

def shell_loop():
    status = 1
    is_admin = os.getuid() == 0
    prompt_sign = "# " if is_admin else "$ "
    while status > 0:
        i = input(prompt_sign)
        status = shell_execute(i.split(' '))

if __name__ == "__main__":
    shell_loop()
