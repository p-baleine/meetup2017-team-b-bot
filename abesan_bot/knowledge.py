import re

class Knowledge(object):
    def __init__(self, sheet_df):
        self._sheet_df = sheet_df
        pass

    def query(self, event):
        return self.sub_user_name(event, self._sheet_df[self._sheet_df["Input"].str.contains(event["text"], na=False)]["Output"].iloc[0])

    def sub_user_name(self, event, text):
        return re.sub(r'^(.*){{USER}}(.*)$',
                      r'\1<@{}>\2'.format(event["user"]),
                      text)
