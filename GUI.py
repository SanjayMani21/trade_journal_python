import tkinter as tk
import json



try:        
    with open("gui_trade.json",'r') as file:
        data = json.load(file)
except (ValueError, FileNotFoundError):   
    data = []


window = tk.Tk()



window.geometry("500x400")
window.title("Test")


qty_text = tk.Label(window, text="Qty:")

qty_text.pack(pady=5)


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


p_l = 0
p_l_label = tk.Label(window,text =f"P/L:  {p_l}")
p_l_label.pack()


trade_box =tk.Text(window,height=10,width=50)
trade_box.pack()
for index,trade in enumerate(data,start=1):
            trade_box.insert(
                 tk.END,f"T{index} - QTY:{trade['QTY']} BUY:{trade['BUY']} SELL:{trade['SELL']} P/L:{trade['P/L']}\n"
                 )


total_p_l = 0

if not data:
        print("\nNo Data Saved")
        
for trade in data:
        total_p_l += trade['P/L']
total_p_l_label = tk.Label(window,text=f"Total P/L: {total_p_l}")
total_p_l_label.pack()

def submit():

    try:
        qty = int(qty_entry.get())
        buy = float(buy_entry.get())
        sell = float(sell_entry.get())
        p_l = float((sell - buy)* qty)


        
        if p_l > 0 :
            p_l_label.config(text=f"Profit: {p_l}")
        elif p_l < 0 :
            p_l_label.config(text=f"Loss: {p_l}")
        else:
            p_l_label.config(text=f"Breakeven: {p_l}")
            return
        
        unsaved_data = {
            "QTY": qty,
            "BUY":buy,
            "SELL": sell,
            "P/L": p_l
        }


        data.append(unsaved_data)

        with open("gui_trade.json",'w') as file:
            json.dump(data,file)

        #Totalling:
        total_p_l = 0

        for trade in data:
            total_p_l += trade["P/L"]

        total_p_l_label.config(text=f"Total P/L: {total_p_l}")
            



        qty_entry.delete(0,tk.END)
        buy_entry.delete(0,tk.END)
        sell_entry.delete(0,tk.END)


        trade_box.insert(tk.END, f"QTY:{qty} BUY:{buy} SELL:{sell} P/L:{p_l}\n")

        


    except ValueError:


        p_l_label.config(text="Invalid Input")
    
 
    # print(qty)
    # print(buy)
    # print(sell)
    # print(p_l)


submit_button = tk.Button(window,text="Submit",command=submit)
submit_button.pack()




window.mainloop()

