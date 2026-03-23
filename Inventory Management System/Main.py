from modules import billing, dashboard, create_db
from tkinter import *


class Menu():
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        Button(
        self.root, text="Dashboard", command=self.dashboard,
        font=("times new roman", 15, "bold"),
        bg="yellow", cursor="hand2"
        ).place(x=150, y=100, height=50, width=300)

        Button(
            self.root, text="Logout", command=self.logout,
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2"
        ).place(x=150, y=300, height=50, width=300)

        Button(
            self.root, text="billing", command=self.billing,
            font=("times new roman", 15, "bold"),
            bg="yellow", cursor="hand2"
        ).place(x=150, y=200, height=50, width=300)
    
    def dashboard(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = dashboard.IMS(self.new_win)

    def logout(self):
        exit(0)
    
    def billing(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = billing.billClass(self.new_win)
    

        
def setup():
    create_db.create_db()

def main():
    root = Tk()
    Menu(root)
    root.mainloop()
if __name__ == "__main__":
    setup()
    main()