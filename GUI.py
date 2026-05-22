
    ### DATALAYER###

#Importing
import tkinter as tk
import json


#Loading with try and except
try:        
    with open("gui_trade.json",'r') as file:
        data = json.load(file)
except (ValueError, FileNotFoundError):   
    data = []

#Variables(Global)
p_l = 0
total_p_l = 0

current_edit_index = None

    ###UI###

#Create windpw with Tkinter
window = tk.Tk()
window.geometry("500x500")
window.title("GUI Trade Journal")

#Creating frame
#FOR INPUT
input_frame = tk.Frame(window)
input_frame.pack(pady=5, side="top")

#FOR DISPLAY
display_frame = tk.Frame(window)
display_frame.pack(pady=5,side="top")

#FOR BUTTON
button_frame = tk.Frame(window)
button_frame.pack(pady=5,side="bottom")
#EDIT FRAME:
edit_frame = tk.Frame(window)
edit_frame.pack(side='bottom',pady=5)

#Delete Frame
delete_frame = tk.Frame(window)
delete_frame.pack(pady=3,side="bottom")



#Using Label & Entry field
qty_text = tk.Label(input_frame, text="Qty:")
qty_text.pack(side='top')


qty_entry = tk.Entry(input_frame,justify="center")
qty_entry.pack(side='top')

buy_price_text = tk.Label(input_frame,text="Buy price:")
buy_price_text.pack(side='top')

buy_entry = tk.Entry(input_frame,justify="center")
buy_entry.pack(side='top')

sell_price_text = tk.Label(input_frame,text="Sell price:")
sell_price_text.pack(side='top')

sell_entry = tk.Entry(input_frame,justify="center")
sell_entry.pack(side='top')



delete_text = tk.Label(delete_frame,text="Enter Trade Id to Delete: ")
delete_text.pack(side='left',padx=5)

delete_trade_input = tk.Entry(delete_frame,justify='left')
delete_trade_input.pack(side='left',padx=5)

#Label for showing in window always
p_l_label = tk.Label(display_frame,text =f"P/L:  {p_l}")
p_l_label.pack(pady=5)

#Using Text to display saved trades
trade_box =tk.Text(display_frame,height=10,width=50)
trade_box.pack(side='left')

#Using Scrollbar for display frame:

scroll_bar = tk.Scrollbar(display_frame)
scroll_bar.pack(side="right",fill=tk.Y)

trade_box.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=trade_box.yview)

edit_label = tk.Label(edit_frame,text='Enter Trade Id to Edit:')
edit_label.pack(side='left',padx=5)
edit_entry = tk.Entry(edit_frame)
edit_entry.pack(side='left',padx=5)



# #Startup display trade in text box:
# for index,trade in enumerate(data,start=1):
#             trade_box.insert(
#                  tk.END,f"T{index} - QTY:{trade['QTY']} BUY:{trade['BUY']} SELL:{trade['SELL']} P/L:{trade['P/L']}\n"
#                  )
            


#If data empty:
if not data:
        print("\nNo Data Saved")

#If present:     
for trade in data:
        total_p_l += trade['P/L']  #display Total P/L of all trades

#Label for display P/L        
total_p_l_label = tk.Label(text=f"Total P/L: {total_p_l}")
total_p_l_label.pack(side='top',pady=5)


### LOGIC ###

#Modify/Edit function:
def load_trade():
    try:
        index =  int(edit_entry.get()) - 1
        
        trade = data[index]

        qty_entry.delete(0, tk.END)
        buy_entry.delete(0, tk.END)
        sell_entry.delete(0, tk.END)
        edit_entry.delete(0,tk.END)


        qty_entry.insert(0,trade['QTY'])
        buy_entry.insert(0,trade['BUY'])
        sell_entry.insert(0,trade['SELL'])

        global current_edit_index
        current_edit_index = index

    except:
         p_l_label.config(text="Invalid Edit ID")

def update_trade():
     global current_edit_index 
     new_qty = int(qty_entry.get())
     new_buy = float(buy_entry.get())
     new_sell = float(sell_entry.get())
     
     new_p_l = ( new_sell - new_buy ) * new_qty

     updated_trade = {"QTY": new_qty,"BUY": new_buy,"SELL": new_sell,"P/L": new_p_l}

     data[current_edit_index] = updated_trade

     with open("gui_trade.json", "w") as file:
          json.dump(data, file)

     qty_entry.delete(0,tk.END)
     buy_entry.delete(0,tk.END)
     sell_entry.delete(0,tk.END)

     print(data)
     refresh()
     update_total()
    
   

update_button =tk.Button(edit_frame,text="Update",command=update_trade)
update_button.pack(side='left', padx=5,pady=5)

edit_button = tk.Button(edit_frame,text='Load',command=load_trade)
edit_button.pack(side='left',padx=5,pady=5)

#Delete function
def trade_id_delete():
    try:
        trade_id = int(delete_trade_input.get()) - 1

        del data[trade_id]

        with open("gui_trade.json",'w') as file:
            json.dump(data,file)

        delete_trade_input.delete(0,tk.END)

        refresh()
        update_total()

    except:
        p_l_label.config(text="Invalid Trade ID")
#Refresh function
def refresh():
     trade_box.delete("1.0", tk.END)

     for index, trade in enumerate(data, start=1):
        trade_box.insert(
            tk.END,
            f"T{index} - QTY:{trade['QTY']} BUY:{trade['BUY']} SELL:{trade['SELL']} P/L:{trade['P/L']}\n"
        )

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
   


# def modify():
     
     













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


###UI###

# Delete Button
delete_button = tk.Button(delete_frame,text="Delete",command=trade_id_delete)
delete_button.pack(pady=5 ,side='right')

#Submit button create and display
submit_button = tk.Button(input_frame,text="Submit",command=submit)
submit_button.pack(side='top',padx=20,pady=5)

#Calling main func:
refresh()
window.mainloop()

