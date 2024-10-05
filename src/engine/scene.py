from src.engine.models import *
from src.worlds.world import World


class Scene:
    def __init__(self, app):
        self.app = app
        self.elements = []
        if app.world:
            self.load(app.world)
        self.skybox = Skybox(app)
        self.total_ticks = 0

    def load(self, world: World):
        for element in world.__dict__.keys():
            current_element = getattr(world, element)
            self.elements.append(
                current_element.model(
                    app=self.app,
                    texture_id=current_element.texture,
                    scale=current_element.scale,
                    rotation=current_element.rotation,
                    position=current_element.position,
                    instance=current_element.instance,
                    saturated=current_element.saturated,
                )
            )
            
    def update(self):
        self.total_ticks += self.app.delta_time

        for element in self.elements:
            if element.instance:
                element.update_visual(
                    position=element.instance.position,
                    scale=element.instance.scale,
                    rotation=element.instance.rotation,
                )
    
    def destroy(self):
        del self
