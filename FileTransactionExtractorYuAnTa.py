
"""
클래스는 파일에서 특정 키워드가 포함된 거래 내역을 파싱하여 추출하는 역할을 합니다. 
이 클래스는 주어진 파일 경로에서 파일을 읽고, 특정 키워드가 포함된 라인과 
그 다음 몇 개의 라인을 추출하여 transactions 리스트에 저장합니다.
"""
import re
from datetime import datetime  # datetime 모듈 임포트

class FileTransactionExtractorYuAnTa:
    
    def __init__(self):
        self.file_path = ""
        self.transactions = []
        self.parsed_transactions = []
        self.result_transactions = []
        self.company = ""
        self.broker = ""
        self.date_time_match = ""
        

    def set_file_path(self, file_path):
        self.file_path = file_path
        print(self.file_path)
    def set_company(self, company):
        self.company = company
    def get_company(self):
        return self.company
    def get_transactions(self):
        return self.transactions
    def get_result_transactions(self):
        return self.result_transactions

    def parse_transactions(self): # 이 클래스의 main 과 같은 함수. 이 함수를 통해 거래내역을 파싱하고 결과를 반환
        if(self.company == "키움증권"):
            self.parse_transactions_kiwoom()
        elif(self.company == "유안타증권"):
            self.parse_transactions_yooanta()
        else:
            print("No company")
            return
        for transaction in self.parsed_transactions:
            tp = self.transaction_to_tuple(transaction)
            # print(tp)
            
            
            # print('========MID' + mid_result)
            output_result = self.make_one_str_from_tuple(tp)
            if output_result is not None:
                self.result_transactions.append(output_result)
            
            
        return self.get_result_transactions()
        # self.parsed_transactions = self.make_one_str_from_tuple(self.transactions) # 여기를 거치면 원하는 형태의 transactions이 나옴
        
        #    print(transaction)

    def parse_transactions_kiwoom(self):
        keywords = ['매수', '매도', '---------------'] #, '[키움]체결통보']
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        lines_iter = iter(lines)
        for line in lines_iter:
            if any(keyword in line for keyword in keywords):
                if '---------------' in line:
                    self.transactions.append(line.strip())
                    for _ in range(4):
                        self.transactions.append(next(lines_iter).strip())
    
    def parse_transactions_yooanta(self): # 유안타증권 거래내역 파싱 parsed_transactions 에 append
        keywords = ['매수', '매도', '---------------']
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print(f"Error: The file at {self.file_path} was not found.")
            return
        except IOError:
            print(f"Error: An IOError occurred while reading the file at {self.file_path}.")
            return
        for line in lines:
            #if '유안타증권' in line and any(keyword in line for keyword in keywords):
            self.parsed_transactions.append(line.strip())

    def set_date_time_match(self, date_time_match):
        self.date_time_match = date_time_match

    def is_valid_date(self, date_str, format='%Y. %m. %d'):
        # date_str이 문자열인지 확인
        if not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    def get_transactions(self):
        return self.transactions

    def make_one_str_from_tuple(self, transaction):
        parsed_str = ""
        # print(transaction)
        if transaction and transaction[0].isdigit():
            return None
        if(transaction == None):
            return ""
        for i, item in enumerate(transaction):
            if i == 4:  # If it's the "매수" or "매도" part
                # if isinstance(item, tuple):
                #     print("===============================!!!!!")
                #     for sub_item in item:
                #         parsed_str += str(sub_item) + "\t"
                # else:
                #     parsed_str += str(item) + "\t"
                parsed_str += item + "\t" * 4
            elif i == 8:  # If it's the 체결수량 part
                parsed_str += str(item) + "\t" * 2
            else:
                parsed_str += str(item) + "\t"
        return parsed_str
            
    def transaction_to_tuple(self, transaction):
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
        """Parse a transaction and return a tuple of relevant details."""
        if "---------------" in transaction:
            if self.is_valid_date(self.parse_transaction_date(transaction)) == True:
                self.set_date_time_match(self.parse_transaction_date(transaction))
                return self.parse_transaction_date(transaction)
        elif " 매수 " in transaction:
            return self.parse_buy_transaction(transaction)
        elif "매도" in transaction:
            tmp = self.parse_sell_transaction(transaction)
            # print("매도!!!!!!")
            # print(tmp)
            return tmp
        else:
            return None

    def parse_kiwoom_transaction(self, transaction):
        lines = transaction.split('\n')
        # print(transaction)
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
        # price = int(re.sub(r'[^\d]', '', parts[-3]))  # Remove non-numeric characters and convert to int
        try:
            price_str = re.sub(r'[^\d]', '', parts[-3])  # 숫자가 아닌 문자 제거
            # print(transaction)
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
        # print("stock_name:", stock_name)
        # print("self.broker:", self.broker)
        # print("매도")
        # print("빈 문자열:", "")
        # print("self.date_time_match:", self.date_time_match)
        # print("price:", price)
        # print("quantity:", quantity)
        # print("빈 문자열:", "")
        # print("total_cost:", total_cost)

        return (stock_name, self.broker, "매도", "",self.date_time_match, price, quantity,"",total_cost)


