import tkinter
import ttkbootstrap as tb
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (
                                    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import *
from functools import partial
from matplotlib import pyplot as plt


#window
root = tb.Window(themename= "solar")
root.title("N Body")

#Layout 
#General Frame
top_frame = tb.Frame(root)
bottom_frame = tb.Frame(root)

#general grid frame
top_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
bottom_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)


root.grid_columnconfigure(0, weight=1)

root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=2)

#Top Frame internal

canvas_frame = tb.Frame(top_frame)
treeview_frame = tb.Frame(top_frame)

canvas_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
treeview_frame.grid(row=0, column=1, sticky="nsew")

top_frame.grid_columnconfigure(0, weight=6)
top_frame.grid_columnconfigure(1, weight=2)
top_frame.grid_rowconfigure(0, weight=5)
top_frame.grid_rowconfigure(1, weight=0)

#Bot frame internal 
position_frame = tb.Frame(bottom_frame)
velocity_frame = tb.Frame(bottom_frame)
simulation_frame = tb.Frame(bottom_frame)

position_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
velocity_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
simulation_frame.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)


bottom_frame.grid_columnconfigure(0, weight=2)
bottom_frame.grid_columnconfigure(1, weight=2)
bottom_frame.grid_columnconfigure(2, weight=2)
bottom_frame.grid_rowconfigure(0, weight=5)



#N body simulator

#Global Constants

min = 0.00000001
dt = 0.01
G = 0.1

#Situational constants
steps = 60000


class Body():
  def __init__(self,mass,x_pos,y_pos,z_pos, V): # V is some 3dimentional velcity vector array = [Vx,Vy,Vz]
    self.mass = mass
    self.x = x_pos
    self.y = y_pos
    self.z = z_pos
    self.P = list([np.array([self.x,self.y,self.z], dtype = float)]) #position attribute a list of 3d arrays
    self.V = np.array(V,dtype = float) #velocity attribute
    self.a = np.array([0,0,0], dtype = float) #accleration attribute
    self.d = 0 #Attribute to store distance

  def accel(self,other,i):
    if self == other:
      return [0,0,0]
    else:
      distance = (pow((self.P[i][0] - other.P[i][0]),2) + pow((self.P[i][1] - other.P[i][1]),2) + pow((self.P[i][2] -other.P[i][2]),2))**(1/2)
      self.d = distance
      if distance < min:
        return [0,0,0]
      u_vectorx = (other.P[i][0] - self.P[i][0])
      u_vectory = (other.P[i][1] - self.P[i][1])
      u_vectorz = (other.P[i][2] - self.P[i][2])
      acceleration = (G * other.mass/pow(distance,3)) * np.array([u_vectorx,u_vectory,u_vectorz])
      return acceleration

  def update(self,i):
    self.V = (self.V + (dt*self.a))
    self.P.append(self.P[i] + (self.V*dt))

  def test(self):
    print(f"Position {self.P}")
    print(f"Velocity {self.V}")
    print(f"Accel {self.a}")

#N Body functions

def calculate(bodies,i):
  for body1 in bodies:
    body1.a = np.array([0,0,0], dtype = float)
    for body2 in bodies:
      a = np.array(body1.accel(body2,i))
      body1.a += a
    body1.update(i)

def simulate(bodies,steps):
  for i in range(0,steps):
    calculate(bodies,i)


#Functions


Bodies = []
scatter_list = []
def enter_point():
   
  

  global Bodies
  body = Body(int(mass_entry.get()),int(pos_entry_1.get()),int(pos_entry_2.get()),int(pos_entry_3.get()),
                                   [int(vel_entry_1.get()),int(vel_entry_2.get()),int(vel_entry_3.get())])
  Bodies.append(body)
  simulate_button.configure(state="enabled")

  my_tree.insert('', END, values=(len(Bodies),int(mass_entry.get()),(int(pos_entry_1.get()),int(pos_entry_2.get()),int(pos_entry_3.get())),
                                   (int(vel_entry_1.get()),int(vel_entry_2.get()),int(vel_entry_3.get()))))
  my_tree.pack(fill=BOTH )
  
   
  for body in Bodies:
    ax.scatter(body.P[0][0],body.P[0][1],body.P[0][2])
  canvas.draw()
  canvas.get_tk_widget().pack_forget()
  canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



# [[x value of each position],[y value of each position],[z value of each position]]
def disect(body):
  index = 0
  data = [[],[],[]]
  for component in data:
    for entry in body.P:
      component.append(entry[index])
    index += 1
  return data


def simulate_button():

  global Bodies

  canvas.get_tk_widget().pack_forget()

  simulate(Bodies,int(steps_entry.get()))
  for body in Bodies:
    data = disect(body)
    ax.plot3D(data[0], data[1], data[2])
    ax.scatter3D(data[0][-1], data[1][-1], data[2][-1])

  
  canvas.draw()
  canvas.get_tk_widget().pack_forget()
  canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def remove_placeholder(event):
    """Remove placeholder text, if present"""
    placeholder_text = getattr(event.widget, "placeholder", "")
    if placeholder_text and event.widget.get() == placeholder_text:
        event.widget.delete(0, "end")

def add_placeholder(event):
    """Add placeholder text if the widget is empty"""
    placeholder_text = getattr(event.widget, "placeholder", "")
    if placeholder_text and event.widget.get() == "":
        event.widget.insert(0, placeholder_text)

def init_placeholder(widget, placeholder_text):
    widget.placeholder = placeholder_text
    if widget.get() == "":
        widget.insert("end", placeholder_text)

    # set up a binding to remove placeholder text
    widget.bind("<FocusIn>", remove_placeholder)
    widget.bind("<FocusOut>", add_placeholder)


#Setting up intial canvas
fig = Figure(figsize=(5, 4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=canvas_frame)  # A tk.DrawingArea.
canvas.draw()

ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel('$X-coordinate$')
ax.set_ylabel('$Y-coordinate$')
ax.set_zlabel('$Z-coordinate$')

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

   

#Position entries


position_label = tb.Label(position_frame, text = "Position ", font = ("Helvetica",20), 
                    bootstyle = 'default')
position_label.pack(pady= 20)


pos_entry_1 = tb.Entry(master = position_frame, bootstyle="SUCCESS")
init_placeholder(pos_entry_1,"X position")
pos_entry_1.pack(padx=5, pady=5)

pos_entry_2 = tb.Entry(master = position_frame, bootstyle="SUCCESS")
init_placeholder(pos_entry_2,"Y position")
pos_entry_2.pack(padx=5, pady=5)

pos_entry_3 = tb.Entry(master = position_frame, bootstyle="SUCCESS")
init_placeholder(pos_entry_3,"Z position")
pos_entry_3.pack(padx=5, pady=5)

#Velocity entries


velocity_label = tb.Label(velocity_frame, text = "Velocity", font = ("Helvetica",20), 
                    bootstyle = 'default')
velocity_label.pack(pady= 20)

vel_entry_1 = tb.Entry(master = velocity_frame, bootstyle="SUCCESS")
init_placeholder(vel_entry_1,"X velocity")
vel_entry_1.pack(padx=5, pady=5)

vel_entry_2 = tb.Entry(master = velocity_frame, bootstyle="SUCCESS")
init_placeholder(vel_entry_2,"Y velocity")
vel_entry_2.pack(padx=5, pady=5)

vel_entry_3 = tb.Entry(master = velocity_frame, bootstyle="SUCCESS")
init_placeholder(vel_entry_3,"Z velocity")
vel_entry_3.pack(padx=5, pady=5)

#Simulation entry 


mass_entry = tb.Entry(master = simulation_frame, bootstyle="SUCCESS")
init_placeholder(mass_entry,"mass")
mass_entry.pack(padx=5, pady=5)


steps_entry = tb.Entry(master = simulation_frame, bootstyle="SUCCESS")
init_placeholder(steps_entry,"steps")
steps_entry.pack(padx=5, pady=5)


update_button = tb.Button(master = simulation_frame, text="Update", bootstyle="SUCCESS", command = enter_point)
update_button.pack(padx=5, pady=10)


simulate_button = tb.Button(master = simulation_frame, text="Simulate", bootstyle="SUCCESS", command= simulate_button, state="disabled")
simulate_button.pack(padx=5, pady=10)

#Treeview


columns = ("Name","Mass", "Position", "Velocity")

my_tree = tb.Treeview(master=treeview_frame,bootstyle = "success",columns= columns, show= 'headings')

my_tree.heading('Name',text = "Name")
my_tree.column("Name",anchor=CENTER, stretch=YES, width=60)

my_tree.heading('Mass',text = "Mass")
my_tree.column("Mass",anchor=CENTER, stretch=YES, width=60)

my_tree.heading('Position',text = "Position")
my_tree.column("Position",anchor=CENTER, stretch=YES, width=100)

my_tree.heading('Velocity',text = "Velocity")
my_tree.column("Velocity",anchor=CENTER)

my_tree.pack(expand=True,fill=BOTH )


tkinter.mainloop()