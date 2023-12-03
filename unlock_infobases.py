import config
from utils import one_s


def main():
    one_s_clusters = one_s.get_clusters()
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
                for infobase in bases_in_process:
                    if infobase.Name not in config.EXCLUDE_BASE:
                        try:
                            infobase.ScheduledJobsDenied = False
                            infobase.SessionsDenied = False
                            infobase.PermissionCode = ''
                            infobase.DeniedMessage = ''
                            connect.UpdateInfoBase(infobase)
                        except Exception as e:
                            print(f'\nОшибка доступа к базе: {e}')


if __name__ == '__main__':
    main()
   