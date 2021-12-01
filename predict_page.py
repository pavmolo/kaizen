import streamlit as st
import numpy as np
import pandas as np

sector_av_ebitda_margin_table = {'Consumer Discretionary': 22.216970460607886, 'Consumer Staples': 23.146861043187315, 'Energy': 38.69977063208259,
                                 'Financials': 41.085547708295664, 'Health Care': 29.385876126208842, 'Industrials': 22.38041537508514,
                                 'Information Technology': 32.313896822280405, 'Materials': 23.230850464225615,
                                 'Real Estate': 76.070948087517, 'Telecommunication Services': 37.41939100247284, 'Utilities': 44.15140491944504}

gro_state = {'Много небольших участников на конкурентом рынке': 0.3,
            'В моем секторе есть крупные игроки, в число которых я не вхожу': 0.5,
            'В моем секторе есть крупные игроки, в том числе я': 0.2,
            'Я монополист': 0.05}
gro_state_list = list(gro_state.keys())
industry_list = list(sector_av_ebitda_margin_table.keys())


def lost_profit(ind, mar, rev, marg, gro):
    growth_rate = gro_state[mar]
    margin_ind_rate = sector_av_ebitda_margin_table[ind]
    potencial_profit = rev * (margin_ind_rate / 100)
    act_profit = (marg / 100) * rev
    profit_delta_qdc = potencial_profit - act_profit
    profit_delta_growth = (growth_rate - gro) * rev
    profit_delta_total = profit_delta_qdc + profit_delta_qdc
    return [profit_delta_total, profit_delta_qdc, profit_delta_growth]

def show_predict_page():
    st.title("Определеи свой потенциал")

    st.write("""### Нам необходима информация, чтобы спрогнозировать ваши показатели прибыли""")

    industry = st.selectbox("Ваша отрасль:", industry_list)
    market_state = st.selectbox("Охарактеризуйте состояние сектора, в котором вы работаете:", gro_state_list)
    revenue = st.number_input("Какова ваша выручка, млн, руб. в год:")
    margin = st.number_input("Какова ваша маржа операционной прибыли, % к выручке:")
    growth = st.slider("Каков ваш среднегодовой рост выручки в % за последние 3 года", -20, 100, 2)

    ok = st.button("Определить прибыль")
    if ok:
        lost = lost_profit(industry, market_state, revenue, margin, growth)
        st.subheader(f"Предварительная оценка разницы в прибыли при сравнении с компаниями мирового класса: {lost[0]:.2f} млн. руб.")
        st.subheader(f"в том числе:")
        st.subheader(f"Прибыль упущенная в операционной деятельности: {lost[1]:.2f} млн.руб.")
        st.subheader(f"Прибыль упущенная из-за отсутствия роста: {lost[2]:.2f} млн.руб.")
