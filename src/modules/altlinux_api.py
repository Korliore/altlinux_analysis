import asyncio
import aiohttp
from modules.base_requests import Reqests


class AltLinuxAPI:
    def __init__(self):
        self.base_url = "https://rdb.altlinux.org/api"

    async def export_branch_binary_packages(
        self, branch_name_1: str, branch_name_2: str
    ):
        """Получить данные из указанных веток

        Args:
            branch_name_1 (str): 1 ветка
            branch_name_2 (str): 2 ветка

        Returns:
            dict: Словарь с результатами запросов, где ключ - URL
        """
        url = f"{self.base_url}/export/branch_binary_packages"
        urls = [
            f"{url}/{branch_name_1}",
            f"{url}/{branch_name_2}",
        ]

        async with aiohttp.ClientSession() as session:
            tasks = [Reqests.get(url, session) for url in urls]
            results = await asyncio.gather(*tasks)

            data = {}
            for url, result in zip(urls, results):
                data[url.split("/")[-1]] = result

            return data
