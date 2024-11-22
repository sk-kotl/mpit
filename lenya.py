import tkinter as tk 
from tkinter import messagebox 
 
class PointApplication: 
    def __init__(self, master): 
        self.master = master 
        self.master.title("Создание точек") 
 
        self.points = [] 
        self.point_ids = [] 
 
        self.canvas = tk.Canvas(self.master, bg="white", width=400, height=400) 
        self.canvas.pack() 
 
        self.canvas.bind("<Button-1>", self.create_point) 
 
        self.show_points_button = tk.Button(self.master, text="Показать координаты", command=self.show_coordinates) 
        self.show_points_button.pack() 
 
    def create_point(self, event): 
        x, y = event.x, event.y 
 
        if len(self.points) >= 2: 
            self.canvas.delete(self.point_ids[0]) 
            self.points.pop(0) 
            self.point_ids.pop(0) 
 
        self.points.append((x, y)) 
        point_id = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black") 
        self.point_ids.append(point_id) 
 
    def show_coordinates(self): 
        if not self.points: 
            messagebox.showinfo("Координаты", "Нет созданных точек.") 
            return 
         
        coord_window = tk.Toplevel(self.master) 
        coord_window.title("Координаты точек") 
 
        coord_text = tk.Text(coord_window, width=40, height=10) 
        coord_text.pack() 
 
        for point in self.points: 
            coord_text.insert(tk.END, f"{point}\n") 

if __name__ == "__main__": 
    root = tk.Tk() 
    app = PointApplication(root) 
    root.mainloop()
