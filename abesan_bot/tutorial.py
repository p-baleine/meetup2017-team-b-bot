class Sequence(object):
    def __init__(self, sheet_df):
        self._sheet_df = sheet_df
        pass

    def query(self, event):
        return self._sheet_df["Output"][0]
