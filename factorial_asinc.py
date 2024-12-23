"""Асинхронное вычисление факториала"""

import logging
import pathlib
import sys
import asyncio
import time
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


def calculate_factorial(number: int) -> int:
    """
    Вычисление факториала числа
    :param number: число
    :return: факториал
    """
    factorial = 1
    for i in range(2, number + 1):
        factorial *= i
    return factorial


async def start_task(number: int) -> None:
    """
    Запуск серии вычислений факториала
    :param number: число для вычисления факториала
    :return:
    """

    async def async_calculate_factorial(number):
        return calculate_factorial(number)

    tasks = []
    for _ in range(100):
        tasks.append(
            async_calculate_factorial(number)
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
    # основание факториала
    number = 7000
    # запускаем каждую серию вычислений, фиксируем время выполнения
    time_lst = []
    for _ in range(quantity):
        start = time.perf_counter()
        asyncio.run(start_task(number))
        finish = time.perf_counter()
        time_lst.append(finish - start)
        logger.info('Время работы: ' + str(finish - start))

    # среднее значение времени
    mean_time = sum(time_lst) / quantity
    logger.info('Среднее время вычисления факториала (асинхронно): ' + str(mean_time))
    # строим график по полученным значениям
    f, ax = plt.subplots(1)
    f.set_size_inches(8, 8)
    ax.plot(list(range(1, quantity + 1)), np.array(time_lst), color='green', marker='o', markersize=7)
    ax.axline((0, mean_time), (quantity, mean_time), color='red', linestyle='dashed')
    plt.xlabel('Итерация')  # Подпись для оси х
    plt.ylabel('Время вычисления факториала, сек')  # Подпись для оси y
    plt.title(f'Время вычисления факториала (асинхронно), среднее - {round(mean_time, 2)} сек.')  # Название
    ax.set_ylim([0, 3.0])
    ax.set_xlim([1, quantity])

    if save_fig:
        here = pathlib.Path(__file__).parent
        path_fig = here.joinpath("save_fig")
        path_fig = path_fig.joinpath("factorial_asinc.jpg")
        plt.savefig(path_fig)
    if plot_fig:
        plt.show()

    return mean_time


if __name__ == "__main__":
    runner(50, plot_fig=True, save_fig=True)

