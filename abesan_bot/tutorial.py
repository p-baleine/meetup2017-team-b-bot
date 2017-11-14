import pandas as pd 
import re

class Sequence(object):
    def __init__(self, sheet_df):
        self._sheet_df = sheet_df
        self._sheet_row_id = 0.0

    def next(self, event):
        msgs = [self.sub_user_name(event, x) for x in self._sheet_df[self._sheet_df['ID']==self._sheet_row_id]['Output'].tolist()]
        self._sheet_row_id += 1
        return msgs

    def is_finished(self):
        return self._sheet_row_id == 4.0

    def sub_user_name(self, event, text):
        user = event["inviter"] if "inviter" in event else event["user"]
        return re.sub(r'^(.*){{USER}}(.*)$',
                      r'\1<@{}>\2'.format(user),
                      text,
                      flags=re.MULTILINE)
