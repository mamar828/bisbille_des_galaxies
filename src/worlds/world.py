class World:
    def update(self, app):
        for obj in self.__dict__.values():
            if obj.instance:
                obj.instance.update(app)
