class Style:
    """
    A class which contains the color codes for printing in color
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    END = "\033[0m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cprint(text, option = "white", *args, **kwargs):
    """
    Prints the text with the option provided.
    Available options are:
    - black
    - red
    - green
    - yellow
    - blue
    - magenta
    - cyan
    - white
    - header
    - okblue
    - okgreen
    - warning
    - fail
    - bold
    - underline

    >> cprint("Hello", "green")
    """

    option_upper = option.upper()
    if option_upper not in Style.__dict__.keys():
        raise ValueError(f"The option {option} not found. Available options are: {', '.join(list(Style.__dict__.keys())[2:-2])}")
    print(eval(f"Style.{option_upper}") + str(text) + Style.END, *args, **kwargs)