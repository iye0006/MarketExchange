# Order Book Snapshot

This project reads order book events from a binary file and generates snapshots of the top N bids and asks for each symbol. The events include order additions, updates, deletions, and trades.


## Dependencies

- Python 3.8

## Usage

1. Run the `main.py` script with the input file name and the desired depth N as command line arguments:


```bash
python main.py <file_name> <N>

```

## Example Command 

```bash
python main.py input1.stream 2

```


## Attached Files
I have attached the source code files. Which are
1. main.py
2. message.py
3. order_book.py



