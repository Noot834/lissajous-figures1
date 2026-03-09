import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


#вращение
ROTATION_SPEED = 0.02  # плавность
UPDATE_INTERVAL = 50    #скорость

class LissajousApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()

        #график
        self.window_plot = tk.Toplevel(self.root)
        self.window_plot.title(" Лиссажу")
        self.window_plot.geometry("600x600")
        self.window_plot.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Управление
        self.window_ctrl = tk.Toplevel(self.root)
        self.window_ctrl.title("настройки")
        self.window_ctrl.geometry("400x350")
        self.window_ctrl.resizable(True, True)
        self.window_ctrl.protocol("WM_DELETE_WINDOW", self.on_closing)

        # наполнение настроек
        self.var_fx = tk.DoubleVar(value=3.0)
        self.var_fy = tk.DoubleVar(value=2.0)
        self.var_phase = tk.DoubleVar(value=np.pi/4)
        self.var_amp = tk.DoubleVar(value=1.0)
        self.var_rotation = tk.BooleanVar(value=True) #вращение

        # Дополнительная фаза для анимации вращения
        self.extra_phase = 0.0

        #интерфейс
        self.create_plot_window()
        self.create_control_window()

        self.animate() #запуск с анимацией(лагает)

        self.root.mainloop()

    def create_plot_window(self):
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        # Начальные значения
        t = np.linspace(0, 2*np.pi, 5000)
        x = np.sin(3 * t)
        y = np.sin(2 * t + np.pi/4)
        self.line, = self.ax.plot(x, y, 'b-', lw=2)
        self.ax.set_title('Лиссажу: 3.0:2.0, фаза=0.79')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window_plot)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def create_control_window(self):
        # слайдеры
        ttk.Label(self.window_ctrl, text="Амплитуда колебаний вдоль X:").pack(pady=(10,0))
        self.slider_fx = ttk.Scale(self.window_ctrl, from_=1, to=10, orient=tk.HORIZONTAL,
                                   variable=self.var_fx, command=self.on_slider_change)
        self.slider_fx.pack(fill=tk.X, padx=20)


        ttk.Label(self.window_ctrl, text="Амплитуда колебаний вдоль Y:").pack(pady=(10,0))
        self.slider_fy = ttk.Scale(self.window_ctrl, from_=1, to=10, orient=tk.HORIZONTAL,
                                   variable=self.var_fy, command=self.on_slider_change)
        self.slider_fy.pack(fill=tk.X, padx=20)


        ttk.Label(self.window_ctrl, text="Разность фаз:").pack(pady=(10,0))
        self.slider_phase = ttk.Scale(self.window_ctrl, from_=0, to=2*np.pi, orient=tk.HORIZONTAL,
                                      variable=self.var_phase, command=self.on_slider_change)
        self.slider_phase.pack(fill=tk.X, padx=20)


        ttk.Label(self.window_ctrl, text="Масштаб:").pack(pady=(10,0))
        self.slider_amp = ttk.Scale(self.window_ctrl, from_=0.1, to=2.0, orient=tk.HORIZONTAL,
                                    variable=self.var_amp, command=self.on_slider_change)
        self.slider_amp.pack(fill=tk.X, padx=20)


        # вращение
        self.cb_rotation = ttk.Checkbutton(self.window_ctrl, text="Вращение (имитация осциллографа)",
                                           variable=self.var_rotation)
        self.cb_rotation.pack(pady=10)




    def on_slider_change(self, event=None): #изменение ползунков

        self.extra_phase = 0.0
        self.update_plot()

    def update_plot(self):
        fx = self.var_fx.get()
        fy = self.var_fy.get()
        base_phase = self.var_phase.get()
        amp = self.var_amp.get()

        total_phase = base_phase + self.extra_phase

        t = np.linspace(0, 2 * np.pi, 5000)
        x = amp * np.sin(fx * t)
        y = amp * np.sin(fy * t + total_phase)

        self.line.set_data(x, y)
        self.ax.set_title(f'Х: {fx:.1f},Y:{fy:.1f}, фаза={total_phase:.2f}')
        self.canvas.draw_idle()

    def animate(self):
        if self.var_rotation.get():
            self.extra_phase += ROTATION_SPEED
            self.extra_phase %= (2 * np.pi)
        self.update_plot()

        self.window_plot.after(UPDATE_INTERVAL, self.animate)


    def reset_values(self):
        self.var_fx.set(3.0)
        self.var_fy.set(2.0)
        self.var_phase.set(np.pi/4)
        self.var_amp.set(1.0)
        self.extra_phase = 0.0
        self.update_plot()

    def on_closing(self):#закрытие программы
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    app = LissajousApp()
