import pandas as pd
from modules.other.version_compare import _compare_rpm_labels


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

    def version_release_check(self, first_df, second_df):
        """Получить пакеты, где версии в first_df больше second_df"""
        new_version = {}
        unique_architectures = first_df["arch"].unique()

        for arch in unique_architectures:
            df1_arch = first_df[first_df["arch"] == arch]
            df2_arch = second_df[second_df["arch"] == arch]

            merged_df = df1_arch.merge(
                df2_arch, on="name", suffixes=("_df1", "_df2"), how="inner"
            )

            for index, row in merged_df.iterrows():
                version1 = row["version_df1"]
                release1 = row["release_df1"]
                epoch1 = row["epoch_df1"]
                version2 = row["version_df2"]
                release2 = row["release_df2"]
                epoch2 = row["epoch_df2"]
                comparison_result = _compare_rpm_labels(
                    (epoch1, version1, release1), (epoch2, version2, release2)
                )
                if comparison_result == 1:
                    new_version[arch] = row
        return new_version
