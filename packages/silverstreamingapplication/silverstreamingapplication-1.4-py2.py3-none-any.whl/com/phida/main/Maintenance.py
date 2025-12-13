from com.phida.main.sparksession import spark


class Maintenance:
    def __init__(self, dbName, tblName, zOrderColumn, intervalHours, retentionHours):
        self.dbName = dbName
        self.tblName = tblName
        self.zOrderColumn = zOrderColumn
        self.intervalHours = intervalHours
        self.retentionHours = retentionHours

    def optimizeDeltaTable(self):
        spark.sql(f"""OPTIMIZE {self.dbName}.{self.tblName}
                      WHERE src_commit_time >= current_timestamp() - INTERVAL {self.intervalHours} HOURS
                      ZORDER BY ({self.zOrderColumn})
                   """
                  )

    def vacuumDeltaTable(self):
        spark.sql(f"VACUUM {self.dbName}.{self.tblName} RETAIN {self.retentionHours}")
