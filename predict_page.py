

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

gsheetid = '1S7gJojFKedjSvSRM9npIDAzN_6mkSZhgEdGpNbxXnK0'
list_1 = 'sector_margin'
list_2 = 'growth_rate'
list_3 = 'deltas_breakdown'
list_4 = 'answer_score'

df_sector_margin_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_growth_rate_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)
deltas_breakdown_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_3)
answer_score_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_4)


df_sector_margin = pd.read_csv(df_sector_margin_csv)
df_growth_rate = pd.read_csv(df_growth_rate_csv)
df_deltas_breakdown = pd.read_csv(deltas_breakdown_csv)
df_answer_score = pd.read_csv(answer_score_csv)


df_growth_rate.set_index('growth_state', inplace=True)
df_sector_margin.set_index('sector', inplace=True)
df_deltas_breakdown.set_index('answer', inplace=True)
df_answer_score.set_index('answer_id', inplace=True)

df_sector_margin = pd.Series(df_sector_margin['margin'])
df_growth_rate = pd.Series(df_growth_rate['growth_rate'])
df_deltas_breakdown = pd.Series(df_deltas_breakdown['question_score'])

gro_state_list = df_growth_rate.index
industry_list = df_sector_margin.index
answers_list = df_answer_score['answer']

# Функция прибыли
def lost_profit(ind, mar, rev, marg, gro):
    growth_rate = df_growth_rate[mar]
    margin_ind_rate = df_sector_margin[ind]
    potencial_profit = rev * (margin_ind_rate)
    act_profit = (marg / 100) * rev
    profit_delta_qdc = max(potencial_profit - act_profit, 0.05 * act_profit)
    profit_delta_growth = max(((growth_rate - (gro / 100)) * rev * margin_ind_rate), 0.005 * rev)
    profit_delta_total = profit_delta_qdc + profit_delta_growth
    return [profit_delta_total, profit_delta_qdc, profit_delta_growth]
   

# Функция приложения
def show_predict_page():
    st.sidebar.markdown('''<img src='https://www.kaizen.com/images/kaizen_logo.png' style="max-width: 30%;"><p>''', unsafe_allow_html=True)
    st.sidebar.title("Определи свой потенциал")
    st.sidebar.subheader('Нам необходима информация, чтобы спрогнозировать ваши показатели прибыли')

    industry = st.sidebar.selectbox("Ваша отрасль:", industry_list)
    market_state = st.sidebar.selectbox("Охарактеризуйте состояние сектора, в котором вы работаете:", gro_state_list)
    revenue = st.sidebar.number_input("Какова ваша выручка, млн, руб. в год:", value=0)
    margin = st.sidebar.slider("Какова ваша маржа операционной прибыли, % к выручке:", -20, 80, 0, 2)
    growth = st.sidebar.slider("Каков ваш среднегодовой рост выручки в % за последние 3 года", -20, 100, 0, 5)
    lost = lost_profit(industry, market_state, revenue, margin, growth)
    lost = pd.Series(lost).round(0)
    st.title("Результат")
    st.markdown(f'Предварительная оценка разницы в прибыли при сравнении с компаниями, реализующими Kaizen: <b>{lost[0]:.0f}</b> млн. руб. <p> в том числе: <p>Операционная Дельта (прибыль упущенная в операционной деятельности): <b>{lost[1]:.0f}</b> млн. руб.<p> Дельта Роста (прибыль упущенная из-за отсутствия роста): <b>{lost[2]:.0f}</b> млн. руб.', unsafe_allow_html=True)
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
    st.title("Оцените следующие аспекты вашей компании:")
    anw_0 = st.radio(df_deltas_breakdown.index[0], list(answers_list), index=0)
    st.markdown(anw_0)
        


# Вызываем приложение
show_predict_page()
