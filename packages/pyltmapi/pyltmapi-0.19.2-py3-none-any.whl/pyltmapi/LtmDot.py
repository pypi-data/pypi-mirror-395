import graphviz
from IPython.display import Image, display


def display_dot_image(dot_string: str):
    graph = graphviz.Source(dot_string)
    display(graph)


class printer(str):
    def __repr__(self):
        return self


def print(str: str):
    display(printer(str))
