import callirhoe
import layouts._base as layout
import lib

def main_program():
    paper = "a4w"
    cols = rows = 1
    #when cols and rows are both 1, then calendar month
    #takes up one page each, of a4 paper

    callirhoe.main_program(paper, cols, rows)

if __name__ == "__main__":
    try:
        main_program()
    except lib.Abort as e:
        sys.exit(e.args[0])
