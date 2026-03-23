from tkinter import*
from tkinter import ttk,messagebox
from . import databaseHandler

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        #---------------------------------------
        #----------- variables -------------
        self.input_categories=StringVar()
        self.categories_list=[]
        self.suppliers_list=[]
        self.refresh_categories()
        self.refresh_suppliers()
        self.input_pid=StringVar()
        self.input_suppliers=StringVar()
        self.input_name=StringVar()
        self.input_price=StringVar()
        self.input_qty=StringVar()
        self.input_status=StringVar()
        self.input_searchby=StringVar()
        self.input_searchtxt=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #------------ title --------------
        Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)

        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.input_categories,values=self.categories_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.input_suppliers,values=self.suppliers_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        Entry(product_Frame,textvariable=self.input_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)
        Entry(product_Frame,textvariable=self.input_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=210,width=200)
        Entry(product_Frame,textvariable=self.input_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.input_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #-------------- buttons -----------------
        Button(product_Frame,text="Save",command=self.add_product,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        Button(product_Frame,text="Update",command=self.update_product,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        Button(product_Frame,text="Delete",command=self.delete_product,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        Button(product_Frame,text="Clear",command=self.clear_inputfields,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.input_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        Entry(SearchFrame,textvariable=self.input_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        Button(SearchFrame,text="Search",command=self.search_product,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #------------ product details -------------
        product_frame=Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(product_frame,orient=VERTICAL)
        scrollx=Scrollbar(product_frame,orient=HORIZONTAL)\
        
        self.ProductTable=ttk.Treeview(product_frame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="P ID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Suppler")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Quantity")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data_table)
        self.refresh_product_table()
        self.refresh_categories()
        self.refresh_suppliers()
#-----------------------------------------------------------------------------------------------------
    def refresh_categories(self):
        self.categories_list.append("Empty")
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select name from category")
            categories=cur.fetchall()
            if len(categories)>0:
                del self.categories_list[:]
                self.categories_list.append("Select")
                for i in categories:
                    self.categories_list.append(i[0])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
    
    def refresh_suppliers(self):
        self.suppliers_list.append("Empty")
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select name from supplier")
            suppliers=cur.fetchall()
            if len(suppliers)>0:
                del self.suppliers_list[:]
                self.suppliers_list.append("Select")
                for i in suppliers:
                    self.suppliers_list.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")
    
    
    def add_product(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_categories.get()=="Select" or self.input_categories.get()=="Empty" or self.input_suppliers=="Select" or self.input_suppliers=="Empty":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.input_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already present",parent=self.root)
                else:
                    cur.execute("insert into product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                        self.input_categories.get(),
                        self.input_suppliers.get(),
                        self.input_name.get(),
                        self.input_price.get(),
                        self.input_qty.get(),
                        self.input_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.clear_inputfields()
                    self.refresh_product_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def refresh_product_table(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data_table(self, _):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.input_pid.set(row[0])
        self.input_categories.set(row[1])
        self.input_suppliers.set(row[2])
        self.input_name.set(row[3])
        self.input_price.set(row[4])
        self.input_qty.set(row[5])
        self.input_status.set(row[6])

    def update_product(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.input_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.input_categories.get(),
                        self.input_suppliers.get(),
                        self.input_name.get(),
                        self.input_price.get(),
                        self.input_qty.get(),
                        self.input_status.get(),
                        self.input_pid.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.refresh_product_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def delete_product(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent=self.root)
            else:
                cur.execute("Select * from product where pid=?",(self.input_pid.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.input_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear_inputfields()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def clear_inputfields(self):
        self.input_categories.set("Select")
        self.input_suppliers.set("Select")
        self.input_name.set("")
        self.input_price.set("")
        self.input_qty.set("")
        self.input_status.set("Active")
        self.input_pid.set("")
        self.input_searchby.set("Select")
        self.input_searchtxt.set("")
        self.refresh_product_table()

    
    def search_product(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.input_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select * from product where "+self.input_searchby.get()+" LIKE '%"+self.input_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

def main():
    root=Tk()
    productClass(root)
    root.mainloop()
if __name__=="__main__":
    main()