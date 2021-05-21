from typing import Optional
from algoanim.array import Array
import os
from algoanim.utils import SORTS_DIR
from algoanim.sort import Sort, SortThread, load_sort_file
from threading import Thread
import tkinter as tk
import tkinter.ttk as ttk

from algoanim.graphics import GraphicsThread


class MainWindow:
    root: tk.Tk
    choose_sort: ttk.Combobox
    graphics: GraphicsThread
    sorts: dict[str, Sort]
    array: Array
    sort_thread: Optional[SortThread]

    def __init__(self) -> None:
        self.load_sorts()
        self.create_widgets()
        self.graphics = GraphicsThread()
        self.array = Array(128)
        self.sort_thread = None

    def load_sorts(self) -> None:
        self.sorts = {}
        if os.path.exists(SORTS_DIR):
            for file in os.listdir(SORTS_DIR):
                file = os.path.join(SORTS_DIR, file)
                if os.path.isfile(file):
                    klass = load_sort_file(file, 'algoanim.sorts')
                    if klass is not None:
                        self.sorts[klass.name] = klass

    def create_widgets(self) -> None:
        self.root = tk.Tk()
        # Make the choose sort selection
        tk.Label(self.root, text='Choose Sort:').pack()
        self.choose_sort = ttk.Combobox(self.root, text='Choose Sort', values=list(self.sorts), state='readonly')
        self.choose_sort.bind('<<ComboboxSelected>>', self.choose_sort_click)
        self.choose_sort.pack()

    def choose_sort_click(self, event: tk.Event) -> None:
        if self.sort_thread is not None:
            return
        klass = self.sorts.get(self.choose_sort.get())
        self.choose_sort.set('')
        print('Sort selected:', klass)
        thread = SortThread(self, klass)
        thread.start()

    def check_closed(self) -> None:
        if hasattr(self.graphics, 'running') and not self.graphics.running:
            self.root.quit()
        self.root.after(500, self.check_closed)

    def main(self) -> None:
        self.graphics.start()
        self.root.after(500, self.check_closed)
        self.root.mainloop()
        self.graphics.running = False


def main():
    wind = MainWindow()
    wind.main()


if __name__ == '__main__':
    main()
