from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig

CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
y1 = [1.4124, 1.5378, 1.3091, 1.1416, 1.0263, 0.9346, 0.8672, 0.8144]
y2 = [0.426, 0.229, 0.235, 0.241, 0.242, 0.158, 0.159, 0.161]
y3 = [2.196, 1.905, 2.080, 2.008, 1.721, 2.373, 2.212, 2.122]
x = ['2', '3', '4', '5', '6']
y4 = [0.9522, 0.5239, 0.3899, 0.3296, 0.2737]
y5 = [0.067, 0.067, 0.070, 0.052, 0.053]
y6 = [1.940, 2.434, 4.878, 4.972, 5.831]

xx = ['0.001', '0.051', '0.101', '0.151', '0.201', '0.251', '0.301', '0.351', '0.401', '0.451', '0.501', ]
y7 = [1.5968, 1.6052, 1.5225, 1.5299, 1.5123, 1.4628, 1.5377, 1.5927, 1.6724, 1.5725, 1.5029]
y8 = [0.1222, 0.1327, 0.1433, 0.1436, 0.1444, 0.1465, 0.1409, 0.1053, 0.0762, 0.0896, 0.0931, ]
y9 = [0.9882, 1.0155, 1.058, 1.0599, 1.135, 1.1562, 1.1812, 1.248, 1.4199, 1.5569, 1.5884, ]


def line_with_custom_linestyle():
    line = Line(init_opts=opts.InitOpts(theme='light',
                                        width='1200px',
                                        height='500px'))
    line.add_xaxis(xx)
    line.add_yaxis('CH值(除10后)',
                   y7,
                   linestyle_opts=opts.LineStyleOpts(width=5,
                                                     curve=0,
                                                     opacity=0.7,
                                                     type_='solid',
                                                     color='#42A7DC')
                   )
    line.add_yaxis('轮廓系数',
                   y8,
                   linestyle_opts=opts.LineStyleOpts(width=3,
                                                     curve=0.5,
                                                     opacity=0.9,
                                                     type_='dashed',
                                                     color='#67E0E3')
                   )
    line.add_yaxis('戴维森堡丁指数(DBI)',
                   y9,
                   linestyle_opts=opts.LineStyleOpts(width=5,
                                                     curve=1,
                                                     opacity=0.5,
                                                     type_='dotted',
                                                     color='yellow')
                   )
    return line


def readFile():
    file = open('DBSCAN聚类数.txt', 'r', encoding='utf-8')
    l = file.readlines()
    data_x = []
    data_y1 = []
    data_y2 = []
    data_y3 = []
    for x in l:
        li = x.split()
        data_x.append(float(li[0]))
        data_y1.append(float(li[1][0:6]) / 10)
        data_y2.append(float(li[2][0:6]))
        data_y3.append(float(li[3][0:6]))
    return data_x, data_y1, data_y2, data_y3


chart = line_with_custom_linestyle()
chart.render('img/DBSCAN类数.html')
