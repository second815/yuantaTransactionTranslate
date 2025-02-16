
import tkinter as tk
from tkinter import filedialog

from FileTransactionExtractorYuAnTa import FileTransactionExtractorYuAnTa  # Add this import statement
from FileTransactionExtractorKiwoom import FileTransactionExtractorKiwoom  # Add this import statement
# from TransactionParser import TransactionParser  # Add this import statement

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Converter")
        self.YuantaFileparser = FileTransactionExtractorYuAnTa()
        self.KiwoomFileparser = FileTransactionExtractorKiwoom()
        self.company = ""
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self.root, text="파일 선택", command=self.select_file)
        self.select_button.pack(pady=10)

        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)

        self.convert_button = tk.Button(self.root, text="변환", command=self.show_transactions)
        self.convert_button.pack(pady=5)

        self.result_text = tk.Text(self.root, width=200, height=30)
        self.result_text.pack(pady=10)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if "키움증권" in file_path:
            self.KiwoomFileparser.set_file_path(file_path)
            self.company = "키움증권"
            
        elif "유안타증권" in file_path:
            self.YuantaFileparser.set_file_path(file_path)
            self.YuantaFileparser.set_company("유안타증권")
            self.company = "유안타증권"
            
        if file_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)



    def show_transactions(self):
        if (self.company == "키움증권"):
            self.KiwoomFileparser.parse_transactions()
            for transaction in self.KiwoomFileparser.get_transactions():
                self.result_text.insert(tk.END, transaction + '\n')

            pass
        elif (self.company == "유안타증권"):
            self.YuantaFileparser.parse_transactions()
            transactions = self.YuantaFileparser.get_result_transactions()
            self.result_text.delete('1.0', tk.END)
            for each_transaction in transactions:
                # print(f"Transaction: {each_transaction}")  # 디버깅 출력을 추가하여 each_transaction의 값을 확인
                if each_transaction:  # each_transaction이 None 또는 빈 문자열이 아닌 경우에만 추가
                    self.result_text.insert(tk.END, each_transaction + '\n')
                else:
                    pass
                    #print("Empty or None transaction found")  # 디버깅 출력을 추가하여 빈 문자열 또는 None인 경우를 확인

    # def show_transactions(self):
    #     self.fileparser.parse_transactions()
    #     transactions = self.fileparser.get_result_transactions()
    #     self.result_text.delete('1.0', tk.END)
    #     for each_transaction in transactions:
    #         print(each_transaction)
    #         self.result_text.insert(tk.END, each_transaction + '\n')
    #     # self.result_text.insert(tk.END, tParser.make_one_str_from_transaction(parsedObj) + '\n')    