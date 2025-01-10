# **Сравнение различных подходов к реализации асинхронного программирования: asyncio, threading и multiprocessing**
## **Введение**
Асинхронное программирование в Python становится все более важным в разработке высокопроизводительных и масштабируемых приложений. Этот проект посвящен сравнительному анализу трех ключевых подходов к асинхронному программированию: asyncio, threading и multiprocessing. Цель исследования заключается в оценке производительности и уместности каждого подхода в зависимости от типа задач.
## Основные понятия
+ **Асинхронное программирование**: Позволяет выполнять задачи параллельно, не блокируя основной поток выполнения программы.
+ **Threading**: Механизм многопоточности для параллельного выполнения задач в рамках одного процесса.
+ **Multiprocessing**: Запуск нескольких процессов, каждый из которых выполняется независимо от других.
+ **Asyncio**: Библиотека для написания асинхронного кода с использованием синтаксиса async/await.
## Методы реализации
Проект включает примеры использования всех трех подходов для различных типов задач:
1. **I/O-bound задачи** - Например, асинхронная загрузка данных с веб-сервера.
2. **CPU-bound задачи** - Выполнение вычислительно сложных операций, таких как вычисление факториала.
3. **Задачи с высокой параллельностью** - Массовая обработка небольших файлов или данных.
## Запуск методов для сбора статистики
Для запуска сбора статистики по каждому виду из исследуемых задач, можно запустить непосредственно необходимый модуль, указав в функции runner() количество вызовов для сбора статистики, необходимость отображения графика статистики на экране, необходимость сохранения графика статистики в файл
![logo](resources/request_site_asinc.png)
Также можно импортировать модуль целиком в Ваш проект и запускать функцию runner() с необходимыми параметрами
![logo](resources/request_site_asinc_import.png)
## Сравнительный анализ
+ **Asyncio**: Идеален для задач, связанных с вводом-выводом, где требуется высокая производительность и масштабируемость.
+ **Threading**: Хорошо подходит для параллельной обработки задач, связанных с ожиданием, особенно в многозадачных приложениях.
+ **Multiprocessing**: Эффективен для задач, требующих интенсивных вычислений и использования нескольких ядер процессора.
## Заключение
Проект показал, что каждый подход имеет свои сильные и слабые стороны в зависимости от специфики задачи. Полученные результаты могут быть полезны для выбора оптимального подхода при разработке высокопроизводительных приложений на Python.

