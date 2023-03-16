from progress.bar import IncrementalBar

import config
from utils import disk
from utils import one_s
from utils import yadisk


def main():
    one_s_clusters = one_s.get_clusters()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            bases_in_cluster = one_s.get_bases_in_cluster(cluster,
                                                          config.CLUSTER_USER,
                                                          config.CLUSTER_PASSWORD)

            print('Начинаем выгрузку баз: ')
            bar = IncrementalBar('Выгрузка баз: ', max=len(bases_in_cluster))

            for infobase in bases_in_cluster:

                if infobase.Name not in config.EXCLUDE_BASE:
                    sessions = one_s.get_infobase_sessions(cluster,
                                                           config.CLUSTER_USER,
                                                           config.CLUSTER_PASSWORD,
                                                           infobase)

                    for session in sessions:
                        one_s.terminate_session(cluster, config.CLUSTER_USER,
                                                config.CLUSTER_PASSWORD,
                                                session)

                    if infobase.Name in config.INFOBASES_USER.keys():

                        infobase_user = \
                            list(config.INFOBASES_USER.get(
                                infobase.Name).keys())[
                                0]
                        infobase_password = list(config.INFOBASES_USER.get(
                            infobase.Name).values())[0]
                    else:
                        infobase_user = config.DEFAULT_INFOBASE_USERNAME
                        infobase_password = config.DEFAULT_INFOBASE_PASSWORD

                    one_s.backup_server_base(config.ONE_S_SERVER,
                                             infobase.Name,
                                             infobase_user,
                                             infobase_password,
                                             config.BACKUP_FOLDER)
                    bar.next()
            bar.finish()
            print('Выгрузка баз окончена!')

    if config.YADISK_UPLOAD:
        print('Начинаем выгрузку на Яндекс.Диск: ')
        yadisk.recursive_upload(config.BACKUP_FOLDER, config.YADISK_FOLDER)
        if not config.SAVE_BACKUP_AFTER_YADISK_UPLOAD:
            disk.clear_folder(config.BACKUP_FOLDER)
        print('Выгрузка на Яндекс.Диск закончена!')

    one_s.kill_processes()


if __name__ == '__main__':
    main()
