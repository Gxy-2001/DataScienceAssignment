from pyecharts import options as opts
from pyecharts.charts import Radar

data = [
    # {"value": [0.3368, 0.2092, 0.0208, 0.0364, 0.3967], "name": "人传人"},
    {"value": [0.5491, 0.4166, 0.0042, 0.0042, 0.0256], "name": "复工"},
    # {"value": [0.4541, 0.4378, 0.0203, 0.0325, 0.0549], "name": "对口支援"},
    # {"value": [0.2822, 0.1173, 0.0203, 0.0193, 0.5606], "name": "封城"},
]
c_schema = [
    {"name": "乐", "max": 0.55, "min": 0},
    {"name": "好", "max": 0.55, "min": 0},
    {"name": "哀", "max": 0.55, "min": 0},
    {"name": '恶', "max": 0.55, "min": 0},
    {"name": "惧", "max": 0.55, "min": 0},
]
c = (
    Radar()
        .set_colors(["#CC3300"])
        .add_schema(
        schema=c_schema,
        shape="circle",
        center=["50%", "50%"],
        radius="80%",
        angleaxis_opts=opts.AngleAxisOpts(
            min_=0,
            max_=360,
            is_clockwise=False,
            interval=5,
            axistick_opts=opts.AxisTickOpts(is_show=False),
            axislabel_opts=opts.LabelOpts(is_show=False),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            splitline_opts=opts.SplitLineOpts(is_show=False),
        ),
        radiusaxis_opts=opts.RadiusAxisOpts(
            min_=-4,
            max_=4,
            interval=2,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        polar_opts=opts.PolarOpts(),
        splitarea_opt=opts.SplitAreaOpts(is_show=False),
        splitline_opt=opts.SplitLineOpts(is_show=False),
    )
        .add(
        series_name="复工复产",
        data=data,
        areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
        linestyle_opts=opts.LineStyleOpts(width=3),
    )
        .render("img/复工复产.html")
)
