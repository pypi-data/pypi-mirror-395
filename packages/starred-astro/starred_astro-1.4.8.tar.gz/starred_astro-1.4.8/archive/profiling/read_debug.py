import pstats

def main():
    p = pstats.Stats('debug.txt')
    p.sort_stats("time").print_stats(20)
    # p.sort_stats(sort='time').print_stats()

if __name__ == "__main__":
    main()