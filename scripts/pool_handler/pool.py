from pygame import Surface
from sprites import Sprite


class SpritePool():
    def __init__(self, sprite: Sprite, size: int, resizable: bool=False) -> None:
        self.name: str = sprite.__name__
        self.sprites: 'list[Sprite]' = [sprite() for x in range(size)]
        self.resizable: bool = resizable
        self.size: int = size


    def update(self, *args, **kwargs):
        for sprite in self.sprites:
            if not sprite.disabled:
                pass

            sprite.update(args, kwargs)


    def render(self, layer: Surface, *args, **kwargs) -> None:
        for sprite in self.sprites:
            if not sprite.disabled:
                pass

            sprite.render(args, kwargs)