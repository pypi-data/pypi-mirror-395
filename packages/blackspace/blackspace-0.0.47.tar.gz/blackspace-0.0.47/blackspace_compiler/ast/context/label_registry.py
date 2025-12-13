class LabelRegistry:
    def __init__(self):
        self._counter = 0

    def new_label(self) -> int:
        label = self._counter
        self._counter += 1
        return label
