from tkinter import*
from tkinter import ttk,messagebox
import time
import os
import tempfile
import databaseHandler
import directoryHandler

BASE_DIR = directoryHandler.base_path()
IMAGE_DIR = directoryHandler.image_path()
BILL_DIR = directoryHandler.bill_path()

class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False,False)
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0

        #------------- title --------------
        self.icon_title=PhotoImage(file=IMAGE_DIR + "/logo1.png")
        Label(self.root,text="Inventory Management System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #------------ logout button -----------
        Button(self.root,text="Logout",command=self.logout, font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #------------ clock -----------------
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD:MM:YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #-------------- product frame -----------------
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        self.var_search=StringVar()

        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        Button(ProductFrame2,text="Search",command=self.search_products,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        Button(ProductFrame2,text="Show All",command=self.refresh_product_table,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)\
        
        self.product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)
        self.product_Table.heading("pid",text="P ID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="Quantity")
        self.product_Table.heading("status",text="Status")
        self.product_Table["show"]="headings"
        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data_table)
        self.refresh_product_table()

        Label(ProductFrame1,text="Note: 'Enter 0 Quantity to remove product from the Cart'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #-------------- customer frame ---------------
        self.var_cname=StringVar()
        self.var_contact=StringVar()

        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)

        Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)
        
        Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",15),bg="lightyellow").place(x=380,y=35,width=140)
        Cal_Cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=420,y=190,width=530,height=360)

        #--------------- calculator frame ---------------------
        self.cal_input=StringVar()

        Cal_Frame=Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        self.txt_cal_input=Entry(Cal_Frame,textvariable=self.cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        self.txt_cal_input.grid(row=0,columnspan=4)

        Button(Cal_Frame,text=7,font=('arial',15,'bold'),command=lambda:self.get_input_cal(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        Button(Cal_Frame,text=8,font=('arial',15,'bold'),command=lambda:self.get_input_cal(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        Button(Cal_Frame,text=9,font=('arial',15,'bold'),command=lambda:self.get_input_cal(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        Button(Cal_Frame,text="+",font=('arial',15,'bold'),command=lambda:self.get_input_cal('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        Button(Cal_Frame,text=4,font=('arial',15,'bold'),command=lambda:self.get_input_cal(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        Button(Cal_Frame,text=5,font=('arial',15,'bold'),command=lambda:self.get_input_cal(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        Button(Cal_Frame,text=6,font=('arial',15,'bold'),command=lambda:self.get_input_cal(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        Button(Cal_Frame,text="-",font=('arial',15,'bold'),command=lambda:self.get_input_cal('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        Button(Cal_Frame,text=1,font=('arial',15,'bold'),command=lambda:self.get_input_cal(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        Button(Cal_Frame,text=2,font=('arial',15,'bold'),command=lambda:self.get_input_cal(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        Button(Cal_Frame,text=3,font=('arial',15,'bold'),command=lambda:self.get_input_cal(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        Button(Cal_Frame,text="*",font=('arial',15,'bold'),command=lambda:self.get_input_cal('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        Button(Cal_Frame,text=0,font=('arial',15,'bold'),command=lambda:self.get_input_cal(0),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        Button(Cal_Frame,text="C",font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        Button(Cal_Frame,text="=",font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        Button(Cal_Frame,text="/",font=('arial',15,'bold'),command=lambda:self.get_input_cal('/'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)

        #------------------ cart frame --------------------
        Cart_Frame=Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        Cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(Cart_Frame,text="Cart \t Total Products: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(Cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(Cart_Frame,orient=HORIZONTAL)\
        
        self.CartTable=ttk.Treeview(Cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=100)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=30)
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #-------------- add cart widgets frame ---------------
        self.input_pid=StringVar()
        self.input_pname=StringVar()
        self.input_price=StringVar()
        self.input_qty=StringVar()
        self.input_stock=StringVar()

        Add_CartWidgets_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgets_Frame.place(x=420,y=550,width=530,height=110)

        Label(Add_CartWidgets_Frame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        Entry(Add_CartWidgets_Frame,textvariable=self.input_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        Label(Add_CartWidgets_Frame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        Entry(Add_CartWidgets_Frame,textvariable=self.input_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        Label(Add_CartWidgets_Frame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        Entry(Add_CartWidgets_Frame,textvariable=self.input_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_inStock=Label(Add_CartWidgets_Frame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=70)

        Button(Add_CartWidgets_Frame,command=self.clear_cart,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        Button(Add_CartWidgets_Frame,command=self.add_update_cart,text="Add | Update",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)
        
        #------------------- billing area -------------------
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=400,height=410)

        Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #------------------- billing buttons -----------------------
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=400,height=140)

        self.lbl_amnt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)

        self.refresh_product_table()
        self.update_date_time()
#---------------------- all functions ------------------------------
    def logout(self):
        exit(0)

    def get_input_cal(self, input):
        calculation=self.cal_input.get()+str(input)
        self.cal_input.set(calculation)

    def clear_cal(self):
        self.cal_input.set('')

    def perform_cal(self):
        result=self.cal_input.get()
        self.cal_input.set(eval(result))

    def refresh_product_table(self):
        cur, con = databaseHandler.get_con_and_cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def search_products(self):
        cur, con=databaseHandler.get_con_and_cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found!!!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def get_data_table(self, _):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']
        self.input_pid.set(row[0])
        self.input_pname.set(row[1])
        self.input_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock [{str(row[3])}]")
        self.input_stock.set(row[3])
        self.input_qty.set('1')
    
    def get_data_cart(self, _):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        self.input_pid.set(row[0])
        self.input_pname.set(row[1])
        self.input_price.set(row[2])
        self.input_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock [{str(row[4])}]")
        self.input_stock.set(row[4])
        
    def add_update_cart(self):
        if self.input_pid.get()=="":
            messagebox.showerror("Error","Please select product from the list",parent=self.root)
        elif self.input_qty.get()=="":
            messagebox.showerror("Error","Quantity is required",parent=self.root)
        elif int(self.input_qty.get())>int(self.input_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            price_cal=self.input_price.get()
            cart_data=[self.input_pid.get(),self.input_pname.get(),price_cal,self.input_qty.get(),self.input_stock.get()]
            #---------- update cart --------------
            present="no"
            index_=0
            for row in self.cart_list:
                if self.input_pid.get()==row[0]:
                    present="yes"
                    break
                index_+=1
            if present=="yes":
                op=messagebox.askyesno("Confirm","Product already present\nDo you want to Update|Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.input_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal
                        self.cart_list[index_][3]=self.input_qty.get()
            else:
                self.cart_list.append(cart_data)
            self.refresh_cart()
            self.bill_update()

    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f"Bill Amnt\n{str(self.bill_amnt)}")
        self.lbl_net_pay.config(text=f"Net Pay\n{str(self.net_pay)}")
        self.cartTitle.config(text=f"Cart \t Total Products: [{str(len(self.cart_list))}]")

    def refresh_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}")

    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add product to the Cart!!!",parent=self.root)
        else:
            #--------- bill top -----------------
            self.bill_top()
            #--------- bill middle --------------
            self.bill_middle()
            #--------- bill bottom --------------
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been generated",parent=self.root)
            self.chk_print=1

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 9899459288 , Delhi-110053
{str("="*46)}
 Customer Name: {self.var_cname.get()}
 Ph. no. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
 Product Name\t\t\tQTY\tPrice
{str("="*46)}
'''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*46)}
 Bill Amount\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}\n
'''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def bill_middle(self):
        cur, con=databaseHandler.get_con_and_cursor()
        try:
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status="Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"
                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #------------- update qty in product table --------------
                cur.execute("update product set qty=?,status=? where pid=?",(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.refresh_product_table()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear_cart(self):
        self.input_pid.set("")
        self.input_pname.set("")
        self.input_price.set("")
        self.input_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.input_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.clear_cart()
        self.refresh_product_table()
        self.refresh_cart()
        self.var_cname.set("")
        self.var_contact.set("")
        self.chk_print=0
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Products: [0]")
        self.var_search.set("")
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showinfo("Print","Please generate bill to print the receipt",parent=self.root)

def main():
    root=Tk()
    billClass(root)
    root.mainloop()

if __name__=="__main__":
    main()