from pyecharts.charts import *
from pyecharts import options as opts

x = ['疫情认知相关', '群众自我相关', '社会行为相关']
y = [91, 77, 33]  # 复工复产
y1 = [41, 60, 97]  # 对口支援
y2 = [110, 42, 56, ]  # 人传人
y3 = [119, 69, 15]  # 武汉封城


def pie_custom_radius():
    pie = Pie(init_opts=opts.InitOpts(theme='light',
                                      width='600px',
                                      height='400px'))
    pie.add("人传人",
            [list(z) for z in zip(x, y2)],
            # 设置半径范围，0%-100%
            radius=["40%", "75%"])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="人传人事件", subtitle='聚类饼图'))
    pie.set_series_opts(
        # 自定义数据标签
        label_opts=opts.LabelOpts(position='top',
                                  color='red',
                                  font_family='Arial',
                                  font_size=12,
                                  font_style='italic',
                                  interval=1,
                                  formatter='{b}:{d}%'
                                  )
    )
    return pie


chart = pie_custom_radius()
chart.render('img/人传人聚类分析饼图.html')
