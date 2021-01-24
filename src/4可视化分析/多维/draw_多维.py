import os
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig

CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s/%s' % (filepath, allDir)))
    return child


def img():
    v1 = [[0.3176, 0.3104, 0.0356, 0.0441, 0.2910]]
    v2 = [[0.2953, 0.2881, 0.0552, 0.0422, 0.3188]]
    v3 = [[0.2793, 0.3582, 0.0546, 0.0556, 0.2518]]
    v4 = [[0.2767, 0.3668, 0.0521, 0.0670, 0.2370]]

    (
        Radar(init_opts=opts.InitOpts(width="720px", height="480px", bg_color="#ffffff"))
            .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="乐", max_=0.4),
                opts.RadarIndicatorItem(name="好", max_=0.4),
                opts.RadarIndicatorItem(name="哀", max_=0.4),
                opts.RadarIndicatorItem(name="恶", max_=0.4),
                opts.RadarIndicatorItem(name="惧", max_=0.4),
            ],
            splitarea_opt=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
            textstyle_opts=opts.TextStyleOpts(color="#000"),
        )
            .add(
            series_name="阶段一(红色)",
            data=v1,
            linestyle_opts=opts.LineStyleOpts(color="#CD0000", width=3),
        )
            .add(
            series_name="阶段二(蓝色)",
            data=v2,
            linestyle_opts=opts.LineStyleOpts(color="#5CACEE", width=3),
        )
            .add(
            series_name="阶段三(绿色)",
            data=v3,
            linestyle_opts=opts.LineStyleOpts(color="green", width=3, opacity=0.3, type_='dashed'),
        )
            .add(
            series_name="阶段四(黄色)",
            data=v4,
            linestyle_opts=opts.LineStyleOpts(color="yellow", width=3, opacity=0.8),
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="多维情感分析"), legend_opts=opts.LegendOpts()
        )
            .render("img/多维雷达图.html")
    )


if __name__ == "__main__":
    filepwd = eachFile("data")
    img()
