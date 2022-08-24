from dotenv import load_dotenv, find_dotenv

class ListWork:
    def __init__(self, list_1, list_2):
        self.list_1 = list_1
        self.list_2 = list_2

    def add_favorites(self):
        if len(self.list_1) > 0:
            self.list_2.append(self.list_1[-1])

        else:
            pass

    def get_favorites(self):

        if len(self.list_2) > 0:
            return set(self.list_2)
        else:
            return f"у вас пока нет избранных контактов"

if __name__ == '__main__':
    load_dotenv(find_dotenv())
