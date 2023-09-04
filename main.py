import tempfile
import shutil

from progress.bar import IncrementalBar

import config
from utils import disk, one_s, system, ya_disk


def main():
    current_scheduled_jobs_denied = False
    current_sessions_denied = False
    one_s_clusters = one_s.get_clusters()
    temp_dir = tempfile.mkdtemp()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            process_list = one_s.get_working_processes(cluster,
                                                       config.CLUSTER_USER,
                                                       config.CLUSTER_PASSWORD)
            for process in process_list:
                conn_string = process.HostName + ":" + str(process.MainPort)
                connect = one_s.engine.ConnectWorkingProcess(conn_string)
                connect.AddAuthentication(config.CLUSTER_USER, config.CLUSTER_PASSWORD)
                bases_in_process = connect.GetInfoBases()
                print('Начинаем выгрузку баз: ')
                bar = IncrementalBar('Выгрузка баз: ',
                                     max=len(bases_in_process))

                for infobase in bases_in_process:
                    if infobase.Name not in config.EXCLUDE_BASE:
                        current_scheduled_jobs_denied = infobase.ScheduledJobsDenied
                        current_sessions_denied = infobase.SessionsDenied
                        infobase.ScheduledJobsDenied = True
                        infobase.SessionsDenied = True
                        infobase.PermissionCode = config.PERMISSION_CODE
                        connect.UpdateInfoBase(infobase)

                        if infobase.Name in config.INFOBASES_USER.keys():

                            infobase_user = list(config.INFOBASES_USER.get(infobase.Name).keys())[0]
                            infobase_password = list(config.INFOBASES_USER.get(infobase.Name).values())[0]
                        else:
                            infobase_user = config.DEFAULT_INFOBASE_USERNAME
                            infobase_password = config.DEFAULT_INFOBASE_PASSWORD

                        one_s.backup_server_base(config.ONE_S_SERVER,
                                                infobase.Name,
                                                infobase_user,
                                                infobase_password,
                                                temp_dir)
                        infobase.ScheduledJobsDenied = current_scheduled_jobs_denied
                        infobase.SessionsDenied = current_sessions_denied
                        infobase.PermissionCode = ''
                        connect.UpdateInfoBase(infobase)
                    bar.next()
                bar.finish()

            print('Выгрузка баз окончена!')

    if config.YADISK_UPLOAD:
        print('Начинаем выгрузку на Яндекс.Диск: ')
        ya_disk.recursive_upload(temp_dir, config.YADISK_FOLDER)
        print('Выгрузка на Яндекс.Диск закончена!')
    if config.SAVE_BACKUP_ON_LOCAL_DISK:
        print('Копируем выгрузки в локальный бэкап')
        shutil.copytree(temp_dir, config.BACKUP_FOLDER, dirs_exist_ok=True)
        print('Копирование в локальный бэкап закончено!')
    shutil.rmtree(temp_dir)

    one_s.kill_processes()

    if config.HOW_LONG_KEEP_BACKUP:
        if config.YADISK_UPLOAD:
            folder_for_delete = ya_disk.get_list_folder_for_clean(
                config.YADISK_FOLDER)
            for folder in folder_for_delete:
                ya_disk.delete_folder(folder)
        if config.SAVE_BACKUP_ON_LOCAL_DISK:
            folders_for_delete = disk.get_list_folder_for_clean(
                config.BACKUP_FOLDER)
            for folder in folders_for_delete:
                shutil.rmtree(folder)

    if config.SHUTDOWN_AFTER_BACKUP:
        system.shutdown_windows()


if __name__ == '__main__':
    main()
