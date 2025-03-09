import sys
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
import os

class DrawingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Dessin du pavage")
        self.geometry("800x600")

        self.canvas = tk.Canvas(self, bg="white", width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.X)

        self.save_button = tk.Button(self.button_frame, text="Sauvegarder", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.clear_button = tk.Button(self.button_frame, text="Effacer", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.image = Image.new("RGB", (800, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.old_x = None
        self.old_y = None

    def start_draw(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def draw_line(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, fill="black", width=2)
            self.draw.line([(self.old_x, self.old_y), (event.x, event.y)], fill="black", width=2)
        self.old_x = event.x
        self.old_y = event.y

    def end_draw(self, event):
        self.old_x = None
        self.old_y = None

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.image.save(file_path)
            os.system(f"xdg-open {file_path}" if sys.platform == "linux" else f"start {file_path}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (800, 500), "white")
        self.draw = ImageDraw.Draw(self.image)
