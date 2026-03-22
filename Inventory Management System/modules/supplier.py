from tkinter import*
from tkinter import ttk,messagebox
import databaseHandler

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ all variables --------------
        self.input_searchtxt=StringVar()
        self.input_sup_invoice=StringVar()
        self.input_name=StringVar()
        self.input_contact=StringVar()
        
        
        #---------- Search Frame -------------
        lbl_search=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)

        Entry(self.root,textvariable=self.input_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=850,y=80,width=160)
        Button(self.root,command=self.search_supplier,text="Search",font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=79,width=100,height=28)

        #-------------- title ---------------
        Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1000,height=40)

        #-------------- content ---------------
        #---------- row 1 ----------------
        Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=80)
        Entry(self.root,textvariable=self.input_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=180,y=80,width=180)
        
        #---------- row 2 ----------------
        Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=50,y=120)
        Entry(self.root,textvariable=self.input_name,font=("goudy old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #---------- row 3 ----------------
        Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=50,y=160)
        Entry(self.root,textvariable=self.input_contact,font=("goudy old style",15),bg="lightyellow").place(x=180,y=160,width=180)
        
        #---------- row 4 ----------------
        Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=470,height=120)
        
        #-------------- buttons -----------------
        Button(self.root,text="Save",command=self.add_supplier,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        Button(self.root,text="Update",command=self.update_supplier,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        Button(self.root,text="Delete",command=self.delete_supplier,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        Button(self.root,text="Clear",command=self.clear_inputfields,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)

        #------------ supplier details -------------
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)\
        
        self.SupplierTable=ttk.Treeview(sup_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        self.SupplierTable.heading("invoice",text="Invoice")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable.heading("desc",text="Description")
        self.SupplierTable["show"]="headings"
        self.SupplierTable.column("invoice",width=90)
        self.SupplierTable.column("name",width=100)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.column("desc",width=100)
        
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data_table)
        self.refresh_supplier_table()
#-----------------------------------------------------------------------------------------------------
    def add_supplier(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.input_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice no. is already assigned",parent=self.root)
                else:
                    cur.execute("insert into supplier(invoice,name,contact,desc) values(?,?,?,?)",(
                        self.input_sup_invoice.get(),
                        self.input_name.get(),
                        self.input_contact.get(),
                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                    self.clear_inputfields()
                    self.refresh_supplier_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def refresh_supplier_table(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children())
            for row in rows:
                self.SupplierTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data_table(self, _):
        f=self.SupplierTable.focus()
        content=(self.SupplierTable.item(f))
        row=content['values']
        self.input_sup_invoice.set(row[0])
        self.input_name.set(row[1])
        self.input_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])

    def update_supplier(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.input_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,desc=? where invoice=?",(
                        self.input_name.get(),
                        self.input_contact.get(),
                        self.txt_desc.get('1.0',END),
                        self.input_sup_invoice.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.refresh_supplier_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete_supplier(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.input_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from supplier where invoice=?",(self.input_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear_inputfields()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear_inputfields(self):
        self.input_sup_invoice.set("")
        self.input_name.set("")
        self.input_contact.set("")
        self.txt_desc.delete('1.0',END)
        self.input_searchtxt.set("")
        self.refresh_supplier_table()

    def search_supplier(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_searchtxt.get()=="":
                messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.input_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children())
                    self.SupplierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

def main():
    root=Tk()
    supplierClass(root)
    root.mainloop()
if __name__=="__main__":
    main()