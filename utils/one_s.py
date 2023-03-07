from comtypes.client import CreateObject

engine = CreateObject('V83.COMConnector')
server_agent = engine.ConnectAgent('localhost')


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

def get_clusters(server_agent):
    """Получить список кластеров сервера 1С"""
    return server_agent.GetClusters()


def get_working_processes(server_agent, cluster, cluster_user,
                          cluster_password):
    """Получить список рабочих процессов кластера"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    return server_agent.GetWorkingProcesses(cluster)


def get_bases_in_cluster(server_agent, cluster, cluster_user,
                         cluster_password):
    """Получить список информационных баз в кластере"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    return server_agent.GetInfoBases(cluster)


def get_infobase_sessions(server_agent, cluster, cluster_user,
                          cluster_password, base):
    """Получить список сессий для информационной базы"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    return server_agent.GetInfoBaseSessions(cluster, base)


def terminate_session(server_agent, cluster, cluster_user, cluster_password,
                      session):
    """Отключить сессию информационной базы"""
    server_agent.Authenticate(cluster, cluster_user, cluster_password)
    server_agent.TerminateSession(cluster, session)
