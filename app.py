import streamlit as st


from dbpayment import get_penaltyval,do_plot_penalty,searchEvent,get_pendetail

def main():

    st.subheader("支付行业处罚分析")
    # upload excel file
    plt_val = get_penaltyval()
    plt_list = plt_val['三级流程'].drop_duplicates().tolist()
    make_choice = st.sidebar.multiselect('选择三级流程:', plt_list)
    if make_choice == []:
        make_choice = plt_list

    city_list = plt_val[plt_val['三级流程'].isin(
        make_choice)]['处罚地域'].drop_duplicates().tolist()

    city_choice = st.sidebar.multiselect('选择地域:', city_list)

    company_text = st.sidebar.text_input('搜索企业关键词')
    rule_text = st.sidebar.text_input('搜索法规关键词')
    amount_text = st.sidebar.text_input('处罚金额大于等于（万元）', 0)
    if not amount_text.isnumeric():
        amount_text = 0

    # if make_choice != []:
    # st.subheader("详细案例")
    # if make_choice and city_choice:
    if make_choice or city_choice:
        df = get_pendetail(make_choice, city_choice)
        # st.write(df)
        do_plot_penalty(df)
        # st.dataframe(df)
        st.write("详细案例")
        sampledf = searchEvent(df, company_text, rule_text,
                                amount_text)

        st.table(sampledf)


if __name__ == '__main__':
    main()