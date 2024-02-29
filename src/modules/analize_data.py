import pandas as pd


class AnalayzData:
    def __init__(self, first_branch_data, second_branch_data):
        self.first_branch_df = self.get_df(first_branch_data)
        self.second_branch_df = self.get_df(second_branch_data)

    @staticmethod
    def get_df(data):
        df = pd.DataFrame(data)
        return df
