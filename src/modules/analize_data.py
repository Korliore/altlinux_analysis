import pandas as pd


class AnalayzData:
    def __init__(self, first_branch_data, second_branch_data):
        self.first_branch_df = self.get_df(first_branch_data)
        self.second_branch_df = self.get_df(second_branch_data)

    @staticmethod
    def get_df(data):
        """Получить датафрейм"""
        df = pd.DataFrame(data)
        return df

    def get_uniq_packages(self, first_df, second_df):
        """Получить уникальные пакеты"""
        unique_architectures = first_df["arch"].unique()
        missing_packages_by_arch = {}
        for arch in unique_architectures:
            # фильтр по архитектуре
            df1_arch = first_df[first_df["arch"] == arch]
            df2_arch = second_df[second_df["arch"] == arch]
            # поиск уникальных значений
            missing_packages = df1_arch[~df1_arch["name"].isin(df2_arch["name"])]
            missing_packages_by_arch[arch] = missing_packages
        return missing_packages_by_arch
