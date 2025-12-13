from com.phida.main.sparksession import spark, logger
from com.phida.main.Operations import tableExists, addDerivedColumns, createDeltaTable, alterDeltaTable, \
    dropColumns, getDerivedColumnsList, schemaDiff, getKeyCols, buildJoinCondition, buildColumnsDict, hiveDDL, schemaDataTypeDiff
from com.phida.main.utils import pathExists, convertStrToList
from pyspark.sql.functions import row_number, col, broadcast,expr, max as spark_max
from pyspark.sql.window import Window
from delta.tables import DeltaTable
from pyspark.sql import DataFrame

class SilverMerge:
    """
    A streaming pipeline for cleansing incremental data from Bronze table and merge into Silver

    args:
        srcDatabaseName: String - Source Database (typically Bronze)
        srcTableName: String - Source Table Name
        tgtDatabaseName: String - Target Database Name (Will be created if not exists)
        tgtTableName: String - Target Table Name (Will be created if not exists)
        tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
        tgtTablePath: String - Target Table Path (so that the table is created as external)
        tgtPartitionColumns: String - Target partition columns (optional)
        derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
        triggerOnce: String - Whether continuous streaming or just once
        dropColumnStr: String - Columns to be dropped from source table df
        pruneColumn: String - Column for applying the prune filter in the merge ON condition clause \
                              (to improve performance of the merge)
        cluster_table_path: String - Path to the cluster table
        enable_delete_filter: String - Flag to enable/disable filtering of deleted records (default: 'N')
        use_auto_loader: String - Flag to enable/disable use of autoloader for reading source table (default: 'N')

    methods:
        silverCleansing
        prepareTarget
        upsertToDelta
        streamIntoDeltaTarget

    example:
        from com.phida.SilverMerge import SilverMerge
        silverMergeObj = SilverMerge(srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn, cluster_table_path, enable_delete_filter, use_auto_loader)

    """
    def __init__(self, srcDatabaseName, srcTableName, tgtDatabaseName, tgtTableName,
                 tgtCheckpoint, tgtTablePath, tgtPartitionColumns, derivedColExpr,
                 triggerOnce, dropColumnStr, pruneColumn, cluster_table_path, enable_delete_filter, use_auto_loader):
        """
        desc:
            Initialize the required class variables

        args:
            srcDatabaseName: String - Source Database (typically Bronze)
            srcTableName: String - Source Table Name
            tgtDatabaseName: String - Target Database Name (Will be created if not exists)
            tgtTableName: String - Target Table Name (Will be created if not exists)
            tgtCheckpoint: String - Target Checkpoint (For storing the status of the stream)
            tgtTablePath: String - Target Table Path (so that the table is created as external)
            tgtPartitionColumns: String - Target partition columns (optional)
            derivedColExpr: String - Derived columns to be added to Silver, separated by § (optional)
            triggerOnce: String - Whether continuous streaming or just once
            dropColumnStr: String - Columns to be dropped from source table df
            pruneColumn: String - Column to use for dynamic file pruning (future feature)
            cluster_table_path: String - Path to the cluster table
            enable_delete_filter: String - Flag to enable/disable filtering of deleted records (default: 'N')
            use_auto_loader: String - Flag to enable/disable use of autoloader for reading source table (default: 'N')
        """

        logger.info("phida_log: Initialising class variables")

        self.srcDatabaseName = srcDatabaseName
        self.srcTableName = srcTableName
        self.tgtDatabaseName = tgtDatabaseName
        self.tgtTableName = tgtTableName
        self.tgtCheckpoint = tgtCheckpoint
        self.tgtTablePath = tgtTablePath
        self.tgtPartitionColumns = tgtPartitionColumns
        self.derivedColExpr = derivedColExpr
        self.triggerOnce = triggerOnce
        self.dropColumnStr = dropColumnStr
        self.pruneColumn = pruneColumn
        self.cluster_table_path = cluster_table_path
        self.enable_delete_filter = enable_delete_filter.strip().upper() if enable_delete_filter else 'N'
        self.use_auto_loader = use_auto_loader.strip().upper() if use_auto_loader and use_auto_loader.strip().upper() == 'Y' else 'N'

        logger.info(f"phida_log: Check if source table {self.srcDatabaseName}.{self.srcTableName} exists")

        if tableExists(self.srcDatabaseName, self.srcTableName):

            logger.info(f"phida_log: source table exists")

            logger.info(f"phida_log: initialising derived class variables")

            if self.use_auto_loader == 'N':
                self.srcDF = spark.readStream.table(self.srcDatabaseName + "." + self.srcTableName)
            elif self.use_auto_loader == 'Y':
                src_table_path = spark.sql(f"DESCRIBE DETAIL {self.srcDatabaseName}.{self.srcTableName}").collect()[0]['location']
                self.srcDF = spark.readStream.format("cloudFiles").option("cloudFiles.format", "parquet").option("cloudFiles.schemaLocation", src_table_path + "/_cloudfiles/_schemas").load(src_table_path)

            self.keyCols = getKeyCols(self.srcDatabaseName, self.srcTableName)

            self.keyColsList = convertStrToList(self.keyCols, ",")

            self.joinCondition = buildJoinCondition(self.keyColsList)

            self.condition = f"{self.pruneColumn} <> '' AND {self.joinCondition}" if self.pruneColumn.strip() \
                             else self.joinCondition

            self.dropColumnList = convertStrToList(self.dropColumnStr, ",")

            self.columnsDict = buildColumnsDict(self.srcDF, self.dropColumnList)

    def silverCleansing(self):
        """
        desc:
            A Method for reading from source table (Bronze) as a stream and apply cleansing transformations

        args:
            None

        return:
            silverCleansedDF: DataFrame - returns the bronze dataframe after cleansing

        example:
            silverCleansing()

        tip:
            N/A
        """
        logger.info(f"phida_log: applying cleansing rules on source dataframe ")

        if tableExists(self.srcDatabaseName, self.srcTableName):

            silverRawDF = self.srcDF

            if self.derivedColExpr:
                derivedColExprList = convertStrToList(self.derivedColExpr, "§")

                silverDerivedColumns = addDerivedColumns(silverRawDF, derivedColExprList)

            else:
                silverDerivedColumns = silverRawDF

            self.columnsDict = buildColumnsDict(silverDerivedColumns, self.dropColumnList)

            return silverDerivedColumns

    def prepareTarget(self, inDF):
        """
        desc:
            A Method for preparing the target delta table.
            Creates the delta table if it does not exists
            Raise error if there are missing column(s) 
            Raise error if data types are different between existing table and source table
            Alters the delta table if there is new column added in the source schema

        args:
            inDF: DataFrame - input spark dataframe (typically the output of silverCleansing())

        return:
            None - Does not return anything - Just creates or alters the target delta table

        example:
            prepareTarget(silverCleansedDF)

        tip:
            N/A
        """
        logger.info(f"phida_log: preparing the target delta table ")

        targetTableExists = tableExists(self.tgtDatabaseName, self.tgtTableName)

        targetPathExists = pathExists(self.tgtTablePath)

        inDF = dropColumns(inDF, self.dropColumnList)

        first_run = False if (targetTableExists & targetPathExists) else True

        if first_run:

            logger.info(f"phida_log: This seems to be the first run")
            logger.info(f"phida_log: creating the target table {self.tgtDatabaseName}.{self.tgtTableName}")

            createDeltaTable(inDF,
                             self.tgtTablePath,
                             self.tgtDatabaseName,
                             self.tgtTableName,
                             self.tgtPartitionColumns)

        else:

            existingDF =spark.read.table(self.tgtDatabaseName + "." + self.tgtTableName)

            diff2DF = schemaDiff(existingDF,inDF)

            if diff2DF.columns:
                raise Exception(f"Column(s) {diff2DF.columns} is(are) missing")

            mismatched_columns = schemaDataTypeDiff(existingDF, inDF)

            if mismatched_columns:
                raise Exception(f"There is data type mismatch in column(s): {mismatched_columns}")

            diffDF = schemaDiff(inDF, existingDF)

            addColumns = hiveDDL(diffDF)

            if addColumns:
                logger.info(f"phida_log: There seems to be a schema change in silver")
                logger.info(f"phida_log: Altering the target table {self.tgtDatabaseName}.{self.tgtTableName}")

                alterDeltaTable(self.tgtDatabaseName, self.tgtTableName, addColumns)

                logger.info(f"phida_log: newly added columns {addColumns}")

            else:
                logger.info(f"phida_log: There is no change in schema in silver")

    def filter_deleted_records(self, microBatchOutputDF):
           """
            Filters out records from microBatchOutputDF that have been marked as deleted in the Bronze table
            within the last 4 hours based on hvr_integ_key.
           """
           
           if microBatchOutputDF.isEmpty():
               return microBatchOutputDF

           filtered_table_name = f"{self.srcDatabaseName}.{self.srcTableName}_filtered"
           
           if not tableExists(self.srcDatabaseName, f"{self.srcTableName}_filtered"):
               return microBatchOutputDF
        
           delete_records = spark.read.table(filtered_table_name).filter(col("source_operation") == 0)

           if delete_records.isEmpty():
               return microBatchOutputDF

           delete_keys_df = (delete_records.groupBy(self.keyColsList).agg(spark_max(col("hvr_integ_key")).alias("delete_hvr_integ_key")))

           joined_df = microBatchOutputDF.join(broadcast(delete_keys_df), on=self.keyColsList, how="left")

           filtered_df = (joined_df.filter(
                              (col("delete_hvr_integ_key").isNull()) |
                              (col("hvr_integ_key") > col("delete_hvr_integ_key"))
                          )
                          .drop("delete_hvr_integ_key"))

           return filtered_df 
                
    def preprocess_dataframe(self, df: DataFrame, parent_keys: list) -> DataFrame:
        
            """Removes rows where all or any 'source_operation' values for a group are 8."""

            grouped_df = df.groupBy(parent_keys).agg(
                expr("bool_and(source_operation = 8)").alias("all_8"),
                expr("bool_or(source_operation = 8)").alias("any_8")
            )

            return df.join(grouped_df, on=parent_keys, how="left").filter("NOT (all_8 OR any_8)")
        
    
    def get_parent_keys(self, df: DataFrame, kernel_value: str, unpack_table_value: str) -> list:
        
        """Get the parent keys for the given kernel and unpack_table values"""
        
        filtered_df = df.filter(
            (col("kernel") == kernel_value) & (col("unpack_table") == unpack_table_value)
        )
        row = filtered_df.select("key_columns_for_pack_table", "key_columns_for_unpack_table").first()
        pack_keys = set(row["key_columns_for_pack_table"].split(',')) if row["key_columns_for_pack_table"] else set()
        unpack_keys = set(row["key_columns_for_unpack_table"].split(',')) if row["key_columns_for_unpack_table"] else set()
        parent_keys = list(pack_keys & unpack_keys)
        return parent_keys
    
        

    def upsertToDelta(self, microBatchOutputDF, batchId):
        """
        desc:
            A Function for merging the records from a given dataframe into delta Target table (foreachBatch)

        args:
            microBatchOutputDF: DataFrame -
            batchId: BigInt - required by the foreachBatch stream processor

        return:
            None - Does not return anything - This function is used by foreachbatch in streamIntoDeltaTarget

        example:
            N/A - see method streamIntoDeltaTarget() for usage

        tip:
            N/A
        """
        op_8_df = microBatchOutputDF.filter("source_operation = 8")
        microBatchOutputDF = microBatchOutputDF.filter("source_operation in (0,1,2,3)")
        microBatchOutputDF_8 = microBatchOutputDF.filter("source_operation in (0,1,2,3,8)")
        tgtDeltaTable = DeltaTable.forName(spark, self.tgtDatabaseName + "." + self.tgtTableName)
        
        if self.cluster_table_path:
            if not op_8_df.isEmpty():
                table_details = DeltaTable.forName(spark, self.cluster_table_path)
                table_details_df = table_details.toDF()
                parent_keys = self.get_parent_keys(table_details_df, self.srcDatabaseName, self.srcTableName)
                parent_key_conditions = " AND ".join([f"t.{col} = s.{col}" for col in parent_keys])
                if not tgtDeltaTable.toDF().isEmpty():
                    tgtDeltaTable.alias("t").merge(microBatchOutputDF_8.alias("s"), parent_key_conditions) \
                    .whenMatchedDelete() \
                    .execute()
                microBatchOutputDF = self.preprocess_dataframe(microBatchOutputDF_8, parent_keys)

        windowSpec = Window.partitionBy(self.keyColsList).orderBy(col("hvr_integ_key").desc())

        microBatchOutputDF = microBatchOutputDF.withColumn("latest_record", row_number().over(windowSpec)).filter(
            "latest_record == 1").drop("latest_record")

        if self.enable_delete_filter == 'Y':
            microBatchOutputDF = self.filter_deleted_records(microBatchOutputDF)

        tgtDeltaTable.alias("t").merge(microBatchOutputDF.alias("s"), self.condition) \
            .whenMatchedDelete("s.source_operation in (0,3)") \
            .whenMatchedUpdate(condition="s.source_operation not in (0,3)", set=self.columnsDict) \
            .whenNotMatchedInsert(condition="s.source_operation not in (0,3)", values=self.columnsDict) \
            .execute()
 
    def streamIntoDeltaTarget(self):
        """
        desc:
            A Function for writing the given streaming dataframe into Delta Target table with foreachBatch merge
            Main layer the triggers/kicks off the entire process of reading from Bronze and merging into silver.
        args:
            None

        return:
            outputDF: DataFrame - Returns a spark streaming dataframe that writes into target delta table

        example:
            streamIntoDeltaTarget()

        tip:
            N/A
        """

        silverCleansedDF = self.silverCleansing()

        self.prepareTarget(silverCleansedDF)

        logger.info(f"phida_log: performing streaming merge on target {self.tgtDatabaseName}.{self.tgtTableName}")

        if self.triggerOnce == "Y":
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .trigger(once=True)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )
        else:
            outputDF = (silverCleansedDF.writeStream
                        .outputMode("update")
                        .option("checkpointLocation", self.tgtCheckpoint)
                        .option("failOnDataLoss", False)
                        .queryName(self.srcDatabaseName + "_" + self.srcTableName + "_to_" +
                                   self.tgtDatabaseName + "_" + self.tgtTableName)
                        .foreachBatch(self.upsertToDelta)
                        .start(self.tgtTablePath)
                        )

        return outputDF
