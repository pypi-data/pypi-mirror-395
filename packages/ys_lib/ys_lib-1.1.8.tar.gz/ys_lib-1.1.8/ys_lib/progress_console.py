# -*- coding: utf-8 -*-
import collections
import functools
import multiprocessing
import threading
import time
from rich.box import SIMPLE_HEAD
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.text import Text
from typing import Deque
from loguru import logger


class LogHandler:
    MAX_LOGS: int = 1000
    logs: Deque[str] = collections.deque(maxlen=MAX_LOGS)
    counter = multiprocessing.Value('l', 0)

    @classmethod
    def hijack(cls, record: str):
        # 获取对应的 logging 级别
        cls.logs.appendleft(record.rstrip('\n'))
        with cls.counter.get_lock():
            cls.counter.value += 1


logger.remove()
logger.add(LogHandler.hijack, level="TRACE", colorize=True)


class ProgressConsole:
    layout = Layout()
    layout.split(
        Layout(name="progress", size=2, visible=False),
        Layout(renderable=Panel(Text(), box=SIMPLE_HEAD, title=f"日志"), name="logs", ratio=1),
    )
    progress: Progress| None = None
    console = Console(record=False)

    @classmethod
    def new_progress(cls, filename: bool = False) -> Progress:
        cs = [
            TextColumn("[yellow]{task.description}", justify="left"),
            "•",
            TextColumn("[bold blue]{task.fields[filename]}", justify="right") if filename else None,
            "•" if filename else None,
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        ]
        return Progress(*[c for c in cs if c is not None])

    @classmethod
    def set_progress(cls, progress: Progress):
        cls.progress = progress
        cls.layout["progress"].visible = True
        cls.layout["progress"].update(
            Panel(cls.progress, title="进度监控", border_style="blue")
        )

    @classmethod
    def update_log_display(cls):
        """更新日志区域的显示内容"""
        # 添加所有缓冲区中的日志，每行之间用换行符分隔
        height: int = cls.console.height
        text = Text()
        for i, line in enumerate(LogHandler.logs.copy()):
            text.append(line + '\n')
            if i == height - 1:
                break
        cls.layout["logs"].update(
            Panel(text, box=SIMPLE_HEAD, title=f"日志")
        )

    @classmethod
    def live(cls, *partials: functools.partial):
        # 使用Live显示动态界面
        counter: int = 0
        size: int = 0
        with Live(cls.layout, console=cls.console, refresh_per_second=20, screen=True) as live:
            task_threads = []
            for partial in partials:
                task_thread = threading.Thread(target=partial, daemon=True)
                task_thread.start()
                task_threads.append(task_thread)
            for task_thread in task_threads:
                while task_thread.is_alive():
                    # 按需更新日志
                    _counter = LogHandler.counter.value
                    if _counter != counter:
                        cls.update_log_display()
                        counter = _counter
                    # 调整进度条区域高度
                    if cls.progress:
                        _size: int = len(cls.progress.tasks) + 2
                        if _size != size:
                            cls.layout["progress"].size = size = _size
                    live.refresh()
                    time.sleep(0.05)
        cls.console.print(cls.layout)
        cls.console.log("[bold green]\n所有任务已完成！")


if __name__ == '__main__':
    progress = ProgressConsole.new_progress(filename=False)

    def run_tasks(progress: Progress) -> None:
        task1 = progress.add_task(description="[cyan]下载文件", total=100)
        task2 = progress.add_task(description="[green]处理数据", total=150)
        task3 = progress.add_task(description="[green]处理数据1", total=60)
        task3_done = False

        try:
            while not progress.finished:
                progress.update(task1, advance=0.5)
                progress.update(task2, advance=0.8)
                if not task3_done:
                    progress.update(task3, advance=2)
                time.sleep(1)
                # 模拟日志输出
                logger.info("任务进行中... 状态正常")
                logger.warning(time.time())
                if progress.tasks[0].completed > 30:
                    logger.warning("遇到非关键性延迟")
                if progress.tasks[1].completed > 100:
                    logger.error("数据处理阶段出现异常")
                if len(progress.tasks) > 2 and progress.tasks[2].completed >= 60:
                    progress.stop_task(task3)
                    progress.remove_task(task3)
                    task3_done = True
                logger.debug(f'loguru debug: {time.time()}')
                logger.error(f'loguru error: {time.time()}')
                logger.success(f'loguru success: {time.time()}')
                logger.critical(f'loguru critical: {time.time()}')
        except Exception as e:
            logger.exception(e)

    ProgressConsole.set_progress(progress=progress)
    ProgressConsole.live(functools.partial(run_tasks, progress), functools.partial(run_tasks, progress))
