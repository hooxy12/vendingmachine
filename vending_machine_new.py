import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
from tkinter import simpledialog

class Beverage:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Customer:
    def __init__(self, budget):
        self.budget = budget

    def buy_beverage(self, vending_machine, choice):
        # customer choose the desired beverage
        # this is to check whether beverage is till available in vending machine
        beverage = vending_machine.get_beverage(choice) 

        if beverage is None:
            message = f"Sorry, {choice} is not available."
            return message

        if self.budget < beverage.price:
            message = f"Sorry, you don't have enough budget to buy {beverage.name}."
            return message
          
        self.budget -= beverage.price
        vending_machine.dispense_beverage(beverage)
        message = f"Dispensing your {beverage.name}, there you go.. enjoy!"
        return message

class VendingMachine:
  
    def __init__(self):
        self.beverages = [
            Beverage("Cola", 3.5, 10),
            Beverage("Tea", 4.0, 10),
            Beverage("Juice", 5.0, 10),
            Beverage("Coffee", 5.6, 10),
            Beverage("Water", 1.2, 10),
        ]
        self.total=0
    
    # def get_name(self):
    #     for i in range(len(self.beverages)):
    #         return self.beverages[i].name

    def get_available_beverages(self):
        available_beverages = []
        for b in self.beverages:
            if b.quantity > 0:
                available_beverages.append(b.name)
        return available_beverages

    def get_beverage(self, name):
        for beverage in self.beverages:
            if beverage.name.lower() == name.lower() and beverage.quantity > 0:
                return beverage
        return None

    def dispense_beverage(self, beverage):
        for i in range(len(self.beverages)):
            if self.beverages[i].name == beverage.name:
                self.beverages[i].quantity -= 1
                self.total += beverage.price
                break
 

class VendingMachineGUI:
    def __init__(self):
        # self.customer = Customer(10)
        self.vm = VendingMachine()
        self.secretpassword=123
        self.total=0
        # customer = Customer(random.uniform(1.2, 10.0))
        # print(f"{customer} approaches the vending machine.")
        
        self.root = tk.Tk()
        self.root.title("Vending Machine")
        
        #loading all available beverages
        self.loadingBeverages=self.vm.get_available_beverages()
        
        #label for beverage
        self.chooseBeverageLabel=tk.Label(self.root, text="Please choose the beverages from the dropdown: ")
        self.chooseBeverageLabel.grid(column=0, row=0, padx=10, pady=10)
        
        #creating dropdown menu
        self.bVar=tk.StringVar()
        self.dropdown =ttk.Combobox(self.root, textvariable=self.bVar, values=self.loadingBeverages, state="readonly")
        self.dropdown.grid(column=0, row=1, padx=10, pady=10)
        
        #creating pricing label
        self.pricingLabel= tk.Label(self.root, text="Beverage's price ")
        self.pricingLabel.grid(column=1, row=1, padx=10, pady=10)
              
        #creating checkout button
        self.checkoutButton = tk.Button(self.root, text="Checkout", command=self.checkout)
        self.checkoutButton.grid(column=1, row=0, padx=10, pady=10)
        
        #activate the pricing whenever select on beverage
        def beverage_selected(event):
            selected = self.bVar.get()
            if selected:
                bv = self.vm.get_beverage(selected)
                if bv:
                    self.pricingLabel.config(text="RM: " + str(bv.price))
                    self.total+=bv.price
                
        self.dropdown.bind("<<ComboboxSelected>>", beverage_selected)
        
        #creating money collection button
        self.collectButton=tk.Button(self.root, text="Collect", command=self.collection)
        self.collectButton.grid(column=1, row=3, padx=10, pady=10)
    
        self.root.mainloop()
        
        
    def checkout(self):
        customer=Customer(random.uniform(1.2,10.0))
        choice = self.bVar.get()
        m = customer.buy_beverage(self.vm, choice)
        messagebox.showinfo(title="Checkout", message=m)
        self.loadingBeverages = self.vm.get_available_beverages()
        self.dropdown.config(values=self.loadingBeverages)
        
    #creating collect function
    def collection(self):
        total=self.total
        passcode = simpledialog.askinteger("passcode: ","Only for staff")
        t=round(total,2)
        if passcode==self.secretpassword:
            messagebox.showinfo("Passed: ", "you have collected: "+str(t))
                  

if __name__ == "__main__":
    
    vm = VendingMachineGUI()

# v = VendingMachineGUI()
# v.checkout()