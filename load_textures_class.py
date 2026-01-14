import xml.etree.ElementTree as ET
import arcade


class Load_textures:
        def __init__(self):
            self.path_image = "assets/Spritesheet/onlyObjects_default.png"

            self.atlas = arcade.load_texture(self.path_image)

            self.path_to_atlas = "assets/Spritesheet/allSprites_default.xml"

            self.tree = ET.parse(self.path_to_atlas)
            self.root = self.tree.getroot()

            self.subtetures = self.root.findall("SubTexture")

        def get_texture(self, name):
            for texture in self.subtetures:
                if texture.name == name:
                    return self.atlas.crop(texture.x, texture.y,
                                           texture.width, texture.height
                                           )
