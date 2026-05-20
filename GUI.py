#Importing

import tkinter as tk
import json


#Loading with try and except
try:        
    with open("gui_trade.json",'r') as file:
        data = json.load(file)
except (ValueError, FileNotFoundError):   
    data = []

#Create windpw with Tkinter
window = tk.Tk()
window.geometry("500x400")
window.title("Test")

#Using Label
qty_text = tk.Label(window, text="Qty:")
qty_text.pack(pady=5)

#Using entry field
qty_entry = tk.Entry(window,justify="center")
qty_entry.pack(pady=5)

buy_price_text = tk.Label(window,text="Buy price:")
buy_price_text.pack()

buy_entry = tk.Entry(window,justify="center")
buy_entry.pack()

sell_price_text = tk.Label(window,text="Sell price:")
sell_price_text.pack()

sell_entry = tk.Entry(window,justify="center")
sell_entry.pack()


#Variables(Global)
p_l = 0

#Label for showing in window always
p_l_label = tk.Label(window,text =f"P/L:  {p_l}")
p_l_label.pack()


#Using Text to display saved trades
trade_box =tk.Text(window,height=10,width=50)
trade_box.pack()

#Startup display trade in text box:
for index,trade in enumerate(data,start=1):
            trade_box.insert(
                 tk.END,f"T{index} - QTY:{trade['QTY']} BUY:{trade['BUY']} SELL:{trade['SELL']} P/L:{trade['P/L']}\n"
                 )
            
#variable global
total_p_l = 0

#If data empty:
if not data:
        print("\nNo Data Saved")

#If present:     
for trade in data:
        total_p_l += trade['P/L']  #display Total P/L of all trades

#Label for display P/L        
total_p_l_label = tk.Label(window,text=f"Total P/L: {total_p_l}")
total_p_l_label.pack()

#Update function:
def update_total():
    #Totalling:
        total_p_l = 0
        for trade in data:
            total_p_l += trade["P/L"]
        total_p_l_label.config(text=f"Total P/L: {total_p_l}")
        
#displaybox function 
def display_trade(qty,buy,sell,p_l):  
    trade_box.insert(
         tk.END,
         f"T{len(data)} - QTY:{qty} BUY:{buy} SELL:{sell} P/L:{p_l}\n"
         )
   

#Submit function
def submit():

    try:
        #get all entry fields and store in variable
        qty = int(qty_entry.get())
        buy = float(buy_entry.get())
        sell = float(sell_entry.get())
        p_l = float((sell - buy)* qty)          #calculate p/l

        #conditions:
        
        if p_l > 0 :
            p_l_label.config(text=f"Profit: {p_l}")
        elif p_l < 0 :
            p_l_label.config(text=f"Loss: {p_l}")
        else:
            p_l_label.config(text=f"Breakeven: {p_l}")
            
        
        #Storing in a list as dictionary
        unsaved_data = {
            "QTY": qty,
            "BUY":buy,
            "SELL": sell,
            "P/L": p_l
        }

        #appending  to data global
        data.append(unsaved_data)


        #Saving to file json
        with open("gui_trade.json",'w') as file:
            json.dump(data,file)

        #Calling update func
        update_total()

        #Deleting the fields to set 0 after click submit:
        qty_entry.delete(0,tk.END)
        buy_entry.delete(0,tk.END)
        sell_entry.delete(0,tk.END)
        
        #Calling Display func
        display_trade(qty,buy,sell,p_l)  


        

    #except for handling value error in input
    except ValueError:


        p_l_label.config(text="Invalid Input")
    
 
    # print(qty)
    # print(buy)
    # print(sell)
    # print(p_l)

#Submit button create and display
submit_button = tk.Button(window,text="Submit",command=submit)
submit_button.pack()



#Calling main func:
window.mainloop()

