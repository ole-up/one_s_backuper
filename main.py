from utils import one_s
from utils import yadisk
from utils import disk

cluster_user = 'Администратор'
cluster_password = 'test'
one_s_server = 'localhost'
backup_folder = 'c:\\backup'
yadisk_folder = 'test'
yadisk_upload = True


def main():
    one_s_clusters = one_s.get_clusters()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            bases_in_cluster = one_s.get_bases_in_cluster(cluster,
                                                          cluster_user,
                                                          cluster_password)
            print(f'Найдено баз в кластере 1С - {len(bases_in_cluster)} ')
            for infobase in bases_in_cluster:
                sessions = one_s.get_infobase_sessions(cluster, cluster_user,
                                                       cluster_password,
                                                       infobase)
                print(f'Количество сессий - {len(sessions)}')
                for session in sessions:
                    one_s.terminate_session(cluster, cluster_user,
                                            cluster_password, session)
                one_s.backup_server_base(one_s_server, infobase.Name,
                                         cluster_user, cluster_password,
                                         backup_folder)
    if yadisk_upload:
        yadisk.recursive_upload(backup_folder, yadisk_folder)
        disk.clear_folder(backup_folder)

    one_s.kill_processes()


if __name__ == '__main__':
    main()
