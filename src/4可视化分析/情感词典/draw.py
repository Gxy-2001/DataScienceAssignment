from pyecharts.charts import *
from pyecharts import options as opts

x_data = ['3月10日', '3月11日', '3月12日', ]
y_data_2 = ['14.150', '16.301', '20.844', ]
y_data_1 = ['13.6843', '37.3377', '18.9978']


def bar_with_multiple_axis():
    bar = Bar(init_opts=opts.InitOpts(theme='macarons',
                                      width='500px',
                                      height='300px'))
    bar.add_xaxis(x_data)
    # 添加一个Y轴
    bar.extend_axis(yaxis=opts.AxisOpts())
    # 分别指定使用的Y轴
    bar.add_yaxis("'复工复产'事件下情感值", y_data_1, yaxis_index=0)
    bar.add_yaxis("当天平均情感值", y_data_2, yaxis_index=0)
    return bar


chart = bar_with_multiple_axis()
chart.render('img/复工复产情感对比.html')
