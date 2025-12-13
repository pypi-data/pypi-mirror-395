import dbutils
from com.phida.main.sparksession import spark
from com.phida.main.Operations import tableExists, getKeyCols, hiveDDL, hasColumn, dropColumns, \
    addDerivedColumns, getDerivedColumnsList, createDeltaTable, schemaDiff, alterDeltaTable, buildColumnsDict, \
    buildJoinCondition
from pyspark.sql.functions import lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


class StaticMethodsTest:
    def __init__(self):
        self.data = [(1, "chandler", "sarcastic"),
                     (2, "joey", "innocent")
                     ]

        self.schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("character", StringType(), True)
                                ])

        self.df = spark.createDataFrame(self.data, self.schema)

        self.rangeDF = spark.range(10)

        spark.sql("CREATE DATABASE phida_test")

        spark.sql("CREATE OR REPLACE TABLE phida_test.static_methods_test( \
                          src_key_cols STRING, \
                          src_commit_time TIMESTAMP) \
                          USING DELTA")

        spark.sql("INSERT INTO default.streaming_testcase_get_key_cols VALUES ('mandt,vbeln','2022-01-01 11:59:59')")

        spark.sql("INSERT INTO default.streaming_testcase_get_key_cols VALUES ('nothing','2022-01-01 11:59:58')")

    @staticmethod
    def tableExistsTest():
        test_table_exists = tableExists("phida_test", "static_methods_test")

        test_table_not_exists = tableExists("phida_test", "some_random_name_test")

        assert test_table_exists is True

        assert test_table_not_exists is False

    @staticmethod
    def getKeyColsTest():
        test_get_key_cols = getKeyCols("default", "streaming_testcase_get_key_cols")

        assert test_get_key_cols == 'mandt,vbeln'

        spark.sql("DROP TABLE IF EXISTS default.streaming_testcase_get_key_cols")

    @staticmethod
    def hiveDDLTest(self):
        test_hive_ddl = hiveDDL(self.rangeDF)

        assert test_hive_ddl == "`id` bigint'"

    @staticmethod
    def hasColumnTest(self):
        # Positive test case scenario
        test_hasColumn1 = hasColumn(self.df, "name")

        assert test_hasColumn1 is True

        # Negative test case scenario
        test_hasColumn2 = hasColumn(self.df, "first_name")

        assert test_hasColumn2 is False

    @staticmethod
    def dropColumnsTest(self):
        # Positive test case scenario
        assert dropColumns(self.df, ["id", "character"]).schema == StructType([StructField("name", StringType(), True)])

        # Negative test case scenario
        assert dropColumns(self.df, ["name", "unknown_column_name"]).schema == StructType(
            [StructField("id", IntegerType(), True),
             StructField("character", StringType(), True)])

    def addDerivedColumnsTest(self):

        newDF = addDerivedColumns(self.df, "substring(character, -3, 3) as p_character")

        testSchema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("character", StringType(), True),
            StructField("p_character", StringType(), True)
        ])

        assert testSchema == newDF.schema

    @staticmethod
    def getDerivedColumnsListTest():

        exprList = ["substring(character, -3, 3) as p_character", "lit('1') as mandt"]

        derivedColumnsList = getDerivedColumnsList(exprList)

        assert derivedColumnsList == ["p_character", "mandt"]

    def createDeltaTableTest(self):
        createDeltaTable(self.df, "/tmp/phida_test/streaming_testcase_createdeltatable", "default",
                         "streaming_testcase_createdeltatable", "")

        assert spark.read.table("default.streaming_testcase_createdeltatable").schema == self.schema

        spark.sql("drop table if exists default.streaming_testcase_createdeltatable")

    def schemaDiffTest(self):
        newDF = self.df.withColumn("age", lit("30"))

        assert schemaDiff(newDF, self.df) == "`age` string'"

    def alterDeltaTableTest(self):
        createDeltaTable(self.df, "/tmp/phida_test/streaming_testcase_createdeltatable", "default",
                         "streaming_testcase_createdeltatable", "")

        alterDeltaTable("default", "streaming_testcase_createdeltatable", "`age` string'")

        assert spark.read.table("default.streaming_testcase_createdeltatable").schema == StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
            StructField("character", StringType(), True),
            StructField("age", StringType(), True)
        ])

    def buildColumnsDictTest(self):
        test_buildColumnsDict = buildColumnsDict(self.df)

        outputDict = {'id': 's.id', 'name': 's.name', 'character': 's.character'}

        assert test_buildColumnsDict == outputDict

    @staticmethod
    def buildJoinConditionTest(self):
        test_buildCondition = buildJoinCondition("mandt,vbeln")

        assert test_buildCondition == "t.mandt = s.mandt AND t.vbeln = s.vbeln"

    @staticmethod
    def cleanUpTables():
        spark.sql("DROP DATABASE IF EXISTS phida_test CASCADE")

        dbutils.fs.rm("/tmp/phida_test/streaming_testcase_createdeltatable", recurse=True)


if __name__ == "__main__":
    unitTests = StaticMethodsTest()

    unitTests.tableExistsTest()
    unitTests.getKeyColsTest()
    unitTests.hiveDDLTest()
    unitTests.hasColumnTest()
    unitTests.dropColumnsTest()
    unitTests.addDerivedColumnsTest()
    unitTests.getDerivedColumnsListTest()
    unitTests.createDeltaTableTest()
    unitTests.cleanUpTables()
