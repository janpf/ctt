import altair as alt

data = "/page/plots/dataByRisk.json"

chart = alt.Chart(data).mark_line(point=True).encode(x="date:T", y="published:Q", color="risk:O")

nearest = alt.selection(type="single", nearest=True, on="mouseover", fields=["date"], empty="none")
selectors = alt.Chart(data).mark_point().encode(x="date:T", opacity=alt.value(0)).add_selection(nearest)

points = chart.mark_point().encode(opacity=alt.condition(predicate=nearest, if_true=alt.value(1), if_false=alt.value(0)))
text = chart.mark_text(align="right", dx=-5, dy=-5).encode(text=alt.condition(predicate=nearest, if_true="tt:N", if_false=alt.value(" "))).transform_calculate(tt="datum.published + ' keys with risk lvl ' + datum.risk")
rule = alt.Chart(data).mark_rule(color="gray").encode(x="date:T").transform_filter(nearest)

result = alt.layer(chart, selectors, points, rule, text).properties(width=500, height=250)
result.save("bla.html")
