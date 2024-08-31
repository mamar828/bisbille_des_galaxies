class World:
    def update(self, delta_time):
        for obj in self.__dict__.values():
            if obj.instance:
                obj.instance.update(delta_time)
