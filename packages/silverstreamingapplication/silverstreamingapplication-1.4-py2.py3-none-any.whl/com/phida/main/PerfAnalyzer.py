from com.phida.main.sparksession import spark
from pyspark.sql.functions import col, avg
from pyspark.sql.utils import AnalysisException


class PerfAnalyzer:
    def __init__(self, dbName, tblName):
        self.dbName = dbName
        self.tblName = tblName
        self.tblDetails = spark.sql(f"DESCRIBE DETAIL {self.dbName}.{self.tblName}").limit(1)
        self.tblFormat = self.tblDetails.select("format").collect()[0][0]
        self.location = self.tblDetails.select("location").collect()[0][0]
        self.tblSize = self.tblDetails.select("sizeInBytes").collect()[0][0]
        self.numFiles = self.tblDetails.select("numFiles").collect()[0][0]
        self.tblProperties = self.tblDetails.select("properties").collect()[0][0]
        self.avgFileSize = self.tblSize / self.numFiles
        self.tgtFileSize = self.tblProperties['delta.targetFileSize'] if self.tblProperties['delta.targetFileSize'] \
            else self.avgFileSize

    def getOperationMetrics(self):
        try:
            targetRowsRatio = spark.sql(f"describe history {self.dbName}.{self.tblName}") \
                .filter("operation == 'MERGE' AND timestamp >= current_timestamp() - INTERVAL 24 HOURS") \
                .select("version", "timestamp", "operationMetrics").limit(50) \
                .selectExpr("version"
                            , "timestamp"
                            , "operationMetrics.numTargetRowsCopied as numTargetRowsCopied"
                            , "operationMetrics.numOutputRows as numOutputRows"
                            , "operationMetrics.numTargetRowsInserted as numTargetRowsInserted"
                            , "operationMetrics.numTargetRowsUpdated as numTargetRowsUpdated"
                            , "operationMetrics.numTargetRowsDeleted as numTargetRowsDeleted"
                            , """operationMetrics.numTargetRowsInserted +  operationMetrics.numTargetRowsUpdated + 
                              operationMetrics.numTargetRowsDeleted as numTargetRowsAffected"""
                            , "operationMetrics.numTargetFilesAdded as numTargetFilesAdded"
                            , "operationMetrics.numTargetFilesRemoved as numTargetFilesRemoved"
                            , "operationMetrics.numTargetChangeFilesAdded as numTargetChangeFilesAdded"
                            , "operationMetrics.executionTimeMs/1000 as executionTimeSeconds"
                            , "operationMetrics.scanTimeMs/1000 as scanTimeSeconds"
                            , "operationMetrics.rewriteTimeMs/1000 as rewriteTimeSeconds"
                            ) \
                .agg(avg(col("numTargetRowsAffected").cast("int")).alias("avgAffectedRows"),
                     avg(col("numTargetRowsCopied").cast("int")).alias("avgCopiedRows")
                     ) \
                .selectExpr("avgAffectedRows/avgCopiedRows as targetRowsRatio") \
                .collect()[0][0]
        except AnalysisException:
            targetRowsRatio = 1

        return targetRowsRatio

    def alterTblProperties(self):
        """
        desc:
            A Function for altering the table properties (targetFileSize) of a given table

        args:
            None

        return:
            N/A - Does not return anything. Just sets the updated table property on the table

        example:
            createDeltaTable("<database name>", "vbak", "yrmnth DATE")

        tip:
            1. This function will only add the given columns to the table
        """
        targetRowsRatio = self.getOperationMetrics()

        try:
            if targetRowsRatio < 0.000001:
                newTgtFileSize = self.tgtFileSize/2
                spark.sql(f"ALTER TABLE {self.dbName}.{self.tblName} "
                          f"SET TBLPROPERTIES (delta.targetFileSize = {newTgtFileSize})")
        except AnalysisException:
            raise Exception(f"The given table {self.dbName}.{self.tblName} does not exists")

