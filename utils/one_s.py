# coding=cp1251
import os.path
import datetime
import subprocess
import sys
import time
import logging

import config
from log import utils_log_config
from comtypes.client import CreateObject

engine = CreateObject('V83.COMConnector')
server_agent = engine.ConnectAgent('localhost')

# app_engine = CreateObject('V83.Application')
# connection_string = "Srvr=localhost;Ref=test;Usr=�������������;Pwd=test;"
# app_agent = app_engine.Connect(connection_string)
# base_connection = engine.Connect(connection_string)

utils_logger = logging.getLogger('utils' + '_' + __name__)


def terminate_one_s_sessions(cluster_user, cluster_password):
    one_s_clusters = get_clusters()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            bases_in_cluster = get_bases_in_cluster(cluster,
                                                    cluster_user,
                                                    cluster_password)
            print(f'������� ��� � �������� 1� - {len(bases_in_cluster)} ')
            for infobase in bases_in_cluster:
                sessions = get_infobase_sessions(cluster, cluster_user,
                                                 cluster_password,
                                                 infobase)
                print(f'���������� ������ - {len(sessions)}')
                for session in sessions:
                    terminate_session(cluster, cluster_user,
                                      cluster_password, session)
    else:
        print("� �������� ���� �� ����������!")
        sys.exit(1)


def kill_processes():
    res = subprocess.run(f'{os.getcwd()}\\utils\\taskkill.bat', shell=True, stderr=subprocess.PIPE)
    if res.stderr:
        utils_logger.error(f'������ �������� �������� ���������: {res.stderr}')
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
        # print('������. ��������� �� �������!')
        utils_logger.error('������. ��������� �� �������!')
        sys.exit(1)
    backup_name = f'{infobase_name}_{datetime.datetime.now().date()}.1cbckp'
    backup_folder = f'{backup_path}\\{datetime.datetime.now().date()}'
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)
    res = subprocess.run([f'{platform_path}\\1cestart.exe', 'CONFIG', f'/S {one_s_server}\\{infobase_name}',
                          f'/N {infobase_user}', f'/P {infobase_password}', f'/DumpIB {backup_folder}\\{backup_name}',
                          '-NoTruncate', f'/UC {config.PERMISSION_CODE}'], shell=True, stderr=subprocess.PIPE,
                         timeout=600)
    # if res.stderr:
    #     utils_logger.error(f'������ ��� �������� ������: {res.stderr}')
    time.sleep(180)  # ������� ��������, �.�. ������� �������� ������ ������������ � ������� ����� ���������� �������


# clusters = server_agent.GetClusters()
# if len(clusters) != 0:
#     for cluster in clusters:
#         server_agent.Authenticate(cluster, '�������������', 'test')
#         working_process = server_agent.GetWorkingProcesses(cluster)
#         bases_in_cluster = server_agent.GetInfoBases(cluster)
#         for base in bases_in_cluster:
#             print(dir(base))
#             print(base.Name)
#             sessions = server_agent.GetInfoBaseSessions(cluster, base)
#             for session in sessions:
#                 server_agent.TerminateSession(cluster, session)

def get_clusters():
    """�������� ������ ��������� ������� 1�"""
    clusters = server_agent.GetClusters()
    # print(f'������� ��������� 1�- {len(clusters)}')
    return clusters


def get_working_processes(cluster, cluster_user,
                          cluster_password):
    """�������� ������ ������� ��������� ��������"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    processes = server_agent.GetWorkingProcesses(cluster)
    # print(f'������� ��������� - {len(processes)}')
    return processes


def get_bases_in_cluster(cluster, cluster_user,
                         cluster_password):
    """�������� ������ �������������� ��� � ��������"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    infobases = server_agent.GetInfoBases(cluster)
    # print(f'������� ��� - {len(infobases)}')
    return infobases


def get_infobase_sessions(cluster, cluster_user,
                          cluster_password, base):
    """�������� ������ ������ ��� �������������� ����"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    sessions = server_agent.GetInfoBaseSessions(cluster, base)
    # print(f'������� ������ - {len(sessions)}')
    return sessions


def terminate_session(cluster, cluster_user, cluster_password,
                      session):
    """��������� ������ �������������� ����"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    server_agent.TerminateSession(cluster, session)


if __name__ == '__main__':

    # backup_server_base('localhost', 'test', '�������������', 'test', '.')
    # server_agent.Authenticate('localhost', '�������������', 'test')
    base_list = get_bases_in_cluster(get_clusters()[0], '�������������', 'test')
    process_list = get_working_processes(get_clusters()[0], '�������������', 'test')
    for process in process_list:
        conn_string = process.HostName + ":" + str(process.MainPort)
        connect = engine.ConnectWorkingProcess(conn_string)
        connect.AddAuthentication('�������������', 'test')
        bases = connect.GetInfoBases()
        # print(dir(connect))
        # print(dir(bases))
        # print(process.License.__str__())
    for base in bases:
        # print(dir(base))
        print(base.ScheduledJobsDenied)
        print(base.SessionsDenied)
        print(base.PermissionCode)
        base.PermissionCode = config.CLUSTER_PASSWORD
        print(base.PermissionCode)
        base.ScheduledJobsDenied = True
        connect.UpdateInfoBase(base)
        # print(dir(connect))
    #
    # print(dir(server_agent))
