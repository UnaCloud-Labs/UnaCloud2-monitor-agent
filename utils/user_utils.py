import subprocess


class UserUtils:

    def get_users_logged(self):
        ERROR = 'Error: '
        command = ['cmd /C query user']
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        if proc.returncode != 0 and proc.returncode != 1:
            if stderr is not None:
                return (ERROR + str(stderr))
            else:
                return (ERROR + 'unkown')
        else:
            result = stdout.decode('utf-8', 'backslashreplace')
            arr_result = result.split(' ')
            return True if 'Activo' in arr_result else False
		
