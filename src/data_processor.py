import pandas as pd
class DataProcessor:
    def process(self, records):
        df = pd.DataFrame([r["fields"] for r in records])
        return df
    def _detect_outliers(self, df):
        return df
