from mysql import db_operate
import settings
class select_ip:
    def selectip(self,platformAlias,serverId):
        sql = 'select serverIp from mds_server where platformAlias="%s" and serverId="%s"' %(platformAlias,serverId)
        db = db_operate()
        serverIp1 = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        for serverIp in serverIp1:
            return serverIp

