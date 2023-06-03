import sys
from collections import defaultdict
import time
import message
from order_book import OrderBook

def main():

    if len(sys.argv) != 3:
        print(f"Invalid Arguments Provided.")
        sys.exit(1)

    input_file = sys.argv[1]
    N = int(sys.argv[2])
    OrderBook.set_depth(N)
    
    # Initializes dictionary which stores each symbol as a key and its orderbook as value
    order_books = defaultdict(OrderBook)
    
    with open(input_file, 'rb') as f:

        for header, order in message.gen_from(f):
            
            order_book = order_books[order.symbol]
            
            if header.msg_type == "A":
                order_book.order_added(order)
            elif header.msg_type == "U":
                order_book.order_updated(order)
            elif header.msg_type == "D":
                order_book.order_deleted(order)
            elif header.msg_type == "E":
                order_book.order_traded(order)

            snapshot = order_book.check_snapshot()
            if snapshot != []:
                print(f"{header.seq_num}, {order.symbol}, {snapshot[0]}, {snapshot[1]}")
            


if __name__ == "__main__":
    main()
