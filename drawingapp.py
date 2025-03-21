import tkinter as tk
from tkinter import colorchooser

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Drawing App")

        # Canvas for drawing
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variables for drawing
        self.last_x, self.last_y = None, None
        self.color = "black"
        self.line_width = 2
        self.current_tool = "pencil"  # Current tool: pencil, eraser, rectangle, circle, square
        self.start_x, self.start_y = None, None  # For shape drawing

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Create a toolbar
        self.toolbar = tk.Frame(root, bg="lightgray")
        self.toolbar.pack(fill=tk.X)

        # Pencil button
        self.pencil_button = tk.Button(self.toolbar, text="Pencil", command=lambda: self.set_tool("pencil"))
        self.pencil_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Eraser button
        self.eraser_button = tk.Button(self.toolbar, text="Eraser", command=lambda: self.set_tool("eraser"))
        self.eraser_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Rectangle button
        self.rectangle_button = tk.Button(self.toolbar, text="Rectangle", command=lambda: self.set_tool("rectangle"))
        self.rectangle_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Circle button
        self.circle_button = tk.Button(self.toolbar, text="Circle", command=lambda: self.set_tool("circle"))
        self.circle_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Square button
        self.square_button = tk.Button(self.toolbar, text="Square", command=lambda: self.set_tool("square"))
        self.square_button.pack(side=tk.LEFT, padx=5, pady=5)

       

        # Color picker button
        self.color_button = tk.Button(self.toolbar, text="Choose Color", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Line width slider
        self.line_width_label = tk.Label(self.toolbar, text="Line Width:")
        self.line_width_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.line_width_slider = tk.Scale(self.toolbar, from_=1, to=10, orient=tk.HORIZONTAL, command=self.set_line_width)
        self.line_width_slider.set(self.line_width)
        self.line_width_slider.pack(side=tk.LEFT, padx=5, pady=5)

        # Clear button
        self.clear_button = tk.Button(self.toolbar, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def set_tool(self, tool):
        """Set the current tool."""
        self.current_tool = tool

    def start_draw(self, event):
        """Record the starting point of the drawing."""
        self.last_x, self.last_y = event.x, event.y
        if self.current_tool in ["rectangle", "circle", "square"]:
            self.start_x, self.start_y = event.x, event.y

    def draw(self, event):
        """Draw based on the current tool."""
        if self.current_tool == "pencil":
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    width=self.line_width, fill=self.color, capstyle=tk.ROUND, smooth=True
                )
            self.last_x, self.last_y = event.x, event.y
        elif self.current_tool == "eraser":
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    width=self.line_width, fill="white", capstyle=tk.ROUND, smooth=True
                )
            self.last_x, self.last_y = event.x, event.y
        elif self.current_tool in ["rectangle", "circle", "square" ]:
            # Delete the previous preview shape
            if hasattr(self, "preview_shape"):
                self.canvas.delete(self.preview_shape)
            # Draw a preview shape
            if self.current_tool == "rectangle":
                self.preview_shape = self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.color, width=self.line_width
                )
            elif self.current_tool == "circle":
                self.preview_shape = self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.color, width=self.line_width
                )
            elif self.current_tool == "square":
                size = max(abs(event.x - self.start_x), abs(event.y - self.start_y))
                self.preview_shape = self.canvas.create_rectangle(
                    self.start_x, self.start_y, self.start_x + size, self.start_y + size,
                    outline=self.color, width=self.line_width
                )
           
                

    def stop_draw(self, event):
        """Reset the last point when the mouse button is released."""
        if self.current_tool in ["rectangle", "circle", "square"]:
            if hasattr(self, "preview_shape"):
                self.canvas.delete(self.preview_shape)
            if self.current_tool == "rectangle":
                self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.color, width=self.line_width
                )
            elif self.current_tool == "circle":
                self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.color, width=self.line_width
                )
            elif self.current_tool == "square":
                size = max(abs(event.x - self.start_x), abs(event.y - self.start_y))
                self.canvas.create_rectangle(
                    self.start_x, self.start_y, self.start_x + size, self.start_y + size,
                    outline=self.color, width=self.line_width
                )
            

    def choose_color(self):
        """Open a color picker dialog and set the drawing color."""
        color = colorchooser.askcolor()[1]
        if color:
            self.color = color

    def set_line_width(self, value):
        """Set the line width based on the slider value."""
        self.line_width = int(value)

    def clear_canvas(self):
        """Clear the entire canvas."""
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()