# Created by Noé Cruz | Zurckz 22 at 23/04/2022
# See https://www.linkedin.com/in/zurckz
from multiprocessing import Pool, cpu_count, Process, Queue
from time import perf_counter, sleep
from zpy.logger import ZLogger
from typing import Any, Callable, Iterable, List, Optional, Tuple, Union

_func: Optional[Callable[[Any], Any]] = None


def worker_init(func):
    global _func
    _func = func


def worker(x):
    return _func(x)


def _task_wrapper(idx, queue, task, args):
    queue.put((idx, task(*args)))


def mapp(
        collection: Iterable[Any],
        fn: Callable[[Any], Any],
        chunk_size: Optional[int] = 1,
        args: Optional[Tuple[Any]] = None,
) -> List[Any]:
    """Parallel Collection Processor

    Args:
        collection (Iterable[Any]): Iterable
        fn (Callable[[Any], Any]): Map function
        chunk_size (Optional[int]): chunk size. Default 1
        args: Args
    Returns:
        List[Any]: iterable

    """
    n_cpu = cpu_count()
    if args:
        with Pool(processes=n_cpu) as pool:
            return pool.starmap(fn, [(e,) + args for e in collection], chunk_size)

    with Pool(processes=n_cpu, initializer=worker_init, initargs=(fn,)) as pool:
        return pool.map(worker, collection, chunk_size)


def runp(
        tasks: List[Callable[[Any], Any]], args: Optional[List[Tuple[Any]]] = None
) -> List[Any]:
    """Run tasks in parallel.

    Args:
        tasks (List[Callable[[Any], Any]]): Collection of tasks references
        args (Optional[List[Tuple[Any]]], optional): Args of tasks. Defaults to None.

    Raises:
        ValueError: if the number of args and tasks aren't the same

    Returns:
        List[Any]: Ordered Tasks result
    """
    if args is not None and len(tasks) != len(args):
        raise ValueError("Number of args must be equal to number of tasks.")

    queue = Queue()
    processes = [
        Process(
            target=_task_wrapper,
            args=(i, queue, task, () if not args else args[i]),
        )
        for i, task in enumerate(tasks)
    ]
    for process in processes:
        process.start()
    for process in processes:
        process.join()

    return [value[1] for value in sorted([queue.get() for _ in processes])]


class TaskExecutor:

    def __init__(self, task: Any, args=(), logger: ZLogger = None):
        self.queue = Queue()
        self.task = task
        self.args = args
        self.logger = logger

    def terminator(self, queue: Queue, seconds):
        sleep(seconds)
        if queue.empty():
            queue.put("TASK_FINISHED_BY_TIMEOUT")

    def runner(self, queue: Queue, task, args):
        queue.put(task(*args))

    def run(self, timeout: float = 0.0, default_value: Any = None):
        start = perf_counter()
        try:
            runner = Process(target=self.runner, args=(self.queue, self.task, self.args))
            scheduler = Process(target=self.terminator, args=(self.queue, timeout))
            scheduler.start()
            runner.start()
            while True:
                if not self.queue.empty():
                    value = self.queue.get()
                    if value == 'TASK_FINISHED_BY_TIMEOUT':
                        if runner.is_alive():
                            runner.terminate()
                        if self.logger:
                            end = perf_counter()
                            self.logger.info(f"Task execution finished by timeout. {round(end - start, 2)}s.")
                        return default_value
                    if scheduler.is_alive():
                        scheduler.terminate()
                    if self.logger:
                        end = perf_counter()
                        self.logger.info(f"Task execution finished successfully. {round(end - start, 2)}s.")
                    return value
        except Exception as e:
            if self.logger:
                self.logger.exception("An error occurred while executing task", exc_info=e)
            else:
                print("An error occurred while executing task", e)
            return default_value
