import tkinter, tkinter.font, time

class Task():
    def __init__(self,parent=None,taskLabel=None,row=None):
        self.parent = parent
        self.task = tkinter.Label(self.parent,text=taskLabel, fg='#1e5f74')
        self.timer = Timer(self.parent)
        self.taskLabel = taskLabel
        self.selected = False

        self.varControl = tkinter.Button(self.parent,text='||',bg="#850a07",fg="#150e1d",activebackground="#8f2220",font="bold",command=self.funControl)

        self.task.grid(row=row,column=0)
        self.timer.grid(row=row,column=1)
        self.varControl.grid(row=row,column=2)

    def funControl(self):
        if(self.timer.enable.get()):
            self.timer.enable.set(False)
            self.varControl.configure(text='>',bg="#898c40",fg="#150e1d",activebackground="#959853", font="bold")
            self.timer.configure(fg='#da0b4e')
        else:
            self.timer.enable.set(True)
            self.varControl.configure(text='||',bg="#850a07",fg="#150e1d",activebackground="#8f2220", font="bold")
            self.timer.configure(fg='#05884c')

class Timer(tkinter.Label):
    def __init__(self,parent=None):
        tkinter.Label.__init__(self, parent, fg='#05884c')
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.enable = tkinter.BooleanVar(parent,True)

        self.after(1000, self.tick)

    def tick(self):
        if self.enable.get():
            self.seconds +=1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes +=1
                if self.minutes == 60:
                    self.minutes = 0
                    self.hours +=1

            dSec = str(self.seconds)
            if self.seconds < 10:   
                dSec = '0'+str(self.seconds)
            dMin = str(self.minutes)
            if self.minutes < 10:   
                dMin = '0'+str(self.minutes)

            display = str(self.hours)+' : '+dMin+' : '+dSec
            self.configure(text=display)
        self.after(1000, self.tick)

class Clock(tkinter.Label):
    def __init__(self, parent=None, date=False):
        tkinter.Label.__init__(self, parent, font = ('Courier', 12, 'bold'), fg='#655044')
        self.date = date
        if self.date: self.ind = time.strftime('%A, %B %d')
        else:    self.ind = time.strftime('%H:%M:%S')

        self.display = self.ind
        self.configure(text=self.display)
        self.after(200, self.tick)


    def tick(self):
        if self.date: new_ind = time.strftime('%A, %B %d')
        else:    new_ind = time.strftime('%H:%M:%S')

        if new_ind != self.ind:
            self.ind = new_ind
            self.display = self.ind
            self.config(text=self.display)
        self.after(200, self.tick)

class App():
    def __init__(self,parent):
        self.parent = parent
        self.currLen = 0
        self.tasklist = []
        self.newTask = tkinter.Entry(self.parent)
        self.selectedTask = tkinter.StringVar(self.parent)
        self.selectedTask.trace('w',self.callback)

        self.taskMenu = tkinter.OptionMenu(self.parent,None,None)
        self.taskControl = tkinter.Button(self.parent,text="Add",bg="#bc641e",fg="#dbb694",font="bold",activebackground="#c37434",command=self.addTask)
        self.taskControl2 = tkinter.Button(self.parent,text="Del",bg="#bc641e",fg="#dbb694",font="bold",activebackground="#c37434",command=self.delTask)

        self.clockApplet = Clock(self.parent)
        self.calendarApplet = Clock(self.parent,True)

        self.newTask.grid(row=self.currLen,column=0,columnspan=2)
        self.taskControl.grid(row=self.currLen,column=2)
        self.taskMenu.grid(row=self.currLen+1,column=0,columnspan=2)
        self.taskControl2.grid(row=self.currLen+1,column=2)
        self.clockApplet.grid(row=self.currLen+2, columnspan=3)
        self.calendarApplet.grid(row=self.currLen+3, columnspan=3)

    def addTask(self,obj=None):
        cs = 1
        self.currLen+=1
        if obj:
            obj.parent = self.parent
            obj.row = self.currLen
            self.tasklist.append(obj)
        else:
            self.tasklist.append(Task(self.parent,self.newTask.get(),self.currLen))

        self.selectedTask.set('')
        self.taskMenu['menu'].delete(0,'end')
        for opt in self.tasklist:
            self.taskMenu['menu'].add_command(label=opt.taskLabel,command=tkinter._setit(self.selectedTask,opt.taskLabel+':'+str(self.tasklist.index(opt))))

        self.newTask.grid(row=self.currLen+1,column=0,columnspan=cs+1)
        self.taskControl.grid(row=self.currLen+1,column=cs+1)
        self.taskMenu.grid(row=self.currLen+2,column=0,columnspan=cs+1)
        self.taskControl2.grid(row=self.currLen+2,column=cs+1)
        self.clockApplet.grid(row=self.currLen+3, columnspan=cs+2)
        self.calendarApplet.grid(row=self.currLen+4, columnspan=cs+2)

    def delTask(self):
        delList = []
        for task in self.tasklist:
            if task.selected:
                delList.append(task)
        
        for task in delList:
            self.tasklist.remove(task)
            task.task.grid_forget()
            task.timer.grid_forget()
            task.varControl.grid_forget()

        self.selectedTask.set('')
        self.taskMenu['menu'].delete(0,'end')
        for opt in self.tasklist:
            self.taskMenu['menu'].add_command(label=opt.taskLabel,command=tkinter._setit(self.selectedTask,opt.taskLabel+':'+str(self.tasklist.index(opt))))



    def callback(self,*args):
        if self.selectedTask.get() != '':
            index = int(self.selectedTask.get().split(':')[1])
            if self.tasklist[index].selected:
                self.tasklist[index].task.configure(fg='#1e5f74',font = tkinter.font.Font(overstrike=int(false)))
                self.tasklist[index].selected = !(True)
            else:
                self.tasklist[index].task.configure(fg='#74331e',font = tkinter.font.Font(overstrike=int(true)))
                self.tasklist[index].selected = !(False)



if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("tusCU saati")
    app = App(root)
    root.attributes('-topmost', True)
    root.mainloop()
