import tkinter as tk

class ResizableCanvas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')

        # Create a canvas widget
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize old width and height for resizing calculations
        self.canvas.old_width = self.canvas.winfo_reqwidth()
        self.canvas.old_height = self.canvas.winfo_reqheight()

        # Bind the resize event
        self.canvas.bind('<Configure>', self.resize_canvas)

        # Example items
        self.canvas.create_rectangle(50, 50, 200, 200, fill='blue')
        self.canvas.create_oval(100, 100, 300, 300, fill='red')

    def resize_canvas(self, event):
        # Calculate width and height scale
        w_scale = event.width / self.canvas.old_width
        h_scale = event.height / self.canvas.old_height

        # Resize all canvas items
        for item in self.canvas.find_all():
            coords = self.canvas.coords(item)
            # Assuming each item has four coordinates (like rectangles, ovals might need adjustment)
            new_coords = [coords[0] * w_scale, coords[1] * h_scale, coords[2] * w_scale, coords[3] * h_scale]
            self.canvas.coords(item, new_coords)

        # Update the canvas's old width and height for next resize event
        self.canvas.old_width = event.width
        self.canvas.old_height = event.height

if __name__ == '__main__':
    app = ResizableCanvas()
    app.mainloop()
