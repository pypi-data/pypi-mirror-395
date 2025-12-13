import os
from com.phida.main.sparksession import spark
from pyspark.sql.utils import AnalysisException

def convertToUnixPath(path):
    """
    desc:
        A Function for converting dbfs path to equivalent unix path with just a dbfs prefix.
        Converting to unix path is to make sure that even if the source path has wild characters,
        we will still be able to list the directory and check if that exists.
    args:
        path: String

    return:
        unixPath: String - returns the unix equivalent of a given dbfs path

    example:
        convertToUnixPath("dbfs:/tmp")

    tip:
        This just merely reformat the dbfs: to /dbfs/
    """
    unixPath = path.lstrip("dbfs:")

    unixPath = "dbfs:" + unixPath

    unixPath = unixPath.replace("dbfs:", "/dbfs")

    return unixPath


def pathExists(tablePath):
    """
    desc:
        A Function for determining whether a table path already exists.

    args:
        tablePath: String

    return:
        Boolean: True or False - depending on whether the path exists or not

    example:
        pathExists(/dbfs/tmp/target/table_path")

    tip:
        N/A
    """
    try:
        spark.read.load(tablePath)
        return True
    except AnalysisException:
        return False


def convertStrToList(string, sep):
    """
    desc:
        A static function for converting a string to a list, separated by given separator)

    args:
        string: String - a string value containing separators
        sep: String - a character used as a separator like comma (,) pipe (|), etc

    return:
        stringList : List - A string containing the entire join condition

    example:
        convertStrToList("abc,efg,hij", ",")

    tip:
        N/A
    """
    stringList = [item.strip() for item in string.split(f"{sep}")]

    return stringList
