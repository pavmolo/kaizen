import streamlit as st
import numpy as np
import pandas as pd

gsheetid = '1S7gJojFKedjSvSRM9npIDAzN_6mkSZhgEdGpNbxXnK0'
list_1 = 'sector_margin'
list_2 = 'growth_rate'

df_sector_margin_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_1)
df_growth_rate_csv = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(gsheetid, list_2)

df_sector_margin = pd.read_csv(df_sector_margin_csv)
df_growth_rate = pd.read_csv(df_growth_rate_csv)
df_growth_rate.set_index('growth_state', inplace=True)
df_sector_margin.set_index('sector', inplace=True)

gro_state_list = df_growth_rate.index
industry_list = df_sector_margin.index


def lost_profit(ind, mar, rev, marg, gro):
    growth_rate = gro_state[mar]
    margin_ind_rate = sector_av_ebitda_margin_table[ind]
    potencial_profit = rev * (margin_ind_rate / 100)
    act_profit = (marg / 100) * rev
    profit_delta_qdc = max(potencial_profit - act_profit, 0)
    profit_delta_growth = max((growth_rate - gro / 100) * rev * (margin_ind_rate / 100), 0)
    profit_delta_total = max(profit_delta_qdc + profit_delta_growth, 0)
    return [profit_delta_total, profit_delta_qdc, profit_delta_growth]

def show_predict_page():
    st.title("Определеи свой потенциал")

    st.write("""### Нам необходима информация, чтобы спрогнозировать ваши показатели прибыли""")

    industry = st.selectbox("Ваша отрасль:", industry_list)
    market_state = st.selectbox("Охарактеризуйте состояние сектора, в котором вы работаете:", gro_state_list)
    revenue = st.number_input("Какова ваша выручка, млн, руб. в год:", value='int')
    margin = st.number_input("Какова ваша маржа операционной прибыли, % к выручке:")
    growth = st.slider("Каков ваш среднегодовой рост выручки в % за последние 3 года", -20, 100, 2)

    ok = st.button("Определить прибыль")
    if ok:
        lost = lost_profit(industry, market_state, revenue, margin, growth)
        st.subheader(f"Предварительная оценка разницы в прибыли при сравнении с компаниями мирового класса: {lost[0]:.2f} млн. руб.")
        st.subheader(f"в том числе:")
        st.subheader(f"Прибыль упущенная в операционной деятельности: {lost[1]:.2f} млн.руб.")
        st.subheader(f"Прибыль упущенная из-за отсутствия роста: {lost[2]:.2f} млн.руб.")
show_predict_page()
