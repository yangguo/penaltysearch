import pandas as pd
import glob
import plotly.express as px

import streamlit as st

penpayment = 'penalty/payment'
mapfolder = 'penalty/citygeo.csv'

@st.cache
def get_csvdf(penfolder):
    files2 = glob.glob(penfolder+'**/*.csv', recursive=True)
    dflist = []
    for filepath in files2:
        pendf = pd.read_csv(filepath)
        dflist.append(pendf)
    alldf = pd.concat(dflist, axis=0)
    return alldf


def get_penaltyval():
    penfolder = penpayment
    pendf = get_csvdf(penfolder)
    return pendf


def get_pendetail(process_list, city_choice):
    penfolder = penpayment
    pendf = get_csvdf(penfolder)

    if process_list == []:
        selectdf = pendf[(pendf['处罚地域'].isin(city_choice))]
    elif city_choice == []:
        selectdf = pendf[(pendf['三级流程'].isin(process_list))]
    else:
        selectdf = pendf[(pendf['三级流程'].isin(process_list)) &
                         (pendf['处罚地域'].isin(city_choice))]
    return selectdf


def do_plot_penalty(eventdb):
    pltnum = eventdb.groupby(['处罚地域', '三级流程']).size().reset_index(name='处罚数量')

    fig = px.bar(pltnum, x='处罚地域', y='处罚数量', color='三级流程', title='处罚数量统计')

    st.plotly_chart(fig)

    citydf = pd.read_csv(mapfolder)
    pat = "|".join(pltnum.处罚地域)
    citydf.insert(0, 'match', citydf['name'].str.extract(
        "(" + pat + ')', expand=False))

    subcitydf = citydf[citydf['match'].notnull()]
    geodf = pd.merge(subcitydf, pltnum, left_on='match', right_on='处罚地域')

    fig = px.scatter_mapbox(
        geodf, lat='lat', lon='lot',
        size="处罚数量", size_max=20,
        color="三级流程",
        color_continuous_scale=px.colors.sequential.Pinkyl,
        center={"lat": 35, "lon": 110},
        hover_name="name",
        mapbox_style="open-street-map",
        title='处罚地图',
        zoom=2
    )
    st.plotly_chart(fig)


def searchEvent(df, company_text, rule_text, amount_text):
    df.loc[~df['处罚金额（万元）（如适用）'].str.isnumeric(), ['处罚金额（万元）（如适用）']] = '0'
    searchdf = df[(df['处罚企业名称'].str.contains(company_text)) &
                  (df['相关法规（如适用）'].str.contains(rule_text)) &
                  (df['处罚金额（万元）（如适用）'].astype(float) >= float(amount_text))]
    sampledf = searchdf[['一级流程', '二级流程','三级流程', '处罚企业名称', '事件描述',
                         '相关法规（如适用）', '处罚金额（万元）（如适用）', '处罚地域']].sort_values(by='处罚地域')

    return sampledf
