import logging
import tempfile
import shutil

from progress.bar import IncrementalBar

import config
from utils import disk, one_s, system, ya_disk
from log import backuper_log_config


def main():
    logger = logging.getLogger('backuper')
    one_s_clusters = one_s.get_clusters()
    temp_dir = tempfile.mkdtemp()
    if len(one_s_clusters) != 0:
        for cluster in one_s_clusters:
            process_list = one_s.get_working_processes(cluster,
                                                       config.CLUSTER_USER,
                                                       config.CLUSTER_PASSWORD)
            bases_in_cluster = one_s.get_bases_in_cluster(cluster,
                                                          config.CLUSTER_USER,
                                                          config.CLUSTER_PASSWORD)
            for process in process_list:
                conn_string = process.HostName + ":" + str(process.MainPort)
                try:
                    connect = one_s.engine.ConnectWorkingProcess(conn_string)
                except Exception as e:
                    print(f'Ошибка подключения к базе {conn_string}: {e}')
                    continue
                connect.AddAuthentication(config.CLUSTER_USER, config.CLUSTER_PASSWORD)
                bases_in_process = connect.GetInfoBases()
                print(
                    f'Обнаружено {len(bases_in_process)} баз на сервере, из них в списке исключений {len(config.EXCLUDE_BASE)}.')
                print('Начинаем выгрузку баз: ')
            bar = IncrementalBar('Выгрузка баз: ',
                                    max=len(bases_in_cluster) - len(config.EXCLUDE_BASE))

            for infobase in bases_in_cluster:
                if infobase.Name not in config.EXCLUDE_BASE:
                    if config.LOG:
                        logger.info(f'Начата выгрузка базы {infobase.Name}')
                    try:
                        base_in_processes = next((base for base in bases_in_process if base.Name == infobase.Name),
                                                 None)
                        base_sessions = one_s.get_infobase_sessions(cluster,
                                                                    config.CLUSTER_USER,
                                                                    config.CLUSTER_PASSWORD,
                                                                    infobase)
                        for session in base_sessions:
                            one_s.terminate_session(cluster,
                                                    config.CLUSTER_USER,
                                                    config.CLUSTER_PASSWORD,
                                                    session)
                        current_scheduled_jobs_denied = base_in_processes.ScheduledJobsDenied
                        current_sessions_denied = base_in_processes.SessionsDenied
                        base_in_processes.ScheduledJobsDenied = True
                        base_in_processes.SessionsDenied = True
                        base_in_processes.PermissionCode = config.PERMISSION_CODE
                        base_in_processes.DeniedMessage = 'База заблокирована для выполнения резервного копирования'
                        connect.UpdateInfoBase(base_in_processes)
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
                        base_in_processes.ScheduledJobsDenied = current_scheduled_jobs_denied
                        base_in_processes.SessionsDenied = current_sessions_denied
                        base_in_processes.PermissionCode = ''
                        base_in_processes.DeniedMessage = ''
                        connect.UpdateInfoBase(base_in_processes)

                    except Exception as e:
                        print(f'\nОшибка доступа к базе: {e}')
                        if config.LOG:
                            logger.critical(f'Ошибка выгрузки базы {infobase.name}:\n{e}')
                    if config.LOG:
                        logger.info(f'Выгрузка базы {infobase.Name} закончена')
                bar.next()
            bar.finish()
        print('Выгрузка баз окончена!')


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

    if config.SAVE_BACKUP_ON_LOCAL_DISK:
        print('Копируем выгрузки в локальный бэкап')
        try:
            shutil.copytree(temp_dir, config.BACKUP_FOLDER, dirs_exist_ok=True)
            if config.LOG:
                logger.info('Выгрузка скопирована в локальный бэкап')
        except Exception as e:
            print('Не удалось скопировать базы в локальный бэкап')
            if config.LOG:
                logger.error(f'Не удалось скопировать базы в локальный архив: \n{e}')
        print('Копирование в локальный бэкап закончено!')

    if config.YADISK_UPLOAD:
        print('Начинаем выгрузку на Яндекс.Диск: ')
        try:
            ya_disk.recursive_upload(temp_dir, config.YADISK_FOLDER)
            if config.LOG:
                logger.info('Выгрузка загружена на Яндекс.Диск')
        except Exception as e:
            print('Не удалось выгрузить бэкапы на Я.Диск')
            if config.LOG:
                logger.error(f'Не удалось выгрузить бэкапы на Я.Диск: \n{e}')

        print('Выгрузка на Яндекс.Диск закончена!')

    shutil.rmtree(temp_dir)

    one_s.kill_processes()

    if config.SHUTDOWN_AFTER_BACKUP:
        system.shutdown_windows()


if __name__ == '__main__':
    main()
