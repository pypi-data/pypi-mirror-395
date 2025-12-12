from pyspark.sql import DataFrame

# ==========================
# SourceData Class
# ==========================

class SourceData:
    def __init__(self, data: DataFrame):
        self.df: DataFrame = data
