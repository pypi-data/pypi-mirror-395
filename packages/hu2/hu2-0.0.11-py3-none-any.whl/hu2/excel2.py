from dataclasses import dataclass
from typing import Dict,Any

from openpyxl.styles import Alignment, Fill, Font, Border, Side
from openpyxl.workbook import Workbook
from openpyxl.cell import Cell



COLOR_BLACK = '00000000'  #COLOR_INDEX[0]
'''黑色'''

COLOR_WHITE = '00FFFFFF'  #COLOR_INDEX[1]
'''白色'''

COLOR_RED   = '00FF0000'  #COLOR_INDEX[2]
'''红色'''

COLOR_DARKRED = '00000000'  #COLOR_INDEX[8]
'''深红'''

COLOR_BLUE = '000000FF'  #COLOR_INDEX[4]
'''蓝色'''

COLOR_DARKBLUE = '000000FF'  #COLOR_INDEX[12]
'''深蓝'''

COLOR_GREEN = '0000FF00'  #COLOR_INDEX[3]
'''绿色'''
COLOR_DARKGREEN = '00FFFFFF'  #COLOR_INDEX[9]
'''深绿'''
COLOR_YELLOW = '00FFFF00'  #COLOR_INDEX[5]
'''黄色'''
COLOR_DARKYELLOW = '00808000'  #COLOR_INDEX[19]
'''深黄'''
sd = Side(style='thin')
BORDER = Border(left=sd, right=sd, top=sd, bottom=sd)

@dataclass
class ExcelStyle:
    '''支持 字体设置  填充设置  对其设置  有无边框设置'''
    font: Font = None
    fill: Fill = None
    alignment: Alignment = None
    border: bool = False
class ExcelTable:
    def __init__(self, file_name):
        self.head_list = None
        self.head_style = None
        self.body_grid = None
        self.body_style = None
        self.file_name = file_name
        self.wb = Workbook()
        self.sheet = self.wb.active
    def set_head_style(self,style:ExcelStyle):
        ''' 设置 列头区域单元格的 全局样式 '''
        self.head_style = style

    def set_head(self, head_list: [str]):
        ''' 设置列头区域单元格内容，数组 '''
        self.head_list = head_list

    def set_body(self, body_grid: [[Any]]):
        ''' 设置 数据区域的单元格内容，二维数组 '''
        self.body_grid = body_grid

    def set_body_style(self, style: ExcelStyle):
        ''' 设置 数据区域单元格的 全局样式 '''
        self.body_style = style


    def set_column_width(self, col_width_dict: Dict[str, int]):
        '''设置指定列的宽度，可以一次指定多列，dict中格式：{'A':30}'''
        for col_str, col_width in col_width_dict.items():
            self.sheet.column_dimensions[col_str].width = col_width

    @staticmethod
    def _set_style(style: ExcelStyle, cell:Cell):
        if style is None:
            return
        if style.fill is not None:
            cell.fill = style.fill
        if style.alignment is not None:
            cell.alignment = style.alignment
        if style.font is not None:
            cell.font = style.font
        if style.border:
            cell.border = BORDER
        return cell

    def save(self):
        '''
        将列头、数据区域 样式 和 内容 都设置到 Excel的sheet中，并保存到文件中
        :return:
        '''
        if self.head_list is not None:
            for index, head in enumerate(self.head_list):
                cell = self.sheet.cell(row=1, column=index + 1, value=str(head))
                ExcelTable._set_style(self.head_style, cell)

        if self.body_grid is not None:
            for row in self.body_grid:
                self.sheet.append(row)

        body_start_idx = 1 if self.head_list else 0
        for i,row in enumerate(self.sheet.rows):
            # 遍历每一行，对数据区域 继续遍历行中单元格 设置样式
            if i >= body_start_idx :
                for cell in row:
                    ExcelTable._set_style(self.body_style, cell)

        self.wb.save(self.file_name)
