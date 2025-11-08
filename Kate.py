class LengthLimit:
    def __init__(self, limit = 300):
        self.length_limit = limit
        self.last_stop = -1
        self.last_space = -1

    def reset(self):
        self.last_stop = -1
        self.last_space = -1

    def is_stop_char(self, char: str):
        stop_chars = [".", "?", "!"]
        return not char.isalnum() or char in stop_chars

    def is_whitespace_char(self, char: str):
        space_chars = [" ", "\n", "\t"]
        return not char.isalnum() or char in space_chars

    def is_length_exceeded(self, text: str, start_index: int, current_index: int):
        return current_index - start_index+1 >= self.length_limit
    
    def check(self, text:str, start_index, current_index: int) -> bool:
        if self.is_stop_char(text[current_index]):
            self.last_stop = current_index

        if self.is_whitespace_char(text[current_index]):
            self.last_space = current_index
        
        return self.is_length_exceeded(text, start_index, current_index)

    def handle(self, text: str, start_index: int, current_index: int) -> tuple[str, int]:
        if self.last_stop >= 0:
            result = ([text[start_index: self.last_stop].strip()], self.last_stop)
        elif self.last_space >= 0:
            result = ([text[start_index: self.last_space].strip()], self.last_space)
        else:
            result = ([text[start_index: current_index].strip()], current_index)

        self.reset()
        return result

class CommandChar:
    def __init__(self):
        pass

    def check(self, text:str, start_index, current_index: int) -> bool:
        return text[current_index] == "#"

    def handle(self, text: str, start_index: int, current_index: int) -> tuple[str, int]:
        pass

def chunkify(text: str, start_index, end_index, chunk_helpers: list[any]):
    start = start_index
    for i in range(start_index, end_index):
        for helper in chunk_helpers:
            if helper.check(text, start, i):
                res: tuple[str, int] = helper.handle(text, start, i)
                start = res[1]
                for txt in res[0]:
                    yield txt



chunk = LengthLimit()
txt: str = "Sleep!#Snap Good boy! You're going to wake up incredibly horny for Kate."
for chunk in chunkify(txt, 0, len(txt), [chunk]):
    print(f'|{chunk}|')