

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

gsheetid = '1S7gJojFKedjSvSRM9npIDAzN_6mkSZhgEdGpNbxXnK0'
list_1 = 'sector_margin'
list_2 = 'growth_rate'

df_sector_margin_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_growth_rate_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)

df_sector_margin = pd.read_csv(df_sector_margin_csv)
df_growth_rate = pd.read_csv(df_growth_rate_csv)
df_growth_rate.set_index('growth_state', inplace=True)
df_sector_margin.set_index('sector', inplace=True)
df_sector_margin = pd.Series(df_sector_margin['margin'])
df_growth_rate = pd.Series(df_growth_rate['growth_rate'])

gro_state_list = df_growth_rate.index
industry_list = df_sector_margin.index


# Функция прибыли
def lost_profit(ind, mar, rev, marg, gro):
    growth_rate = df_growth_rate[mar]
    margin_ind_rate = df_sector_margin[ind]
    potencial_profit = rev * (margin_ind_rate)
    act_profit = (marg / 100) * rev
    profit_delta_qdc = max(potencial_profit - act_profit, 0.05 * act_profit)
    profit_delta_growth = max((growth_rate - (gro / 100)), 0.005 * rev)
    profit_delta_total = profit_delta_qdc + profit_delta_growth
    return [profit_delta_total, profit_delta_qdc, profit_delta_growth]

# Прорисовываем график

# Функция приложения
def show_predict_page():
    st.markdown('''<img src='https://www.kaizen.com/images/kaizen_logo.png' style="max-width: 30%;"><p>''', unsafe_allow_html=True)
    st.title("Определи свой потенциал")
    st.subheader('Нам необходима информация, чтобы спрогнозировать ваши показатели прибыли')

    industry = st.selectbox("Ваша отрасль:", industry_list)
    market_state = st.selectbox("Охарактеризуйте состояние сектора, в котором вы работаете:", gro_state_list)
    revenue = st.number_input("Какова ваша выручка, млн, руб. в год:", value=0)
    margin = st.slider("Какова ваша маржа операционной прибыли, % к выручке:", -20, 80, 0, 2)
    growth = st.slider("Каков ваш среднегодовой рост выручки в % за последние 3 года", -20, 100, 0, 5)

    ok = st.button("Определить прибыль")
    if ok:
        lost = lost_profit(industry, market_state, revenue, margin, growth)
        lost = pd.Series(lost).round(0)
        st.subheader(f"Предварительная оценка разницы в прибыли при сравнении с компаниями, реализующими Kaizen: {lost[0]:.0f} млн. руб.")
        st.markdown('Какой то текст{}'.format(lost[0]), unsafe_allow_html=True)
        st.subheader(f"в том числе:")
        st.subheader(f"Прибыль упущенная в операционной деятельности: {lost[1]:.0f} млн.руб.")
        st.subheader(f"Прибыль упущенная из-за отсутствия роста: {lost[2]:.0f} млн.руб.")
        def grafik():
            fig = go.Figure(go.Waterfall(name="20", orientation="v", measure=["absolute", "relative", "relative"],
                                         x=["Общая дельта", "Операционная дельта", "Дельта роста"],
                                         text=lost, y=[lost[0], -lost[1], -lost[2]],
                                         textposition="auto",
                                         connector={"line": {"color": "rgb(63, 63, 63)"}}))
            fig.update_layout(title = "Потери прибыли, млн. руб. в год")
            return fig
        graph = grafik()
        st.plotly_chart(graph, use_container_width=False, sharing="streamlit")

# Вызываем приложение
show_predict_page()
