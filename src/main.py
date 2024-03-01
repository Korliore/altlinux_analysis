import sys
from modules.altlinux_api import AltLinuxAPI
import asyncio
from modules.analize_data import AnalayzData, ShowData
from pprint import pprint
from modules.logger import logger


async def main(branch_name_1, branch_name_2, save_on_file):
    logger.info(f"Скачиваю данные для веток {branch_name_1} и {branch_name_2}")
    api = AltLinuxAPI()
    data = await api.export_branch_binary_packages(branch_name_1, branch_name_2)
    logger.info("Идёт анализ данных")
    # анализ всех данных
    analayz = AnalayzData(
        data[branch_name_1]["packages"], data[branch_name_2]["packages"]
    )
    # все пакеты, которые есть в sisyphus но нет в p10
    first_uniq = analayz.get_uniq_packages(
        analayz.first_branch_df, analayz.second_branch_df
    )
    # все пакеты, которые есть в p10 но нет в sisyphus
    second_uniq = analayz.get_uniq_packages(
        analayz.second_branch_df, analayz.first_branch_df
    )
    # все пакеты которые новее в 1 ветке
    version_new = analayz.version_release_check(
        analayz.first_branch_df, analayz.second_branch_df
    )
    logger.info("Формирую Json")
    data = ShowData(branch_name_1, branch_name_2).show(
        first_uniq, second_uniq, version_new
    )
    if save_on_file:
        logger.info(f"Идёт запись данных в {save_on_file}")
        with open(save_on_file, "w") as f:
            f.write(data)
    else:
        pprint(data)


if __name__ == "__main__":
    # Получение всех аргументов командной строки
    if len(sys.argv) < 2:
        raise Exception("Запусайте скрипт через ./get_stat.sh")
    arguments = sys.argv
    branch_name_1 = arguments[1]
    branch_name_2 = arguments[2]
    save_on_file = None
    if len(arguments) > 3:
        save_on_file = arguments[3]
    asyncio.run(main(branch_name_1, branch_name_2, save_on_file))
