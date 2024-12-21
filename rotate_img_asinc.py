"""Асинхронный поворот изображения"""

from PIL import Image
import logging
import sys
import asyncio
import time
import pathlib
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
logging.getLogger("PIL.PngImagePlugin").disabled = True
logging.getLogger("matplotlib.font_manager").disabled = True
logging.getLogger("PIL.PngImagePlugin").disabled = True
logging.getLogger("matplotlib.pyplot").disabled = True


def rotate_image(file: Image) -> None:
    """
    Поворот изображения на 90 градусов
    :param file: файл изображения
    :return:
    """
    # поворот на 90 градусов
    return file.rotate(90)

async def start_task(file_lst: list) -> None:
    """
    Запуск поворота изображений из списка
    :param file_lst: список файлов изображений
    :return:
    """
    async def async_rotate_image(file):
        return rotate_image(file)
    tasks = []
    for file_i in file_lst:
        tasks.append(
            async_rotate_image(file_i)
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

    # создаем список файлов изображений
    here = pathlib.Path(__file__).parent
    outpath = here.joinpath("images")
    file_lst = []
    quantity_img = 10
    for _ in range(quantity_img):
        file_lst.append(Image.open(outpath.joinpath("1.jpg")))
    # запускаем поворот изображений из списка, фиксируем время выполнения
    time_lst = []
    for _ in range(quantity):
        start = time.perf_counter()
        asyncio.run(start_task(file_lst))
        finish = time.perf_counter()
        time_lst.append(finish - start)
        logger.info('Время работы: ' + str(finish - start))

    # среднее значение времени
    mean_time = sum(time_lst) / quantity
    logger.info('Среднее время поворота изображения (асинхронно): ' + str(mean_time))
    # строим график по полученным значениям
    f, ax = plt.subplots(1)
    f.set_size_inches(8, 8)
    ax.plot(list(range(1, quantity + 1)), np.array(time_lst), color='green', marker='o', markersize=7)
    ax.axline((0, mean_time), (quantity, mean_time), color='red', linestyle='dashed')
    plt.xlabel('Итерация')  # Подпись для оси х
    plt.ylabel('Время поворота изображения, сек')  # Подпись для оси y
    plt.title(f'Время поворота изображения (асинхронно), среднее - {round(mean_time, 2)} сек.')  # Название
    ax.set_ylim([0, 5.0])
    ax.set_xlim([1, quantity])

    if save_fig:
        here = pathlib.Path(__file__).parent
        path_fig = here.joinpath("save_fig")
        path_fig = path_fig.joinpath("rotate_asinc.jpg")
        plt.savefig(path_fig)
    if plot_fig:
        plt.show()

    return mean_time


if __name__ == "__main__":
    runner(20, plot_fig=True, save_fig=True)