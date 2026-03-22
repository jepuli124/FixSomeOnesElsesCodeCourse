from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import databaseHandler
import directoryHandler

BASE_DIR = directoryHandler.base_path()
IMAGE_DIR = directoryHandler.image_path()
BILL_DIR = directoryHandler.bill_path()

class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()

        #------------ variables -------------
        self.input_cat_id=StringVar()
        self.input_name=StringVar()
        #--------------- title ---------------------
        Label(self.root,text="Manage Product Category",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="white").place(x=50,y=100)
        Entry(self.root,textvariable=self.input_name,bg="lightyellow",font=("goudy old style",18)).place(x=50,y=170,width=300)

        Button(self.root,text="ADD",command=self.add_category,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=360,y=170,width=150,height=30)
        Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=170,width=150,height=30)

        #------------ category details -------------
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)\
        
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cid",text="C ID")
        self.CategoryTable.heading("name",text="Name")
        self.CategoryTable["show"]="headings"
        self.CategoryTable.column("cid",width=90)
        self.CategoryTable.column("name",width=100)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data_inputfields)
        self.refresh_category_table()

        #----------------- images ---------------------
        self.im1=Image.open(IMAGE_DIR + "/cat.jpg")
        self.im1=self.im1.resize((500,250))
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)

        self.im2=Image.open(IMAGE_DIR + "/category.jpg")
        self.im2=self.im2.resize((500,250))
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED)
        self.lbl_im2.place(x=580,y=220)
#----------------------------------------------------------------------------------
    
    
    def add_category(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_name.get()=="":
                messagebox.showerror("Error","Category Name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.input_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Category already present",parent=self.root)
                else:
                    cur.execute("insert into category(name) values(?)",(
                        self.input_name.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.clear_inputfields()
                    self.refresh_category_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def refresh_category_table(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    
    def clear_inputfields(self):
        self.input_name.set("")
        self.refresh_category_table()

    def get_data_inputfields(self, _):
        f=self.CategoryTable.focus()
        content=(self.CategoryTable.item(f))
        row=content['values']
        self.input_cat_id.set(row[0])
        self.input_name.set(row[1])
    
    def delete(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            if self.input_cat_id.get()=="":
                messagebox.showerror("Error","Category name must be required",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.input_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Category Name",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from category where cid=?",(self.input_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)
                        self.clear_inputfields()
                        self.input_cat_id.set("")
                        self.input_name.set("")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")


def main():
    root=Tk()
    categoryClass(root)
    root.mainloop()

if __name__=="__main__":
    main()