from collections import defaultdict
import bisect


class OrderSide:
    """ Stores constant characters """
    BID='B'
    ASK='S'


class MaxHeap:
    """ Data Structure to store and sort all the prices of Bids and asks for a symbol """
    def __init__(self, depth):
        """
        depth stores the price depth level.
        data stores the sorted list of prices
        prices is a set of prices used for quickly checking if a price has been added or not.
        
        """
        self.depth = depth
        self.data = []
        self.prices = set()

    def push(self, value):
        """ Checks if price doesn't exist by looking it up in the set then pushes price """
        if value not in self.prices:
            bisect.insort_left(self.data, value)
            self.prices.add(value)
            
    def remove(self, value):
        """ Finds index of price then removes it """
        index = bisect.bisect_left(self.data, value)
        if index != len(self.data) and self.data[index] == value:
            del self.data[index]
            self.prices.remove(value)
    
    def get_asks(self):
        """ returns the lowest ask prices based on the depth """
        if len(self.data) > self.depth:
            return self.data[:self.depth]
        return self.data
    
    def get_bids(self):
        """ returns the highest bids based on the depth """
        if len(self.data) > self.depth:
            return list(reversed(self.data[-self.depth:]))
        return list(reversed(self.data))



class OrderBook:
    """ Stores all the price volumes and orders for a particular symbol and calculates snapshots """
    
    price_depth = 0
    
    @staticmethod
    def set_depth(n):
        """ sets depth """
        OrderBook.price_depth = n
    
    def __init__(self):
        """
        feed is a dictionary that stores the aggregated volume for each current bid and ask price
        indexes stores the orders with all their information for bids and asks (stores them seperately)
        depth stores the sorted unique prices of the current bids and asks
        snapshot stores the current snapshot at any particular time or order trade.
        """
        self.feed = {OrderSide.BID: defaultdict(int),OrderSide.ASK: defaultdict(int)}
        self.indexes = {OrderSide.BID: {}, OrderSide.ASK: {}}
        self.depth = {OrderSide.BID: MaxHeap(OrderBook.price_depth), OrderSide.ASK: MaxHeap(OrderBook.price_depth)}
        self.snapshot = {OrderSide.BID: [], OrderSide.ASK: []}
    
    def order_added(self,order):
        """ Adds an order to orderbook"""
        self.feed[order.side][order.price] += order.size
        self.indexes[order.side][order.order_id] = order
        self.depth[order.side].push(order.price)
        

    def order_deleted(self,order):
        """ Removes an order from order book 
        Also removes the price from the order book there is no remaining volume for that price
        """
        orderNew = self.indexes[order.side][order.order_id]
        self.feed[order.side][orderNew.price] -= orderNew.size
        if self.feed[order.side][orderNew.price] == 0:
            self.depth[order.side].remove(orderNew.price)
            del self.feed[order.side][orderNew.price]    
        del self.indexes[order.side][orderNew.order_id]

    def order_updated(self,order):
        """ Updates order by deleteing the old order and adding the new order """
        self.order_deleted(order)
        self.order_added(order)
        
    def order_traded(self,order):
        """ Processes an order trade and deletes order and order price 
        if there is no more size/volume for either 
        """
        orderNew = self.indexes[order.side][order.order_id]
        self.feed[order.side][orderNew.price] -= order.volume
        self.indexes[order.side][order.order_id].size -= order.volume
        if self.indexes[order.side][order.order_id].size == 0:
            del self.indexes[order.side][order.order_id]
        if self.feed[order.side][orderNew.price] == 0:
            self.depth[order.side].remove(orderNew.price)
            del self.feed[order.side][orderNew.price]
    
    def check_snapshot(self):
        """ Checks if the snapshot has changed 
        returns the new snapshot if it has
        returns empty list if it hasn't
        """
        asks = self.depth[OrderSide.ASK].get_asks()
        bids = self.depth[OrderSide.BID].get_bids()
        bid_list = []
        ask_list = []
        for i in range(0, len(bids)):
            bid_i = (bids[i], self.feed[OrderSide.BID][bids[i]])
            bid_list.append(bid_i)
        for i in range(0, len(asks)):
            asks_i = (asks[i], self.feed[OrderSide.ASK][asks[i]])
            ask_list.append(asks_i)
        if bid_list != self.snapshot[OrderSide.BID] or ask_list != self.snapshot[OrderSide.ASK]:
            self.snapshot[OrderSide.BID] = bid_list
            self.snapshot[OrderSide.ASK] = ask_list
            return [self.snapshot[OrderSide.BID], self.snapshot[OrderSide.ASK]]
        return []
  
        


