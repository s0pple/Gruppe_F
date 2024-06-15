import os


class Console(object):
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError("Implement this method")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    """
    This function formats and prints a given title and prompt with a specific width. 
    It adds stars (*) to the left and right of the title and prompt, and fills the remaining width with spaces.
    If the title or prompt contains multiple lines (detected by newline characters), it will not add stars or spaces.
    If a prompt is provided, it will also wait for user input and return it.

    Parameters:
    title (str): The main text to be displayed.
    prompt (str, optional): Additional text that asks for user input. Defaults to None.
    width (int, optional): The total width of the printed line, including stars and spaces. Defaults to 90.

    Returns:
    str: The user input if a prompt is provided, otherwise None.
    """
    @staticmethod
    def format_text(title, prompt=None, width=90):
        left = "* "
        right = " *"
        multiple_lines = '\n' in title or (prompt and '\n' in prompt)

        if not multiple_lines:
            print("*" * width)
        space = " " * (width - len(left) - len(title) - len(right))
        print(
            f"{left if not multiple_lines else ''}{title}{space if not multiple_lines else ''}{right if not multiple_lines else ''}")
        if prompt:
            space = " " * (width - len(left) - len(prompt) - len(right))
            print(
                f"{left if not multiple_lines else ''}{prompt}{space if not multiple_lines else ''}{right if not multiple_lines else ''}")
        if not multiple_lines:
            print("*" * width)
        else:
            print("-" * width)

        user_input = None
        if prompt:
            user_input = input()
        return user_input


class Application(object):

    def __init__(self, start: Console):
        self._current: Console = start

    def run(self):
        while self._current:
            self._current = self._current.run()


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)


class Menu(Console):
    def __init__(self, title, width=90):
        super().__init__()
        self._title = title
        self._options = []
        self._width = width

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: MenuOption):
        self._options.append(option)

    def remove_option(self, option: MenuOption):
        self._options.remove(option)

    def _show(self):
        print("*" * self._width)
        left = "*"
        right = "*"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("*" * self._width)
        for i, option in enumerate(self, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("*" * self._width)

    def _make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self._show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int) -> Console:
        raise NotImplementedError("Implement this method")

    def run(self) -> Console:
        self.clear()
        self._show()
        return self._navigate(self._make_choice())
