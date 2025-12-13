from pyspark.sql.utils import AnalysisException
from com.phida.main.sparksession import spark
from pyspark.sql.functions import col


def tableExists(dbName, tblName):
    """
    desc:
        A static function for checking whether a given table exists.
        spark.catalog.tableExists method does not exist in python
        Although the scala method can be accessed using _jsparkSession, it is better to avoid using it

    args:
        dbName: String
        tblName: String

    return:
        Boolean - returns True or if it doesn't exists raises an exception

    example:
        tableExists("<database name>", "vbak")

    tip:
        N/A
    """
    try:
        spark.read.table(dbName + "." + tblName)
        return True
    except AnalysisException:
        return False


def getKeyCols(dbName, tblName):
    """
    desc:
        A Function for getting the primary key cols from the given table
        (Works only if source table is Bronze and src_key_cols is present in the table)

    args:
        dbName: String - A database name that is available in the catalog
        tblName: String - A Table name that is available in the catalog

    return:
        keyCols: String - returns the value of the column "src_key_cols" in the latest record
        of the given bronze table

    example:
        getKeyCols("<database name>", "vbuk")

    tip:
        Make sure the table is a bronze table and has the columns "src_key_cols" and "src_commit_time"
    """
    try:
        
        keyCols = (spark.read.table(dbName + "." + tblName)
                        .select("src_key_cols", "src_commit_time")
                        .limit(1)
                        .collect()[0][0]
                   )
        return keyCols

    except Exception:
        raise Exception(
            f"the column src_key_cols is not present in the given table {dbName}.{tblName}")


def hiveDDL(df):
    """
    desc:
        A static function for printing the schema of a given dataframe in hive DDL format.
        In scala, this can be achieved using df.schema.toDDL()
        but this function is not available on python without using _jdf()

    args:
        df: DataFrame - Just any spark dataframe

    return:
        ddl: String - the schema in hive ddl format as a string

    example:
        df = spark.read.table("<database name>.vbak")
        hiveDDL(df)

    tip:
        N/A
    """
    tblDDL = ""
    for columnName in df.dtypes:
        tblDDL = tblDDL + "`" + columnName[0] + "`" + " " + columnName[1] + ","

    tblDDL = tblDDL.rstrip(",")

    return tblDDL


def hasColumn(df, columnName):
    """
    A Function for checking whether a given column exists in a given dataframe

    args:
        df: DataFrame - a spark dataframe
        columnName: String - Column name as a string

    return:
        BOOLEAN - true or False

    example:
        df = spark.read.table("<database name>.vbuk")
        hasColumn(df, "erdat")

    tip:
        N/A
    """
    try:
        df.select(columnName)
        return True
    except AnalysisException:
        return False


def dropColumns(df, columnList):
    """
    desc:
        A Function for dropping the given columns in a given dataframe

    args:
        df: DataFrame - a spark dataframe
        columnList: List - A List containing column names as string

    return:
        df: DataFrame - returns the dataframe after dropping all the given columns in the list if they exist

    example:
        df = spark.read.table("<database name>.vbuk")
        dropColumns(df, ["src_commit_time", "hvr_integ_key"])

    tip:
        N/A

    """
    for columnName in columnList:

        if hasColumn(df, columnName):
            df = df.drop(columnName)
        else:
            pass

    return df


def addDerivedColumns(df, colExprList):
    """
    desc:
        A static Function for adding a derived partition column to a given dataframe.
        The function make sure the original columns are enclosed in `` to support special characters in the name

    args:
        df: DataFrame - given dataframe
        colExprList: List - A valid python list of spark expressions

    return:
        dfOut: DataFrame - The given dataframe after adding all the given derived columns

    examples:
        df = spark.read.table("<database name>.vbuk")
        somelist = ["cast(MANDT as int) as mandt_int","substr('vbeln',1,3) as sub_vbeln"]
        addDerivedColumns(df, somelist)

    Tips:
        1. Make sure that the expressions inside the list are enclosed by double quotes
        2. Do not use double quotes inside an expression
        3. Provide an alias for the derived column expression using as
    """
    columnList = df.columns

    new_columnList = []
    for column in columnList:
        new_column = f"`{column}`"
        new_columnList.append(new_column)

    columnList = new_columnList

    for colExpr in colExprList:
        try:
            df.selectExpr(colExpr)
        except Exception:
            raise Exception("The given column expression is invalid")

        columnList.append(colExpr)

    dfOut = df.selectExpr(columnList)

    return dfOut


def getDerivedColumnsList(colExprList):
    """
    desc:
        A static function for getting the list of columns that are derived from a given expression list

    args:
        colExprList: List - A valid python list of spark expressions.

    return:
        columnsList: List - returns the column name alone using the alias "as"

    example:
        somelist = ["date_format(to_date(col('erdat'),'yyyyMMdd'),'yyyyMM')) as yrmnth",
        "substr(col('vbeln'),1,3) as sub_vbeln"]
        getDerivedColumnsList(df, somelist)

    Tips:
        1. Make sure that the expressions inside the list are enclosed by double quotes
        2. Do not use double quotes inside an expression
        3. Provide an alias for the derived column expression using as
    """

    derivedColumnsList = []
    for columnName in colExprList:
        derivedColumnsList.append(columnName.split(" as ")[1].strip())

    return derivedColumnsList


def createDeltaTable(df, path, dbName, tblName, pCols=""):
    """
    desc:
        A static function for creating the target table using the given dataframe schema, database and table name

    args:
        df: DataFrame - A spark dataframe
        path: String - A path or an external location for the table
        dbName: String - Name of the database for creating the table
        tblName: String - Name of the table to be created
        pCols: String - partition columns as a string with the column names separated with a comma

    return:
        N/A - Does not return anything. Just creates the table on the catalog

    example:
        df = spark.read.table("<database name>.vbak").drop("src_commit_time")
        createDeltaTable(df, "/user/tmp/table/vbak", "<database name>", "vbak", "objectclas")

    tip:
        1. This function will only create an external table
        2. The table will be created with the below table properties:
            delta.autoOptimize.optimizeWrite = true,
            delta.tuneFileSizesForRewrites = true,
            delta.dataSkippingNumIndexedCols = 10,
            delta.enableChangeDataCapture = true"
    """

    tblDDL = hiveDDL(df)

    partitions = f" \n PARTITIONED BY ({pCols})" if pCols else ""

    tblProps = "delta.autoOptimize.autoCompact = false, \n\
         delta.autoOptimize.optimizeWrite = true, \n\
         delta.tuneFileSizesForRewrites = true, \n\
         delta.dataSkippingNumIndexedCols = 10, \n\
         delta.enableChangeDataCapture = true"

    createTable = "CREATE TABLE IF NOT EXISTS {dbName}.{tblName} ({tblDDL}) \n USING DELTA {partitions} " \
                  "\n LOCATION \"{path}\" \n TBLPROPERTIES ({tblProps})".format(
                    dbName=dbName,
                    tblName=tblName,
                    tblDDL=tblDDL,
                    partitions=partitions,
                    path=path,
                    tblProps=tblProps
                    )

    spark.sql(f"CREATE DATABASE IF NOT EXISTS {dbName}")

    spark.sql(createTable)


def schemaDiff(df1, df2):
    """
    desc:
        A static function for checking the difference between the schema of given 2 dataframes.
        df1 is the driving dataframe and hence is of importance. if there are extra columns in df2,
        that will not be identified by this function as this is not intended for that purpose

    args:
        df1: DataFrame - Given spark dataframe 1
        df2: DataFrame - Given spark dataframe 2

    return:
        df: DataFrame - returns a dataframe with the column,
        that are present in df1 but not in df2

    example:
        df1 = spark.read.table("<database name>.vbuk")
        df2 = spark.read.table("<database name>.vbuk")
        schemaDiff(df1,df1)

    Tips:
        1. Make sure that the first dataframe has got more columns than the second
    """
    df1_columns = df1.columns

    for columnName in df1.columns:
        if columnName in df2.columns:
            df1_columns.remove(columnName)

    df = df1.select(df1_columns)

    return df


def schemaDataTypeDiff(df1, df2):
    """
    desc:
        A static function for checking the difference of column data types of given 2 dataframes.
        The function only checks columns that are present in both dataframes. 
        If a column is present in one dataframe but not in the other, it will not be reflected here. 

    args:
        df1: DataFrame - Given spark dataframe 1
        df2: DataFrame - Given spark dataframe 2

    return:
        mismatched_columns: List - returns a list of column names,
        whose data types are different in the two given dataframes

    example:
        df1 = spark.read.table("<database name>.vbuk")
        df2 = spark.read.table("<database name>.vbuk")
        schemaDiff(df1,df2)
    """
    mismatched_columns = []

    for df1_column in df1.dtypes: 
        for df2_column in df2.dtypes: 
            if df1_column[0] == df2_column[0]:
                if df1_column[1] != df2_column[1]: 
                    mismatched_columns.append(df1_column[0])
                break
                
    return mismatched_columns


def alterDeltaTable(dbName, tblName, addColumns):
    """
    desc:
        A Function for altering the target table if there is a schema change in the source

    args:
        dbName: String - Name of the database for creating the table
        tblName: String - Name of the table to be created
        addColumns: String - newly added columns along with dataty[e in hive DDL format

    return:
        N/A - Does not return anything. Just adds columns to the given table

    example:
        alterDeltaTable("<database name>", "vbak", "yrmnth DATE")

    tip:
        1. This function will only add the given columns to the table
    """

    try:
        spark.sql(f"ALTER TABLE {dbName}.{tblName} ADD COLUMNS ({addColumns})")
    except AnalysisException:
        raise Exception(f"The given table {dbName}.{tblName} does not exist")


def buildColumnsDict(df, dropColumnList):
    """
    desc:
        A Function for building a data dictionary using the columns in the dataframe. (Coverts a list to data dict).
        This is used in whenMatchedUpdate and whenNotMatchedInsert clause of merge

    args:
        df: DataFrame - A spark dataframe

    return:
        columnsDict : Dict{String: String} - returns a python Dictionary

    example:
        df = spark.read.table("<database name>.vbuk")
        buildColumnsDict(df)

    tip:
        N/A

    """

    df = dropColumns(df, dropColumnList)

    columnsDict = {"`" + column + "`": f"s.`{column}`" for column in df.columns}

    return columnsDict


def buildJoinCondition(keyColsList):
    """
    desc:
        A Function for building the join condition for the merge using the key columns

    args:
        df: DataFrame - A spark dataframe

    return:
        condition : List - A List containing the key columns

    example:
        buildJoinCondition(["mandt","vbeln","kunnr"])

    tip:
        N/A
    """
    condition = ""

    for column in keyColsList:
        condition = condition + "t.`" + column + "` <=> " + "s.`" + column + "` AND "

    return condition[:-5]
