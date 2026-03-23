from tkinter import*
from tkinter import ttk,messagebox
from . import databaseHandler


class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")

        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.input_searchby=StringVar()
        self.input_searchtxt=StringVar()
        self.input_emp_id=StringVar()
        self.input_gender=StringVar()
        self.input_contact=StringVar()
        self.input_name=StringVar()
        self.input_dob=StringVar()
        self.input_doj=StringVar()
        self.input_email=StringVar()
        self.input_pass=StringVar()
        self.input_utype=StringVar()
        self.input_salary=StringVar()

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.input_searchby,values=("Select","Email","Name","Contact"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        Entry(SearchFrame,textvariable=self.input_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        Button(SearchFrame,command=self.search_employee,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #-------------- title ---------------
        Label(self.root,text="Employee Details",font=("goudy old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1000)

        #-------------- content ---------------
        #---------- row 1 ----------------
        Label(self.root,text="Emp ID",font=("goudy old style",15),bg="white").place(x=50,y=150)
        Label(self.root,text="Gender",font=("goudy old style",15),bg="white").place(x=350,y=150)
        Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=750,y=150)

        Entry(self.root,textvariable=self.input_emp_id,font=("goudy old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.input_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=150,width=180)
        cmb_gender.current(0)
        Entry(self.root,textvariable=self.input_contact,font=("goudy old style",15),bg="lightyellow").place(x=850,y=150,width=180)

        #---------- row 2 ----------------
        Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=190)
        Label(self.root,text="D.O.B.",font=("goudy old style",15),bg="white").place(x=350,y=190)
        Label(self.root,text="D.O.J.",font=("goudy old style",15),bg="white").place(x=750,y=190)

        Entry(self.root,textvariable=self.input_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        Entry(self.root,textvariable=self.input_dob,font=("goudy old style",15),bg="lightyellow").place(x=500,y=190,width=180)
        Entry(self.root,textvariable=self.input_doj,font=("goudy old style",15),bg="lightyellow").place(x=850,y=190,width=180)

        #---------- row 3 ----------------
        Label(self.root,text="Email",font=("goudy old style",15),bg="white").place(x=50,y=230)
        Label(self.root,text="Password",font=("goudy old style",15),bg="white").place(x=350,y=230)
        Label(self.root,text="User Type",font=("goudy old style",15),bg="white").place(x=750,y=230)

        Entry(self.root,textvariable=self.input_email,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        Entry(self.root,textvariable=self.input_pass,font=("goudy old style",15),bg="lightyellow").place(x=500,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.input_utype,values=("Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=850,y=230,width=180)
        cmb_utype.current(0)
        
        #---------- row 4 ----------------
        Label(self.root,text="Address",font=("goudy old style",15),bg="white").place(x=50,y=270)
        Label(self.root,text="Salary",font=("goudy old style",15),bg="white").place(x=500,y=270)

        self.txt_address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=300,height=60)
        Entry(self.root,textvariable=self.input_salary,font=("goudy old style",15),bg="lightyellow").place(x=600,y=270,width=180)
        
        #-------------- buttons -----------------
        Button(self.root,text="Save",command=self.add_employee,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        Button(self.root,text="Update",command=self.update_employee,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        Button(self.root,text="Delete",command=self.delete_employee,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        Button(self.root,text="Clear",command=self.clear_inputfields,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)

        #------------ employee details -------------
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)\
        
        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","email","gender","contact","dob","doj","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid",text="EMP ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("email",text="Email")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("utype",text="User Type")
        self.EmployeeTable.heading("address",text="Address")
        self.EmployeeTable.heading("salary",text="Salary")
        self.EmployeeTable["show"]="headings"
        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("address",width=100)
        self.EmployeeTable.column("salary",width=100)
        
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data_table)
        self.refresh_employee_table()
#-----------------------------------------------------------------------------------------------------
    def add_employee(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.input_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is already assigned",parent=self.root)
                else:
                    cur.execute("insert into employee(eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.input_emp_id.get(),
                        self.input_name.get(),
                        self.input_email.get(),
                        self.input_gender.get(),
                        self.input_contact.get(),
                        self.input_dob.get(),
                        self.input_doj.get(),
                        self.input_pass.get(),
                        self.input_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.input_salary.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.clear_inputfields()
                    self.refresh_employee_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def refresh_employee_table(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data_table(self, _):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        self.input_emp_id.set(row[0])
        self.input_name.set(row[1])
        self.input_email.set(row[2])
        self.input_gender.set(row[3])
        self.input_contact.set(row[4])
        self.input_dob.set(row[5])
        self.input_doj.set(row[6])
        self.input_pass.set(row[7])
        self.input_utype.set(row[8])
        self.txt_address.delete('1.0',END)
        self.txt_address.insert(END,row[9])
        self.input_salary.set(row[10])

    def update_employee(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.input_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("update employee set name=?,email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",(
                        self.input_name.get(),
                        self.input_email.get(),
                        self.input_gender.get(),
                        self.input_contact.get(),
                        self.input_dob.get(),
                        self.input_doj.get(),
                        self.input_pass.get(),
                        self.input_utype.get(),
                        self.txt_address.get('1.0',END),
                        self.input_salary.get(),
                        self.input_emp_id.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Updated Successfully",parent=self.root)
                    self.refresh_employee_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete_employee(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_emp_id.get()=="":
                messagebox.showerror("Error","Employee ID must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.input_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.input_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear_inputfields()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear_inputfields(self):
        self.input_emp_id.set("")
        self.input_name.set("")
        self.input_email.set("")
        self.input_gender.set("Select")
        self.input_contact.set("")
        self.input_dob.set("")
        self.input_doj.set("")
        self.input_pass.set("")
        self.input_utype.set("Admin")
        self.txt_address.delete('1.0',END)
        self.input_salary.set("")
        self.input_searchby.set("Select")
        self.input_searchtxt.set("")
        self.refresh_employee_table()

    def search_employee(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.input_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from employee where "+self.input_searchby.get()+" LIKE '%"+self.input_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


def main():
    root=Tk()
    employeeClass(root)
    root.mainloop()
if __name__=="__main__":
    main()