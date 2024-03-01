import pandas as pd
from modules.other.version_compare import _compare_rpm_labels
import json


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
        unique_packages_by_arch = {}
        for arch in unique_architectures:
            # фильтр по архитектуре
            df1_arch = first_df[first_df["arch"] == arch]
            df2_arch = second_df[second_df["arch"] == arch]
            # поиск уникальных значений
            unique_packages = df1_arch[~df1_arch["name"].isin(df2_arch["name"])]
            unique_packages_by_arch[arch] = unique_packages
        unique_df = pd.concat(unique_packages_by_arch.values(), ignore_index=True)
        return unique_df

    def version_release_check(self, first_df, second_df):
        """Получить пакеты, где версии в first_df больше second_df"""
        new_versions = []  # список для хранения строк, удовлетворяющих условию

        unique_architectures = first_df["arch"].unique()

        for arch in unique_architectures:
            df1_arch = first_df[first_df["arch"] == arch]
            df2_arch = second_df[second_df["arch"] == arch]

            merged_df = df1_arch.merge(
                df2_arch, on="name", suffixes=("_df1", "_df2"), how="inner"
            )

            for index, row in merged_df.iterrows():
                version1 = str(row["version_df1"])
                release1 = str(row["release_df1"])
                epoch1 = str(row["epoch_df1"])
                version2 = str(row["version_df2"])
                release2 = str(row["release_df2"])
                epoch2 = str(row["epoch_df2"])
                comparison_result = _compare_rpm_labels(
                    (epoch1, version1, release1), (epoch2, version2, release2)
                )
                if comparison_result == 1:
                    new_versions.append(
                        row.to_dict()
                    )  # Преобразуем строку в словарь и добавляем в список

        unique_df = pd.DataFrame(new_versions)  # Создаем DataFrame из списка словарей
        return unique_df


class ShowData:
    def __init__(self, first_branch_name, second_branch_name):
        self.first_branch_name = first_branch_name
        self.second_branch_name = second_branch_name
        self.json_data = {}

    def uniq_to_json(self, first_branch, second_branch, branch_name, branch_name_user):
        """Генерация json для уникальных данных"""
        unique_first_branch_list = []
        grouped = first_branch.groupby("arch")
        for name_arch, group in grouped:
            pkg_list = []
            for index, row in group.iterrows():
                pkg_info = {
                    "name": row["name"],
                    "version": row["version"],
                    "epoch": row["epoch"],
                    "release": row["release"],
                    "arch": row["arch"],
                    "branch": branch_name_user,
                }
                pkg_list.append(pkg_info)
            unique_first_branch_list.append({"arch": name_arch, "pkg": pkg_list})
        self.json_data[branch_name] = unique_first_branch_list

    def newer_version_to_json(self, df_version):
        unique_first_branch_list = []
        grouped = df_version.groupby("arch_df1")
        for arch_name, group in grouped:
            pkg_list = []
            for index, row in group.iterrows():
                pkg_info = {
                    "newer_version": {
                        "name": row["name"],
                        "version": row["version_df1"],
                        "epoch": row["epoch_df1"],
                        "release": row["release_df1"],
                        "arch": row["arch_df1"],
                        "branch": self.first_branch_name,
                    },
                    "older_version": {
                        "name": row["name"],
                        "version": row["version_df2"],
                        "epoch": row["epoch_df2"],
                        "release": row["release_df2"],
                        "arch": row["arch_df1"],
                        "branch": self.second_branch_name,
                    },
                }
                pkg_list.append(pkg_info)
            unique_first_branch_list.append({"arch": arch_name, "pkg": pkg_list})
        self.json_data["version_newer"] = unique_first_branch_list

    def show(self, first_branch, second_branch, version_data_df):
        """Переводит датафрейм в json и отдает"""
        self.uniq_to_json(
            first_branch, second_branch, "unique_first_branch", self.first_branch_name
        )
        self.uniq_to_json(
            second_branch, first_branch, "unique_second_branch", self.second_branch_name
        )
        self.newer_version_to_json(version_data_df)
        return json.dumps(self.json_data)
