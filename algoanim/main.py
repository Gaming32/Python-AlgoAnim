from typing import Optional
from algoanim.array import Array
import os
import math
from algoanim.utils import SORTS_DIR, TITLE
from algoanim.sort import Sort, SortThread, load_sort_file
from threading import Thread
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from algoanim.graphics import GraphicsThread


class MainWindow:
    root: tk.Tk
    choose_sort: ttk.Combobox
    import_sort: ttk.Button
    cancel_delay: ttk.Button
    scales: tk.Frame
    length_scale: ttk.Scale
    speed_scale: ttk.Scale

    graphics: GraphicsThread
    sorts: dict[str, Sort]
    array: Array
    sort_thread: Optional[SortThread]
    file_dialog: filedialog.Open

    def __init__(self) -> None:
        self.load_sorts()
        self.create_widgets()
        self.array = Array(128)
        self.graphics = GraphicsThread(self.array)
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
        self.root.title(TITLE)
        self.file_dialog = filedialog.Open(self.root, initialdir=os.getcwd())
        # Make the choose sort selection
        tk.Label(self.root, text='Choose Sort:').pack()
        self.choose_sort = ttk.Combobox(self.root, text='Choose Sort', values=list(self.sorts), state='readonly')
        self.choose_sort.bind('<<ComboboxSelected>>', self.choose_sort_click)
        self.choose_sort.pack()
        # Import sort button
        self.import_sort = ttk.Button(self.root, text='Import sort', command=self.import_sort_click)
        self.import_sort.pack()
        # Cancel delay button
        self.cancel_delay = ttk.Button(self.root, text='Cancel delay', command=self.cancel_delay_click)
        self.cancel_delay.pack()
        ## Scales
        self.scales = tk.Frame()
        # Length scale
        self.length_scale = ttk.Scale(self.scales, command=self.length_scale_change, orient='vertical', to=1, from_=20, value=7)
        self.length_scale.pack(side=tk.LEFT)
        # Speed scale
        self.speed_scale = ttk.Scale(self.scales, command=self.speed_scale_change, orient='vertical', to=1, from_=20, value=9)
        self.speed_scale.pack(side=tk.LEFT)
        self.scales.pack()

    def choose_sort_click(self, event: tk.Event) -> None:
        if self.sort_thread is not None:
            return
        klass = self.sorts.get(self.choose_sort.get())
        self.choose_sort.set('')
        print('Sort selected:', klass)
        thread = SortThread(self, klass)
        thread.start()

    def import_sort_click(self) -> None:
        path = self.file_dialog.show(title=f'{TITLE} - Import Sort')
        if not path:
            return
        klass = load_sort_file(path, 'algoanim.sorts')
        if klass is not None:
            self.sorts[klass.name] = klass
            self.choose_sort.config(values=list(self.sorts))
            messagebox.showinfo(TITLE, f'Successfully loaded sort "{klass.name}"!')
        else:
            messagebox.showerror(TITLE, f'"{os.path.basename(path)}" is not a sort file!')

    def cancel_delay_click(self) -> None:
        self.array.delay = 0

    def length_scale_change(self, pow) -> None:
        if self.sort_thread is None:
            self.array.reset(int(2 ** float(pow)))

    def speed_scale_change(self, pow) -> None:
        self.array.set_delay_multiplier(int(2 ** float(pow)))

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
