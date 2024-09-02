import asyncio
import time


async def start_strongman(name, power):
    print("Силач {} начал соревнование".format(name))
    await asyncio.sleep(1 / power)
    for i in range(1,6):

        print("Силач {} поднял шар №{}".format(name, i))
        await asyncio.sleep(1/power)
    print("Силач {} завершил соревнование".format(name))


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))

    await asyncio.gather(task1, task2, task3)


asyncio.run(start_tournament())