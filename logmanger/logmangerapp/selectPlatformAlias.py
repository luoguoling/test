from mysql import db_operate
from logmanger import settings
class select_platformAlias:
    def selectplatformAlias(self):
        sql = 'select distinct(platformAlias) from mds_server'
        db = db_operate()
        platformAliass = db.mysql_command(settings.LOGMANGER_MYSQL,sql)
        for platformAlias in platformAliass:
            return platformAlias
