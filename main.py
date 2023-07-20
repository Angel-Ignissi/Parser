from install_driver import driver
from selenium.webdriver.common.by import By
from threading import Thread
from queue import Empty, Queue


def producer(queue):
    # if queue.empty():
    """Парсит по 1 цитате за раз и передает процесс другому потоку"""
    driver.get('https://finewords.ru/cit/delo')
    for elem in driver.find_elements(By.CLASS_NAME, 'cit'):
        # кладет в очередь эту цитату
        queue.put(elem.text)
    driver.quit()


def consumer(queue):
    """Поток-демон по этой функции обрабатывает очередь,
       пока очередь не закончится"""
    while True:
        try:
            element = queue.get()
        except Empty:
            continue
        else:
            with open('quotes.txt', 'a') as f:
                f.write(element)
                f.write('\n')
                f.write('\n')
            queue.task_done()


def main():
    queue = Queue()

    # создаем поток-производитель и запускаем его
    prod_thread = Thread(target=producer, args=(queue, ))
    prod_thread.start()

    consum_thread = Thread(target=consumer, args=(queue, ), daemon=True)
    consum_thread.start()

    prod_thread.join()
    queue.join()


if __name__ == '__main__':
    main()
