"""Многопроцессорный поворот изображения"""

import logging
import pathlib
import sys
import multiprocessing
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


def start_task(number_lst: list, pool: multiprocessing.Pool) -> None:
    """
    Запуск серии вычислений факториала
    :param number_lst: список чисел для вычисления факториала
    :param pool: пул процессов
    :return:
    """

    pool.map(calculate_factorial, number_lst)


def runner(quantity, plot_fig=False, save_fig=False) -> float:
    """
    Запуск сбора статистики
    :param quantity: количество итераций
    :param plot_fig: отрисовать график
    :param save_fig: сохранить график
    :return:
    """

    # запускаем процессы 1 раз, чтобы избавиться от накладных расходов на их перезапуск в цикле
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    # основание факториала
    number = 7000
    number_lst = []
    for _ in range(100):
        number_lst.append(number)
    # запускаем каждую серию вычислений, фиксируем время выполнения
    time_lst = []
    for _ in range(quantity):
        start = time.perf_counter()
        start_task(number_lst, pool)
        finish = time.perf_counter()
        time_lst.append(finish - start)
        logger.info('Время работы: ' + str(finish - start))

    # среднее значение времени
    mean_time = sum(time_lst) / quantity
    logger.info('Среднее время вычисления факториала (по процессам): ' + str(mean_time))
    # строим график по полученным значениям
    f, ax = plt.subplots(1)
    f.set_size_inches(8, 8)
    ax.plot(list(range(1, quantity + 1)), np.array(time_lst), color='green', marker='o', markersize=7)
    ax.axline((0, mean_time), (quantity, mean_time), color='red', linestyle='dashed')
    plt.xlabel('Итерация')  # Подпись для оси х
    plt.ylabel('Время вычисления факториала, сек')  # Подпись для оси y
    plt.title(f'Время вычисления факториала (по процессам), среднее - {round(mean_time, 2)} сек.')  # Название
    ax.set_ylim([0, 3.0])
    ax.set_xlim([1, quantity])

    if save_fig:
        here = pathlib.Path(__file__).parent
        path_fig = here.joinpath("save_fig")
        path_fig = path_fig.joinpath("factorial_multiproc.jpg")
        plt.savefig(path_fig)
    if plot_fig:
        plt.show()

    return mean_time


if __name__ == "__main__":
    runner(50, plot_fig=True, save_fig=True)
