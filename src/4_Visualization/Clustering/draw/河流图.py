from pyecharts.charts import *
from pyecharts import options as opts

x = ['第一阶段', '第二阶段', '第三阶段','第四阶段']
t1 = [[0.245, 0.173, 0.182, 0.099],
      [0.613, 0.511, 0.564, 0.314],
      [0.151, 0.324, 0.270, 0.557]]


def bar_stack():
    bar = Bar(init_opts=opts.InitOpts(theme='light',
                                      width='720px',
                                      height='450px'))
    bar.add_xaxis(x)
    # stack值一样的系列会堆叠在一起
    bar.add_yaxis('疫情认知相关', t1[0], stack='stack1')
    bar.add_yaxis('群众自我相关', t1[1], stack='stack1')
    bar.add_yaxis('社会行为相关', t1[2], stack='stack1')
    return bar


chart = bar_stack()
chart.render('img/四阶段对比图.html')
