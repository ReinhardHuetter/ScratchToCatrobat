#  ScratchToCatrobat: A tool for converting Scratch projects into Catrobat programs.
#  Copyright (C) 2013-2015 The Catrobat Team
#  (http://developer.catrobat.org/credits)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  An additional term exception under section 7 of the GNU Affero
#  General Public License, version 3, is available at
#  http://developer.catrobat.org/license_additional_term
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
import os
import unittest

from scratchtocatrobat import common_testing
from scratchtocatrobat.tools import image_processing as img_proc
import java.awt.Font
from java.awt import Color
import java.awt.image.BufferedImage
import imghdr
from test._mock_backport import _allowed_names

class ImageProcessingTest(common_testing.BaseTestCase):

    _allowed_font_names = ["Marker","Scratch","Gloria", "Helvetica", "Donegal", "Mystery"]

    @classmethod
    def img_proc_pngfile_paths(cls):
        return cls.get_test_resources_paths("img_proc_png")

    @classmethod
    def img_proc_pngfile_output_path(cls, fileName):
        return os.path.join(common_testing.get_test_resources_path(), "img_proc_png", fileName)

    @classmethod
    def img_proc_jpgfile_paths(cls):
        return cls.get_test_resources_paths("img_proc_jpg")

    @classmethod
    def setUpClass(cls):
        #assert len(cls.img_proc_pngfile_paths()) == 1
        assert len(cls.img_proc_jpgfile_paths()) == 0

    def test_can_read_editable_image_from_disk(self):
        dummy_png = self.img_proc_pngfile_paths()[0]
        buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
        assert isinstance(buffered_image, java.awt.image.BufferedImage)

    def test_can_create_font(self):
        for font_name in self._allowed_font_names:
            for (bold, italic) in [(False, False), (False, True), (True, False), (True, True)]:
                font = img_proc.create_font(font_name, 14.0, )
                assert isinstance(font, java.awt.Font)
                print(font.getFontName() )  #results to error
                assert font.getSize() == 14
                

    
              
        
        
    def test_check_stretched_text_on_image(self):   
        dummy_png = self.img_proc_pngfile_paths()[0]
        buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
        font = img_proc.create_font(self._allowed_font_names[0], 14.0, bold=False, italic=False)
        textbox_width = 10
        textbox_height = 10
        buffered_image = img_proc.add_text_to_image(buffered_image, "this is a stretched text", font, Color.BLUE, 10.0, 10.0)
        
        
        
        
    def test_can_add_text_to_editable_image(self):
        dummy_png = self.img_proc_pngfile_paths()[0]
        #buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
        #assert isinstance(buffered_image, java.awt.image.BufferedImage)
        for font_name in self._allowed_font_names:
            font = img_proc.create_font(font_name, 14.0, bold=False, italic=False)
            # check whether the left-outline of letter "H" in "Hello world" is NOT present in the image!
            test_colors = { Color.BLUE: (0, 0, 255), Color.RED: (255, 0, 0), Color.WHITE: (255, 255, 255), Color.BLACK: (0,0,0) }
            for (color, value) in test_colors.iteritems():
                buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
                assert isinstance(buffered_image, java.awt.image.BufferedImage)
                #test1 8 pixel down
                for i in range(0, 8):
                    rgb = buffered_image.getRGB(11, i)               
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff
                    assert red == 0 and green == 0 and blue == 0 and alpha == 0
                buffered_image = img_proc.add_text_to_image(buffered_image, "Hello world!", font, color, 10.0, 10.0)
                #buffered_image = img_proc.add_text_to_image(buffered_image, "Franz ist hier!?", font, Color.BLUE,10.0, 2.0)
                # the left-outline of letter "H" in "Hello world" must NOW appear in the image!
                for i in range(0, 8):
                    rgb = buffered_image.getRGB(11, i)
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff;
                   
                    if font_name == self._allowed_font_names[3]: #helvetica
                        assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[0]: #marker
                        if i > 0 and i < 8:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[1]: #scratch
                        if i == 1 or i == 6 or i == 7: 
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[2]: #gloria
                        if i == 6 or i == 7:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[4]: #donegal
                        if i == 1:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[5]: #mystery
                        assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                        
                #test2 second letter 10 pixel down
                buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
                assert isinstance(buffered_image, java.awt.image.BufferedImage)
                for i in range(20, 29):
                    rgb = buffered_image.getRGB(i, 3)               
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff
                    assert red == 0 and green == 0 and blue == 0 and alpha == 0
                buffered_image = img_proc.add_text_to_image(buffered_image, "Hello world!", font, color, 10.0, 10.0)
                #buffered_image = img_proc.add_text_to_image(buffered_image, "Franz ist hier!?", font, Color.BLUE,10.0, 2.0)
                #some pixels in x space line must appear now
                for i in range(20, 29):
                    rgb = buffered_image.getRGB(i, 3)
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff;
                    if font_name == self._allowed_font_names[3]: #helvetica
                        if i == 22 or i == 23 or i == 24 or i == 25:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[0]: #marker
                        if (i >= 21 and i  <= 26) or i == 29 or i == 30:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[1]: #scratch
                        if (i >= 17 and i <= 21):
                            assert red == 0 and green == 0 and blue == 0 and alpha == 0
                    if font_name == self._allowed_font_names[2]: #gloria
                        if i == 23 or i == 24 or i == 26:
                            assert red == value[0] and green == value[1] and blue == value[2]and alpha == 255
                    if font_name == self._allowed_font_names[4]: #donegal
                        if i >=21 and i <= 26:
                            assert red == 0 and green == 0 and blue == 0 and alpha == 0
                    if font_name == self._allowed_font_names[5]: #mystery
                        if i >=20 and i <= 22:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                            
                            
                            
                            
                            
                #test3 first whole line test
                buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
                assert isinstance(buffered_image, java.awt.image.BufferedImage)
                for i in range(10, 94):
                    rgb = buffered_image.getRGB(i, 0)               
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff
                    assert red == 0 and green == 0 and blue == 0 and alpha == 0
                buffered_image = img_proc.add_text_to_image(buffered_image, "Hello world!", font, color, 10.0, 10.0)
                #buffered_image = img_proc.add_text_to_image(buffered_image, "Franz ist hier!?", font, Color.BLUE,10.0, 2.0)
                #some pixels in x space line must appear now
                for i in range(10, 94):
                    rgb = buffered_image.getRGB(i, 0)
                    red = rgb >> 16 & int("0x000000FF", 16)
                    green = rgb >> 8 & int("0x000000FF", 16)
                    blue = rgb & int("0x000000FF", 16)
                    alpha = (rgb>>24) & 0xff
                    if font_name == self._allowed_font_names[3]: #helvetica
                        if i == 11 or i == 18 or i == 29 or i == 32 or i == 70 or i == 78 or i == 82:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[0]: #marker
                        if i == 12 or i == 17 or i == 18:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[1]: #scratch
                        if i == 14 or i == 15 or i == 16 or i == 17:
                            assert red ==value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[2]: #gloria
                        if i == 12 or i == 19 or i == 30 or i ==34 or i == 79 or i == 88 or i == 92 or i == 93:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[4]: #donegal
                        if i== 26 or i == 27 or i == 29 or i == 30 or i == 64 or i == 65 or i == 72:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                    if font_name == self._allowed_font_names[5]: #mystery
                        if (i >=10  and i <= 12)  or (i >= 15 and i <= 17) or i == 25 or i == 28 or i == 66 or i == 73 or i == 76 or i == 77:
                            assert red == value[0] and green == value[1] and blue == value[2] and alpha == 255
                

                   

                        
                    

                            

                            
                            
    
                         

                        

    def test_can_save_editable_image_as_png_to_disk(self):
        dummy_png = self.img_proc_pngfile_paths()[0]
        buffered_image = img_proc.read_editable_image_from_disk(dummy_png)
        assert isinstance(buffered_image, java.awt.image.BufferedImage)
        font = img_proc.create_font(self._allowed_font_names[0], 14.0, bold=False, italic=False)
        marker_font_value = 0
        scratch_font_value = 1
        gloria_font_value = 2
        helvetica_font_value = 3
        donegal_font_value = 4
        mystery_font_value = 5
        
        marker_font =  img_proc.create_font(self._allowed_font_names[marker_font_value], 14.0, bold=False, italic=False)
        scratch_font =  img_proc.create_font(self._allowed_font_names[scratch_font_value], 14.0, bold=False, italic=False)
        gloria_font =  img_proc.create_font(self._allowed_font_names[gloria_font_value], 14.0, bold=False, italic=False)
        helvetica_font =  img_proc.create_font(self._allowed_font_names[helvetica_font_value], 14.0, bold=False, italic=False)
        donegal_font =  img_proc.create_font(self._allowed_font_names[donegal_font_value], 14.0, bold=False, italic=False)
        mystery_font =  img_proc.create_font(self._allowed_font_names[mystery_font_value], 14.0, bold=False, italic=False)
        
        
        # check whether the left-outline of letter "H" in "Hello world" is NOT present in the image!
        for i in range(0, 8):
            rgb = buffered_image.getRGB(11, i)
            red = rgb >> 16 & int("0x000000FF", 16)
            green = rgb >> 8 & int("0x000000FF", 16)
            blue = rgb & int("0x000000FF", 16)
            alpha = (rgb>>24) & 0xff
            assert red == 0 and green == 0 and blue == 0 and alpha == 0
        buffered_image = img_proc.add_text_to_image(buffered_image, "Hello world!", helvetica_font, Color.BLUE, 10.0, 10.0)
        #buffered_image = img_proc.add_text_to_image(buffered_image, "Franz ist hier!?", marker_font, Color.BLUE,10.0, 20.0)
        #buffered_image = img_proc.add_text_to_image(buffered_image, "iloveKF", donegal_font, Color.GREEN,10.0, 32.0)


        # the left-outline of letter "H" in "Hello world" must NOW appear in the image!
        for i in range(0, 8):
            rgb = buffered_image.getRGB(11, i)
            red = rgb >> 16 & int("0x000000FF", 16)
            green = rgb >> 8 & int("0x000000FF", 16)
            blue = rgb & int("0x000000FF", 16)
            alpha = (rgb>>24) & 0xff
            assert red == 0 and green == 0 and blue == 255 and alpha ==255
        output_path = self.img_proc_pngfile_output_path("test.png")
        try:
            img_proc.save_editable_image_as_png_to_disk(buffered_image, output_path, overwrite=True)
            assert os.path.isfile(output_path)
            assert imghdr.what(output_path) == 'png'
            # Reload the image from disk now and check if left-outline of letter "H" is still present!
            new_buffered_image = img_proc.read_editable_image_from_disk(output_path)
            assert isinstance(new_buffered_image, java.awt.image.BufferedImage)
            for i in range(0, 8):
                rgb = new_buffered_image.getRGB(11, i)
                red = rgb >> 16 & int("0x000000FF", 16)
                green = rgb >> 8 & int("0x000000FF", 16)
                blue = rgb & int("0x000000FF", 16)
                alpha = (rgb>>24) & 0xff;
                assert red == 0 and green == 0 and blue == 255 and alpha == 255
        except Exception, e:
            raise e
       # finally:
            #os.remove(output_path) # finally remove the image

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
