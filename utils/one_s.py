import os.path
import datetime
import subprocess
import time

from comtypes.client import CreateObject

engine = CreateObject('V83.COMConnector')
server_agent = engine.ConnectAgent('localhost')


def terminate_one_s_sessions(cluster_user, cluster_password):
    one_s_clusters = get_clusters()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            bases_in_cluster = get_bases_in_cluster(cluster,
                                                    cluster_user,
                                                    cluster_password)
            print(f'Найдено баз в кластере 1С - {len(bases_in_cluster)} ')
            for infobase in bases_in_cluster:
                sessions = get_infobase_sessions(cluster, cluster_user,
                                                 cluster_password,
                                                 infobase)
                print(f'Количество сессий - {len(sessions)}')
                for session in sessions:
                    terminate_session(cluster, cluster_user,
                                      cluster_password, session)

def kill_processes():
    res = subprocess.run(f'{os.getcwd()}\\utils\\taskkill.bat', shell=True)
    return res

def get_list_basesname(cluster_user, cluster_password):
    result = []
    one_s_clusters = get_clusters()
    for cluster in one_s_clusters:
        bases_in_cluster = get_bases_in_cluster(cluster,
                                                cluster_user,
                                                cluster_password)
        for infobase in bases_in_cluster:
            result.append(infobase.Name)
    return result

def backup_server_base(one_s_server, infobase_name, infobase_user,
                                                infobase_password, backup_path):
    platform_path = ''
    if os.path.isdir('C:\\Program Files\\1cv8\\common'):
        platform_path = 'C:\\Program Files\\1cv8\\common'
    elif os.path.isdir('C:\\Program Files (x86)\\1cv8\\common'):
        platform_path = 'C:\\Program Files (x86)\\1cv8\\common'
    else:
        print('Ошибка. Платформа не найдена!')
        #TODO Сделать исключение
    backup_name = f'{infobase_name}_{datetime.datetime.now().date()}.1cbackup'
    backup_folder = f'{backup_path}\\{datetime.datetime.now().date()}'
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)
    subprocess.run([f'{os.getcwd()}\\utils\\backup_command.bat', f'{platform_path}\\1cestart.exe', f'{one_s_server}\\{infobase_name}', infobase_user, infobase_password, f'{backup_folder}\\{backup_name}' ], shell=True)
    time.sleep(180)


# clusters = server_agent.GetClusters()
# if len(clusters) != 0:
#     for cluster in clusters:
#         server_agent.Authenticate(cluster, 'Администратор', 'test')
#         working_process = server_agent.GetWorkingProcesses(cluster)
#         bases_in_cluster = server_agent.GetInfoBases(cluster)
#         for base in bases_in_cluster:
#             print(dir(base))
#             print(base.Name)
#             sessions = server_agent.GetInfoBaseSessions(cluster, base)
#             for session in sessions:
#                 server_agent.TerminateSession(cluster, session)

def get_clusters():
    """Получить список кластеров сервера 1С"""
    clusters = server_agent.GetClusters()
    print(f'Найдено кластеров 1С- {len(clusters)}')
    return clusters


def get_working_processes(cluster, cluster_user,
                          cluster_password):
    """Получить список рабочих процессов кластера"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    processes = server_agent.GetWorkingProcesses(cluster)
    print(f'Найдено процессов - {len(processes)}')
    return processes


def get_bases_in_cluster(cluster, cluster_user,
                         cluster_password):
    """Получить список информационных баз в кластере"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    infobases = server_agent.GetInfoBases(cluster)
    print(f'Найдено баз - {len(infobases)}')
    return infobases


def get_infobase_sessions(cluster, cluster_user,
                          cluster_password, base):
    """Получить список сессий для информационной базы"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    sessions = server_agent.GetInfoBaseSessions(cluster, base)
    print(f'Найдено сессий - {len(sessions)}')
    return sessions


def terminate_session(cluster, cluster_user, cluster_password,
                      session):
    """Отключить сессию информационной базы"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    server_agent.TerminateSession(cluster, session)

if __name__ == '__main__':
    import locale
    import sys

    backup_server_base('localhost', 'test', 'Администратор', 'test', '.')
    print(sys.getdefaultencoding())
    print(locale.getpreferredencoding())
    print(sys.stdout.encoding)