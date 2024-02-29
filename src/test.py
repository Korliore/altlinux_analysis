from modules.altlinux_api import AltLinuxAPI
import asyncio


async def main():
    api = AltLinuxAPI()
    data = await api.export_branch_binary_packages("sisyphus", "p10")
    print(data.keys())


# запускаем меин
if __name__ == "__main__":
    asyncio.run(main())
