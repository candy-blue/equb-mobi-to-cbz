import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from equb_mobi_to_cbz.converter import ConvertError, convert_to_cbz


class App(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("EQUb/MOBI 转 CBZ")
    self.geometry("760x480")

    self.output_dir = tk.StringVar(value=str(Path.cwd()))
    self.status = tk.StringVar(value="就绪")
    self.is_working = False

    top = tk.Frame(self)
    top.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(top, text="输出目录:").pack(side=tk.LEFT)
    tk.Entry(top, textvariable=self.output_dir).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 6))
    tk.Button(top, text="选择", command=self.choose_output).pack(side=tk.LEFT)

    mid = tk.Frame(self)
    mid.pack(fill=tk.BOTH, expand=True, padx=10)

    self.listbox = tk.Listbox(mid, selectmode=tk.EXTENDED)
    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    right = tk.Frame(mid, width=160)
    right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

    tk.Button(right, text="添加文件", command=self.add_files).pack(fill=tk.X)
    tk.Button(right, text="移除所选", command=self.remove_selected).pack(fill=tk.X, pady=(8, 0))
    tk.Button(right, text="清空列表", command=self.clear_list).pack(fill=tk.X, pady=(8, 0))
    tk.Button(right, text="开始转换", command=self.start_convert).pack(fill=tk.X, pady=(18, 0))

    bottom = tk.Frame(self)
    bottom.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(bottom, textvariable=self.status).pack(side=tk.LEFT)

  def choose_output(self):
    path = filedialog.askdirectory()
    if path:
      self.output_dir.set(path)

  def add_files(self):
    paths = filedialog.askopenfilenames(filetypes=[("E-book", "*.equb *.epub *.mobi"), ("All", "*.*")])
    for p in paths:
      if p and p not in self.listbox.get(0, tk.END):
        self.listbox.insert(tk.END, p)

  def remove_selected(self):
    selected = list(self.listbox.curselection())
    selected.reverse()
    for idx in selected:
      self.listbox.delete(idx)

  def clear_list(self):
    self.listbox.delete(0, tk.END)

  def start_convert(self):
    if self.is_working:
      return
    files = list(self.listbox.get(0, tk.END))
    if not files:
      messagebox.showwarning("提示", "请先添加文件")
      return
    out_dir = Path(self.output_dir.get()).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    self.is_working = True
    self.status.set("转换中...")
    t = threading.Thread(target=self._convert_worker, args=(files, out_dir), daemon=True)
    t.start()

  def _convert_worker(self, files, out_dir: Path):
    ok = 0
    fail = 0
    last_error = ""
    for p in files:
      try:
        convert_to_cbz(Path(p), output_dir=out_dir)
        ok += 1
        self._set_status(f"已完成 {ok}/{len(files)}")
      except ConvertError as e:
        fail += 1
        last_error = str(e)
        self._set_status(f"失败 {fail} 个，已完成 {ok}/{len(files)}")
      except Exception as e:
        fail += 1
        last_error = str(e)
        self._set_status(f"失败 {fail} 个，已完成 {ok}/{len(files)}")

    def done():
      self.is_working = False
      if fail == 0:
        self.status.set(f"完成：{ok} 个文件")
        messagebox.showinfo("完成", f"已转换 {ok} 个文件")
      else:
        self.status.set(f"完成：成功 {ok}，失败 {fail}")
        messagebox.showwarning("完成", f"成功 {ok}，失败 {fail}\n{last_error}")

    self.after(0, done)

  def _set_status(self, text: str):
    self.after(0, lambda: self.status.set(text))


def run_gui():
  app = App()
  app.mainloop()
