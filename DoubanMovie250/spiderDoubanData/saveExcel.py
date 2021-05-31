import xlwt

def saveData(dataList, savepath):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 样式压缩效果
    sheet = book.add_sheet('豆瓣电影250', cell_overwrite_ok=True)  # 单元格内容覆盖重写
    col = ('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评价数', '概况', '相关信息')
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列标题
    for i in range(0, 250):
        data = dataList[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)
    print('数据已保存')