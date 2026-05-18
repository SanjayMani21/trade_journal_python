from datetime import datetime
import json

# LOAD DATA
try:
    with open("trades.json", 'r') as file:
        data = json.load(file)

except FileNotFoundError:
    data = []


# SAVE JSON DATABASE
def save_json():
    with open("trades.json", "w") as file:
        json.dump(data, file)


# CHECK AND RESET IDS
def check():

    for index, trade in enumerate(data, start=1):

        if trade.get("Trade Id") != index:
            trade["Trade Id"] = index

    save_json()


# ENTER TRADE DETAILS
def enter_details():

    date = datetime.today()

    print("\nEnter Details of Trade:")

    try:
        qty = int(input("\nQuantity: "))
    except ValueError:
        print("\nInvalid Quantity")
        return

    try:
        buy_price = round(float(input("Buy Price: ")), 2)
    except ValueError:
        print("\nInvalid Buy Price")
        return

    try:
        sell_price = round(float(input("Sell Price: ")), 2)
    except ValueError:
        print("\nInvalid Sell Price")
        return

    trade_value = round(buy_price * qty, 2)

    p_l = round((sell_price - buy_price) * qty, 2)

    unsaved_data = {

        "Date": str(date.date()),
        "Time": str(date.strftime("%I:%M:%S %p")),
        "Quantity": qty,
        "Buy Price": buy_price,
        "Sell Price": sell_price,
        "P/L": p_l,
        "Trade Value": trade_value
    }

    print("\nCONFIRM YOUR DETAILS:\n")

    for key, value in unsaved_data.items():
        print(f"{key}: {value}")

    save_details(unsaved_data)


# SAVE DETAILS
def save_details(unsaved_data):

    print("\nSave Details - Y/N")
    user_input = input("You: ").lower()

    if user_input == 'y':

        if not data:
            new_id = 1

        else:
            new_id = max(trade.get("Trade Id", 0) for trade in data) + 1

        unsaved_data["Trade Id"] = new_id

        data.append(unsaved_data)

        save_json()

        print("\nSaved!")

    elif user_input == 'n':
        print("\nNot Saved!")

    else:
        print("\nInvalid Input")


# SHOW DETAILS
def show_details(data):

    print("\nSAVED DATA:\n")

    for trade in data:

        for key, value in trade.items():
            print(f"{key}: {value}")

        print()

    print(
        "OPTIONS:\n"
        "\n1 - Modify Data"
        "\n2 - Delete Data"
        "\n3 - Exit"
    )

    user_input = input("\nYou: ")

    if user_input == '1':
        modify()

    elif user_input == '2':
        delete()


# MODIFY FUNCTION
def modify():

    trade_id = input("Enter Trade-Id to Modify: ")

    if not trade_id.isdigit():
        print("\nInvalid Trade ID")
        return

    trade_id = int(trade_id)

    found = False

    for trade in data:

        if trade.get("Trade Id") == trade_id:

            found = True

            print("\nTrade Found:\n")

            for key, value in trade.items():
                print(f"{key}: {value}")

            confirm = input("\nConfirm Modify? (Y/N): ").lower()

            if confirm != 'y':
                print("\nModification Cancelled!")
                return

            keys = list(trade.keys())

            print()

            for option_index, key in enumerate(keys, start=1):
                print(f"{option_index} - {key}")

            opt_select = input("\nSelect Option: ")

            if not opt_select.isdigit():
                print("\nInvalid Option")
                return

            opt_select = int(opt_select) - 1

            if opt_select < 0 or opt_select >= len(keys):
                print("\nInvalid Option")
                return

            selected_option = keys[opt_select]

            if selected_option in (
                'Date',
                'Time',
                'P/L',
                'Trade Value',
                'Trade Id'
            ):

                print(f"\n{selected_option} cannot be modified!")
                return

            new_value = input(f"\nEnter new value for {selected_option}: ")

            try:

                if selected_option == "Quantity":
                    trade[selected_option] = int(new_value)

                elif selected_option in ("Buy Price", "Sell Price"):
                    trade[selected_option] = round(float(new_value), 2)

            except ValueError:
                print("\nInvalid Value")
                return

            # RECALCULATE VALUES
            trade['P/L'] = round(
                (trade["Sell Price"] - trade["Buy Price"]) * trade["Quantity"],
                2
            )

            trade['Trade Value'] = round(
                trade['Buy Price'] * trade["Quantity"],
                2
            )

            print("\nValue Modified Successfully!")

            save_json()

            return

    if not found:
        print("\nTrade Id not found")


# DELETE FUNCTION
def delete():

    trade_id = input("Enter Trade-Id to Delete: ")

    if not trade_id.isdigit():
        print("\nInvalid Trade ID")
        return

    trade_id = int(trade_id)

    found = False

    for trade in data:

        if trade.get("Trade Id") == trade_id:

            found = True

            print("\nTrade Found:\n")

            for key, value in trade.items():
                print(f"{key}: {value}")

            confirm = input("\nConfirm Delete? (Y/N): ").lower()

            if confirm == 'y':

                data.remove(trade)

                # RESET IDS
                for index, trade in enumerate(data, start=1):
                    trade["Trade Id"] = index

                save_json()

                print("\nDeleted Successfully!")

            else:
                print("\nDelete Cancelled!")

            return

    if not found:
        print("\nTrade Id not found")


# WIN RATE
def win_rate_calc():

    wins = 0
    loss = 0
    breakeven = 0

    for trade in data:

        value = trade["P/L"]

        if value > 0:
            wins += 1

        elif value < 0:
            loss += 1

        else:
            breakeven += 1

    print("\nWINS AND LOSSES:\n")

    print(f"WINS      : {wins}")
    print(f"LOSSES    : {loss}")
    print(f"BREAKEVEN : {breakeven}")

    if wins + loss == 0:
        print("\nNo Valid Trades")
        return

    win_rate = round((wins / (wins + loss)) * 100, 2)

    print(f"\nWin Rate : {win_rate}%")


# BEST TRADE
def best_trade():

    if not data:
        print("\nNo saved trades")
        return

    trade_id = None
    max_profit = 0

    for trade in data:

        if trade["P/L"] > max_profit:

            max_profit = trade["P/L"]
            trade_id = trade

    if trade_id is not None:

        print(
            "\n-----------------"
            "\nBEST TRADE"
            "\n-----------------\n"
        )

        for key, value in trade_id.items():
            print(f"{key}: {value}")

    else:
        print("\nNo profitable trades yet!")


# WORST TRADE
def worst_trade():

    if not data:
        print("\nNo saved trades")
        return

    trade_id = None
    min_profit = 0

    for trade in data:

        if trade["P/L"] < min_profit:

            min_profit = trade["P/L"]
            trade_id = trade

    if trade_id is not None:

        print(
            "\n-----------------"
            "\nWORST TRADE"
            "\n-----------------\n"
        )

        for key, value in trade_id.items():
            print(f"{key}: {value}")

    else:
        print("\nNo losing trades yet!")


# SEARCH TRADE
def search_trade():

    found = False

    trade_id = input("Enter Trade Id: ")

    if not trade_id.isdigit():
        print("\nInvalid Trade Id")
        return

    trade_id = int(trade_id)

    for trade in data:

        if trade["Trade Id"] == trade_id:

            found = True

            print("\nTRADE FOUND:\n")

            for key, value in trade.items():
                print(f"{key}: {value}")

            print()

            return

    if not found:
        print("\nTrade not found")


# TOTAL P/L
def total_profit():

    if not data:
        print("\nNo Data Saved")
        return

    total_p_l = 0

    for trade in data:
        total_p_l += trade['P/L']

    print(f"\nTotal Profit/Loss = Rs.{round(total_p_l, 2)}")


# MAIN MENU
def main_menu():

    print("\n------------------------------")
    print("       TRADE JOURNAL")
    print("------------------------------")

    print(
        "\n1 - ENTER TRADE DATA"
        "\n2 - SHOW SAVED DATA"
        "\n3 - TOTAL P/L"
        "\n4 - OTHERS"
        "\n5 - EXIT"
    )


# START PROGRAM
def start():

    while True:

        main_menu()

        user_input = input("\nYou: ")

        if user_input == '1':
            enter_details()

        elif user_input == '2':

            if not data:
                print("\nNO SAVED DATA\n")

            else:
                show_details(data)

        elif user_input == '3':
            total_profit()

        elif user_input == '4':

            print(
                "\nOTHER OPTIONS:"
                "\n\n1 - WIN RATE %"
                "\n2 - BEST TRADE"
                "\n3 - WORST TRADE"
                "\n4 - SEARCH TRADE BY ID"
            )

            option = input("\nYou: ")

            if option == '1':
                win_rate_calc()

            elif option == '2':
                best_trade()

            elif option == '3':
                worst_trade()

            elif option == '4':
                search_trade()

            else:
                print("\nInvalid Option")

        elif user_input == '5':

            print("\nByee!! See you later..!!\n")
            break

        else:
            print("\nInvalid Input")


# MAIN
def main():

    check()
    start()


main()