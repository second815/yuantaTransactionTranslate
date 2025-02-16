


import re
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Converter")

        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self.root, text="파일 선택", command=self.select_file)
        self.select_button.pack(pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        self.convert_button = tk.Button(self.root, text="변환", command=self.convert_transactions)
        self.convert_button.pack(pady=5)

        self.result_text = tk.Text(self.root, width=200, height=30)
        self.result_text.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)


    def convert_transactions(self):
        file_path = self.entry.get()
        if file_path:
            fileparser = FileTransactionParser(file_path)
            fileparser.parse_transactions_orDate()
            transactions = fileparser.get_transactions()
            tParser = TransactionParser()
            self.result_text.delete('1.0', tk.END)
            for each_transaction in transactions:
                parsedObj = tParser.add_transaction(each_transaction)
                if tParser.is_valid_date(parsedObj) == True:
                    #self.result_text.insert(tk.END, parsedObj + '\n')
                    pass
                else:
                    self.result_text.insert(tk.END, tParser.make_one_str_from_transaction(parsedObj) + '\n')
                pass


class FileTransactionParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.transactions = []

    def parse_transactions_orDate(self):
        keywords = ['매수', '매도', '---------------', '[키움]체결통보']
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            if any(keyword in line for keyword in keywords):
                self.transactions.append(line.strip())

    def get_transactions(self):
        return self.transactions

# class FileTransactionParser:
#     def __init__(self, file_path):
#         self.file_path = file_path
#         self.transactions = []
#
#     def parse_transactions_orDate(self):
#         keywords = ['매수', '매도','---------------']
#         with open(self.file_path, 'r', encoding='utf-8') as file:
#             lines = file.readlines()
#
#         for line in lines:
#             if any(keyword in line for keyword in keywords):
#                 if '체결' in line or '---------------' in line:
#                     self.transactions.append(line.strip())
#
#     def get_transactions(self):
#         return self.transactions


class TransactionParser:
    def __init__(self):
        self.transactions = []
        self.broker = ""
        self.date_time_match = ""


    def set_date_time_match(self, date_time_match):
        self.date_time_match = date_time_match

    def is_valid_date(self, date_str, format='%Y. %m. %d'):
        # date_str이 문자열인지 확인
        if not isinstance(date_str, str):
            print("Error: date_str must be a string.")
            return False
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    def get_transactions(self):
        return self.transactions

    def make_one_str_from_transaction(self, transaction):
        if(transaction == None):
            return ""
        output = ""
        for i, item in enumerate(transaction):
            if i == 4:  # If it's the "매수" or "매도" part
                output += item + "\t" * 4
            elif i == 8:  # If it's the 체결수량 part
                output += str(item) + "\t" * 2
            else:
                output += str(item) + "\t"
        return output
    def add_transaction(self, transaction):
        """Add a transaction to the parser."""
        parsed_transaction = self.parse_transaction(transaction)
        if parsed_transaction:
            self.transactions.append(parsed_transaction)
        return parsed_transaction
    # def parse_transaction(self, transaction):
    #     """Parse a transaction and return a tuple of relevant details."""
    #     if "---------------" in transaction:
    #         if self.is_valid_date(self.parse_transaction_date(transaction)) == True:
    #             self.set_date_time_match(self.parse_transaction_date(transaction))
    #             return self.parse_transaction_date(transaction)
    #     elif "매수" in transaction:
    #         return self.parse_buy_transaction(transaction)
    #     elif "매도" in transaction:
    #         return self.parse_sell_transaction(transaction)
    #
    #     else:
    #         return None
    def parse_transaction(self, transaction):
        if "---------------" in transaction:
            if self.is_valid_date(self.parse_transaction_date(transaction)):
                self.set_date_time_match(self.parse_transaction_date(transaction))
                return self.parse_transaction_date(transaction)
        elif "[키움]체결통보" in transaction:
            return self.parse_kiwoom_transaction(transaction)
        elif " 매수 " in transaction:
            return self.parse_buy_transaction(transaction)
        elif "매도" in transaction:
            print(transaction)
            return self.parse_sell_transaction(transaction)
        else:
            return None

    def parse_kiwoom_transaction(self, transaction):
        lines = transaction.split('\n')
        print(transaction)
        stock_name = lines[1].strip()
        transaction_type = "매수" if "매수" in lines[2] else "매도"
        quantity = int(lines[2].split('주')[0].split(transaction_type)[1])
        price = int(lines[3].split('원')[0].split('단가')[1].replace(',', ''))
        total_cost = price * quantity

        self.broker = "키움증권"

        return (stock_name, self.broker, transaction_type, self.date_time_match, "", price, quantity, "", total_cost)
    def parse_transaction_date(self, date_str):
        # 정규 표현식을 사용하여 날짜를 추출합니다.
        match = re.search(r'\d{4}년 \d{1,2}월 \d{1,2}일', date_str)

        if match:
            # 추출한 날짜를 datetime 객체로 변환합니다.
            date = datetime.strptime(match.group(), '%Y년 %m월 %d일')
            # 새로운 형식의 문자열을 반환합니다.
            return date.strftime('%Y. %m. %d')
        else:
            return None
    def parse_buy_transaction(self, transaction):
        """Parse a 'buy' transaction."""
        parts = transaction.split()
        if "62**-**46-015*" in transaction:
            self.broker = "유안타증권(스윙)"
        elif "62**-**46-012*" in transaction:
            self.broker = "유안타증권(단타)"
        elif "62**-**46-018*" in transaction:
            self.broker = "유안타증권(중장기)"
        elif "62**-**46-019*" in transaction:
            self.broker = "유안타증권(모아가는)"

        print("===========" + transaction)
        stock_name = parts[-4]
        price_str = re.sub(r'[^\d]', '', parts[-3])  # Remove non-numeric characters
        price = int(price_str) if price_str else None  # Convert to int if not empty

        # Check if quantity string is empty before conversion
        quantity_str = re.sub(r'[^\d]', '', parts[-2])
        quantity = int(quantity_str) if quantity_str else None

        total_cost = price * quantity if quantity is not None else None

        return (stock_name, self.broker, "매수",self.date_time_match,"", price, quantity,"", total_cost)

    def parse_sell_transaction(self, transaction):
        """Parse a 'sell' transaction."""
        parts = transaction.split()

        stock_name = parts[-4]
        print(stock_name)
        # price = int(re.sub(r'[^\d]', '', parts[-3]))  # Remove non-numeric characters and convert to int
        try:
            price_str = re.sub(r'[^\d]', '', parts[-3])  # 숫자가 아닌 문자 제거
            if not price_str:  # 빈 문자열이면 예외 발생
                raise ValueError("가격 데이터가 숫자가 아닙니다.")

            price = int(price_str)  # 정수 변환
        except ValueError as e:
            print(f"오류: {e}")  # 오류 메시지 출력
            return
            # sys.exit(1)  # 프로그램 종료

        # Check if quantity string is empty before conversion
        quantity_str = re.sub(r'[^\d]', '', parts[-2])
        quantity = int(quantity_str) if quantity_str else None

        total_cost = price * quantity if quantity is not None else None

        # Check if realized profit string is empty before conversion
        realized_profit_str = re.sub(r'[^\d]', '', parts[-4])
        realized_profit = int(realized_profit_str) if realized_profit_str else None

        return (stock_name, self.broker, "매도", "",self.date_time_match, price, quantity,"",total_cost)


def main():
    root = tk.Tk()
    app_ui = AppUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
