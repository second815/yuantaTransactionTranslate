import re
from datetime import datetime
from FileTransactionExtractorYuAnTa import FileTransactionExtractorYuAnTa
from FileTransactionExtractorKiwoom import FileTransactionExtractorKiwoom
from AppUI import AppUI
import tkinter as tk


def main():
    root = tk.Tk()
    test = False
    # if test:
    #     fe = FileTransactionExtractorYuAnTa()
    #     fe.set_file_path("/homes/nas/data/Programming/pythonProject/TransactionTraslateForGoogleSheet/KakaoTalk_20250203_2303_30_797_키움증권 체결알림.txt")
    #     fe.set_company("키움증권")
    #     fe.parse_transactions()
    if test:
        fe = FileTransactionExtractorKiwoom()
        fe.set_file_path("/homes/nas/data/Programming/pythonProject/TransactionTraslateForGoogleSheet/KakaoTalk_20250203_2303_30_797_키움증권 체결알림.txt")
        fe.parse_transactions()
    else:
        app_ui = AppUI(root)
        root.mainloop()
    #app_ui = AppUI(root)
    
    


if __name__ == "__main__":
    main()
