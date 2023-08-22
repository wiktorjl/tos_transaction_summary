
point_values = {
    "/ESU23": 50,
    "/MESU23": 5,
}

class Trans:
    
    def __init__(self, raw_input):
        self.trans_date = raw_input[0]
        self.trans_time = raw_input[1]
        self.direction = raw_input[2]
        self.qtt = int(raw_input[3])
        self.intent = raw_input[4]
        self.symbol = raw_input[5]
        self.price = float(raw_input[9])

    
    def __str__(self) -> str:
        return self.symbol + " " + self.direction + " " + str(self.qtt) + " @ " + str(self.price)


class Account:

    def __init__(self, symbol):
        self.transactions = []
        self.qtt = 0
        self.prices = []
        self.qtts = []
        self.symbol = symbol


    def add_transaction(self, t):
        if t.symbol == self.symbol:
            self.transactions.append(t)


    def calculate_pnl_from_prices_and_qtts(self, prices, qtts):
        pnl = 0
        for i in range(len(prices)):
            pnl += prices[i] * qtts[i]
        return pnl


    def summarize_positions(self):
        q = 0
        a = 0

        for i in range(len(self.qtts)):
            q += self.qtts[i]            

            if self.qtts[i] > 0:
                a -= self.qtts[i] * self.prices[i]
            elif self.qtts[i] < 0:
                a += abs(self.qtts[i]) * self.prices[i]                

        return q, a
    

    def calculate_pnl(self):
        for t in self.transactions:
            self.prices.append(t.price)
            self.qtts.append(t.qtt)

            if t.direction == 'BUY':
                pass
            elif t.direction == 'SELL':
                pass
            else:
                print("ERROR: unknown direction")
                return -1

        self.transactions = []
        return "X"    


def extract_lines_between_strings(file_path, start_string, end_string):
    lines = []
    inside_range = False

    with open(file_path, 'r') as file:
        for line in file:
            if start_string in line:
                inside_range = True
                # lines.append(line.strip())
            elif end_string in line:
                inside_range = False
                # lines.append(line.strip())
                break
            elif inside_range:
                l = line.strip()
                if len(l) > 0:
                    lines.append(l)

    return reversed([l.split(",")[1:] for l in lines[1:]])

file_path = "today.csv"
start_string = 'Account Trade History'
end_string = 'Equities'

extracted_lines = list(extract_lines_between_strings(file_path, start_string, end_string))

u = list(set([s[5] for s in extracted_lines]))
print(f"Available symbols: {u}")


for symbol in u:
    if symbol in point_values:
        a = Account(symbol)
        qtt, amount = None, None
        for line in extracted_lines:
            s = Trans(line)
            # print(s)
            a.add_transaction(s)
            a.calculate_pnl()
            qtt, amount = a.summarize_positions()


        print(f"{symbol} | Size: {qtt}, Amount: {amount * point_values[symbol]}")


