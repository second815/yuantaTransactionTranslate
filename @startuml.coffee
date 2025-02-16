@startuml
actor User

User -> FileTransactionExtractor: parse_transactions()
activate FileTransactionExtractor

alt company == "키움증권"
    FileTransactionExtractor -> FileTransactionExtractor: parse_transactions_kiwoom()
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: transaction_to_tuple(transaction)
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: parse_transaction(transaction)
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: parse_transaction_date(transaction)
    deactivate FileTransactionExtractor
    deactivate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: make_one_str_from_tuple(tp)
    deactivate FileTransactionExtractor@
    deactivate FileTransactionExtractor 
else company == "유안타증권"
    FileTransactionExtractor -> FileTransactionExtractor: parse_transactions_yooanta()
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: transaction_to_tuple(transaction)
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: parse_transaction(transaction)
    activate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: parse_transaction_date(transaction)
    deactivate FileTransactionExtractor
    deactivate FileTransactionExtractor
    FileTransactionExtractor -> FileTransactionExtractor: make_one_str_from_tuple(tp)
    deactivate FileTransactionExtractor
    deactivate FileTransactionExtractor
else
    FileTransactionExtractor -> FileTransactionExtractor: print("No company")
    deactivate FileTransactionExtractor
end

FileTransactionExtractor -> FileTransactionExtractor: get_result_transactions()
deactivate FileTransactionExtractor

@enduml