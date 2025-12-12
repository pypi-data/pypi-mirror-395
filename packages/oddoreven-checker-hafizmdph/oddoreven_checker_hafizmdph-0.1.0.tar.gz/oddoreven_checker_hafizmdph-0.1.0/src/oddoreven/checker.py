def is_even(num):
    """Return True if the number is even."""
    return num % 2 == 0


def is_odd(num):
    """Return True if the number is odd."""
    return num % 2 != 0

def main():
    import sys
    if len(sys.argv) > 1:
        try:
            num = int(sys.argv[1])
            if is_even(num):
                print(f"{num} is even")
            else:
                print(f"{num} is odd")
        except ValueError:
            print("Please provide an integer")
    else:
        print("Usage: oddoreven <number>")

