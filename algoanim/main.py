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
from tkinter import simpledialog

from algoanim.graphics import GraphicsThread


class MainWindow:
    root: tk.Tk
    choose_sort: ttk.Combobox
    import_sort: ttk.Button
    cancel_delay: ttk.Button
    set_delay: ttk.Button
    show_stats: ttk.Checkbutton
    length_scale: ttk.Scale

    graphics: GraphicsThread
    sorts: dict[str, Sort]
    array: Array
    sort_thread: Optional[SortThread]
    file_dialog: filedialog.Open

    is_scale_changing: bool
    lock_to_pow2: bool
    delay_multiplier: float
    show_stats_var: tk.IntVar

    def __init__(self) -> None:
        self.load_sorts()
        self.create_widgets()
        self.array = Array(2048)
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
        self.choose_sort = ttk.Combobox(self.root, text='Choose Sort', values=sorted(self.sorts), state='readonly')
        self.choose_sort.bind('<<ComboboxSelected>>', self.choose_sort_click)
        self.choose_sort.pack()
        # Import sort button
        self.import_sort = ttk.Button(self.root, text='Import sort', command=self.import_sort_click)
        self.import_sort.pack()
        # Cancel delay button
        self.cancel_delay = ttk.Button(self.root, text='Cancel delay', command=self.cancel_delay_click)
        self.cancel_delay.pack()
        # Set delay button
        self.set_delay = ttk.Button(self.root, text='Change speed multiplier', command=self.set_delay_click)
        self.set_delay.pack()
        self.delay_multiplier = 1
        # Show stats checkbox
        self.show_stats_var = tk.IntVar(self.root, 1)
        self.show_stats = ttk.Checkbutton(self.root, text='Show stats', command=self.show_stats_click, variable=self.show_stats_var)
        self.show_stats.pack()
        # Length scale
        self.length_scale = ttk.Scale(self.root, command=self.length_scale_change, orient='vertical', to=1, from_=20, value=11, length=250)
        self.length_scale.bind('<Button-1>', (lambda ev: setattr(self, 'lock_to_pow2', False)))
        self.length_scale.bind('<Shift-Button-1>', (lambda ev: setattr(self, 'lock_to_pow2', True)))
        self.length_scale.pack()
        self.is_scale_changing = False
        self.lock_to_pow2 = False

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
            self.choose_sort.config(values=sorted(self.sorts))
            messagebox.showinfo(TITLE, f'Successfully loaded sort "{klass.name}"!')
        else:
            messagebox.showerror(TITLE, f'"{os.path.basename(path)}" is not a sort file!')

    def cancel_delay_click(self) -> None:
        self.array.set_delay_multiplier(0)

    def set_delay_click(self) -> None:
        new_delay = simpledialog.askfloat(TITLE, 'Enter a speed multiplier:', initialvalue=str(1 / self.delay_multiplier))
        if new_delay is not None:
            self.delay_multiplier = 1 / new_delay
            self.array.set_delay_multiplier(self.delay_multiplier)

    def show_stats_click(self) -> None:
        self.graphics.should_show_stats = bool(self.show_stats_var.get())

    def length_scale_change(self, pow) -> None:
        if self.is_scale_changing or self.sort_thread is not None:
            return
        self.is_scale_changing = True
        if self.sort_thread is None:
            pow = float(pow)
            if self.lock_to_pow2:
                pow = int(pow)
                self.length_scale.set(int(pow))
            self.array.reset(int(2 ** pow))
        self.is_scale_changing = False

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
