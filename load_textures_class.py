import xml.etree.ElementTree as ET
import arcade


class Load_textures:
        def __init__(self):
            self.path_image = "assets/Spritesheet/onlyObjects_default.png"

            self.atlas = arcade.load_texture(self.path_image)

            self.path_to_atlas = "assets/Spritesheet/onlyObjects_default.xml"

            self.tree = ET.parse(self.path_to_atlas)
            self.root = self.tree.getroot()

            self.subtextures = self.root.findall("SubTexture")
            print(self.subtextures)
            print('--------------')

        def get_texture(self, name):
            for texture in self.subtextures:
                print(texture.get('name'))
                if texture.get('name') == name:
                    print(texture.get('x'), texture.get('y'),
                          texture.get('width'), texture.get('height'))
                    return self.atlas.crop(
                         texture.get('x'), texture.get('y'),
                         texture.get('width'), texture.get('height'))


textures = Load_textures()
textures.get_texture('tankBody_red.png')
