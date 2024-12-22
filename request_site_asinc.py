"""Асинхронный запрос HTML страниц"""

import asyncio
import logging
import pathlib
import sys
import time
import aiofiles
from aiohttp import ClientSession
import matplotlib.pyplot as plt
import numpy as np

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("------")
logging.getLogger("asyncio").disabled = True
logging.getLogger("matplotlib.font_manager").disabled = True
logging.getLogger("PIL.PngImagePlugin").disabled = True
logging.getLogger("matplotlib.pyplot").disabled = True


async def fetch_html(url: str, session: ClientSession) -> str:
    """
    Запрос страницы сайта
    :param url: адрес сайта
    :param session: сессия, под которой делаем запрос
    :return: html страница сайта
    """

    resp = await session.request(method="GET", url=url)
    resp.raise_for_status()
    html = await resp.text()
    return html


async def write_one(file: pathlib.Path, url: str, session: ClientSession) -> None:
    """
    Запись страницы html в файл
    :param file: расположение выходного файла
    :param url: адрес сайта
    :param session: сессия, под которой делаем запрос
    :return: None
    """

    # запрашиваем страницу сайта
    res = await fetch_html(url=url, session=session)
    if not res:
        return None
    # записываем страницу в файл
    async with aiofiles.open(file, "a", encoding="utf-8") as f:
        await f.write(f"{url}{res}")


async def start_task(file: pathlib.Path, urls: set) -> None:
    """
    Запуск записи в файл страниц, полученных из списка сайтов
    :param file: расположение выходного файла
    :param urls: список сайтов
    :return:
    """
    # открываем сессию
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session)
            )
        await asyncio.gather(*tasks)


def runner(quantity, plot_fig=False, save_fig=False) -> float:
    """
    Запуск сбора статистики
    :param quantity: количество итераций
    :param plot_fig: отрисовать график
    :param save_fig: сохранить график
    :return:
    """

    # определяем текущую директорию
    here = pathlib.Path(__file__).parent
    # открываем файл с сайтами и заполняем список
    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))
    # определяем выходной файл
    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("\n")
    # список времен выполнения каждой пачки запросов
    time_lst = []
    # запускаем каждую пачку запросов, фиксируем время выполнения
    for _ in range(quantity):
        start = time.perf_counter()
        asyncio.run(start_task(file=outpath, urls=urls))
        finish = time.perf_counter()
        time_lst.append(round(finish - start, 2))
        logger.info('Время работы: ' + str(finish - start))

    # среднее значение времени выполнения пачки запросов
    mean_time = sum(time_lst) / quantity
    logger.info('Среднее время работы (http запросы асинхронно): ' + str(mean_time))
    # строим график по полученным значениям
    f, ax = plt.subplots(1)
    f.set_size_inches(8, 8)
    ax.plot(list(range(1, quantity + 1)), np.array(time_lst), color='green', marker='o', markersize=7)
    ax.axline((0, mean_time), (quantity, mean_time), color='red', linestyle='dashed')
    plt.xlabel('Итерация')  # Подпись для оси х
    plt.ylabel('Время выполнения запросов, сек')  # Подпись для оси y
    plt.title(f'Время выполнения запросов (асинхронно), среднее - {round(mean_time,2)} сек.')  # Название
    ax.set_ylim([0, 5])
    ax.set_xlim([1, quantity])
    if save_fig:
        path_fig = here.joinpath("save_fig")
        path_fig = path_fig.joinpath("site_asinc.jpg")
        plt.savefig(path_fig)
    if plot_fig:
        plt.show()

    return mean_time


if __name__ == "__main__":
    runner(50, plot_fig=True, save_fig=True)

