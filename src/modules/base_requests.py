class Reqests:
    async def get(url, session):
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            raise Exception(f"Ошибка при получении данных с {url}: {response.status}")
