
# """
# 클래스는 파일에서 특정 키워드가 포함된 거래 내역을 파싱하여 추출하는 역할을 합니다. 
# 이 클래스는 주어진 파일 경로에서 파일을 읽고, 특정 키워드가 포함된 라인과 
# 그 다음 몇 개의 라인을 추출하여 transactions 리스트에 저장합니다.
# """

import re
from datetime import datetime

class FileTransactionExtractorKiwoom:
    def __init__(self):
        self.transactions = []
        self.file_path = ""
        self.text = ""
        # self.parse_transactions()
    def set_file_path(self, file_path):
        self.file_path = file_path
        print(self.file_path)
    
    def parse_transactions(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            self.text = file.read()

        sections = re.split(r'--------------- (\d{4}년 \d{1,2}월 \d{1,2}일 \S+) ---------------', self.text)
        
        if len(sections) < 3:
            print("No valid sections found!")
            return
        
        for i in range(1, len(sections), 2):
            date_str = sections[i].strip()
            transactions_str = sections[i + 1].strip()
            
            date_str = re.sub(r' \S+$', '', date_str)
            
            try:
                date_obj = datetime.strptime(date_str, '%Y년 %m월 %d일')
                date_formatted = date_obj.strftime('%Y. %m. %d')
            except ValueError as e:
                print(f"Date parsing error for '{date_str}': {e}")
                continue
            
            transaction_matches = re.findall(
                r'\[키움증권 체결알림\] .*?\[키움\]체결통보\n(.*?)\n(매수|매도)(\d+)주\n평균단가([\d,]+)원', 
                transactions_str, 
                re.MULTILINE
            )
            
            for stock_name, action, quantity, price in transaction_matches:
                quantity = int(quantity)
                price = int(price.replace(',', ''))
                total_price = price * quantity
                
                tab_after_action = "\t" if action == "매수" else "\t\t"
                tab_after_date = "\t\t\t\t\t" if action == "매수" else "\t\t\t\t"
                
                formatted_transaction = f"{stock_name}\t키움증권\t{action}{tab_after_action}{date_formatted}{tab_after_date}{price}\t{quantity}\t\t{total_price}"
                self.transactions.append(formatted_transaction)
    
    def get_transactions(self):
        return self.transactions
