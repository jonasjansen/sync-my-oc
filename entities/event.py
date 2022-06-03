from entities.material import Material


class Event:

    event_name: str = ""
    material_list: [Material] = list()

    def __init__(self, event_name):
        self.event_name = event_name
        self.material_list = list()
        return
