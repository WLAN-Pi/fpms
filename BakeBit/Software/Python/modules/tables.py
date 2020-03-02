#################################
# Various display tables
#################################
import bakebit_128_64_oled as oled
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import bakebit_128_64_oled as oled

from screen import *
from navigation import *

class SimpleTable(object):

    def __init__(self, g_vars):

        # grab a screeb obj
        self.screen_obj = Screen()

        # Create image & draw objects
        self.image = Image.new('1', (g_vars.get('width'), g_vars.get('height')))
        self.draw = ImageDraw.Draw(self.image)

        # grab a navigation obj
        self.nav_button_obj = NavButton(g_vars['draw'], g_vars['nav_bar_top'], 255, g_vars['smartFont'])

    def display_simple_table(self, g_vars, item_list, back_button_req=0, title='', font="small"):
        '''
        This function takes a list and paints each entry as a line on a
        page. It also displays appropriate up/down scroll buttons if the
        entries passed exceed a page length (one line at a time)
        '''

        g_vars['drawing_in_progress'] = True
        g_vars['display_state'] = 'page'

        # Clear display prior to painting new item
        self.screen_obj.clear_display(g_vars)

        y = 0
        x = 0
        font_offset = 0

        if font == "small":
            font_type = g_vars['smartFont']
            font_size = 11
            item_length_max = 20
            table_display_max = 5
        elif font == "medium":
            font_type = g_vars['font11']
            font_size = 11
            item_length_max = 17
            table_display_max = 4

        # write title if present
        if title != '':
            g_vars['draw'].text((x, y + font_offset), title.center(item_length_max,
                                                               " "),  font=font_type, fill=255)
            font_offset += font_size
            table_display_max -= 1

        previous_table_list_length = g_vars['table_list_length']
        g_vars['table_list_length'] = len(item_list)

        # if table length changes, reset current scroll selection
        # e.g. when showing lldp table info and eth cable
        # pulled so list size changes
        if g_vars['table_list_length'] != previous_table_list_length:
            g_vars['current_scroll_selection'] = 0

        # if we're going to scroll of the end of the list, adjust pointer
        if g_vars['current_scroll_selection'] + table_display_max > g_vars['table_list_length']:
            g_vars['current_scroll_selection'] -= 1

        # modify list to display if scrolling required
        if g_vars['able_list_length'] > table_display_max:

            table_bottom_entry = g_vars['current_scroll_selection'] + table_display_max
            item_list = item_list[g_vars['current_scroll_selection']: table_bottom_entry]

            # show down if not at end of list in display window
            if table_bottom_entry < g_vars['table_list_length']:
                self.nav_button_obj.down()

            # show an up button if not at start of list
            if g_vars['current_scroll_selection'] > 0:
                self.nav_button_obj.next(label="Up")

        for item in item_list:

            if len(item) > item_length_max:
                item = item[0:item_length_max]

            self.draw.text((x, y + font_offset), item,
                            font=font_type, fill=255)

            font_offset += font_size

        # Back button
        if back_button_req:
            self.nav_button_obj.back(label="Exit")

        oled.drawImage(g_vars['image'])

        g_vars['display_state'] = 'page'
        g_vars['drawing_in_progress'] = False

        return
