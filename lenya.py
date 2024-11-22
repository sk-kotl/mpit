import tkinter as tk 
from tkinter import messagebox 
 
class PointApplication: 
    def __init__(self, master): 
        self.master = master 
        self.master.title("Создание точек") 
 
        # Список для хранения координат точек и идентификаторов нарисованных объектов 
        self.points = [] 
        self.point_ids = [] 
 
        # Создаем холст для рисования 
        self.canvas = tk.Canvas(self.master, bg="white", width=400, height=400) 
        self.canvas.pack() 
 
        # Связываем событие нажатия мыши с методом 
        self.canvas.bind("<Button-1>", self.create_point) 
 
        # Кнопка для открытия окна с координатами 
        self.show_points_button = tk.Button(self.master, text="Показать координаты", command=self.show_coordinates) 
        self.show_points_button.pack() 
 
    def create_point(self, event): 
        # Получаем координаты щелчка 
        x, y = event.x, event.y 
 
        # Если уже есть 2 точки, удаляем первую 
        if len(self.points) >= 2: 
            # Удаляем первую точку с холста 
            self.canvas.delete(self.point_ids[0]) 
            # Удаляем первую точку из списка 
            self.points.pop(0) 
            self.point_ids.pop(0) 
 
        # Добавляем точку в список 
        self.points.append((x, y)) 
        # Рисуем точку на холсте 
        point_id = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black") 
        self.point_ids.append(point_id) 
 
    def show_coordinates(self): 
        if not self.points: 
            messagebox.showinfo("Координаты", "Нет созданных точек.") 
            return 
         
        # Создаем новое окно для отображения координат 
        coord_window = tk.Toplevel(self.master) 
        coord_window.title("Координаты точек") 
 
        # Добавляем текстовое поле для вывода координат 
        coord_text = tk.Text(coord_window, width=40, height=10) 
        coord_text.pack() 
 
        # Добавляем координаты в текстовое поле 
        for point in self.points: 
            coord_text.insert(tk.END, f"{point}\n") 
 
# Запуск приложения 
if __name__ == "__main__": 
    root = tk.Tk() 
    app = PointApplication(root) 
    root.mainloop()
