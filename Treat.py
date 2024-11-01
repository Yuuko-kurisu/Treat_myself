import streamlit as st
import pandas as pd
import json

# 主页名字

st.set_page_config(layout="wide")
st.markdown("# Main page —— Treatment 🎈")

with st.expander("奖励规则"):

    st.markdown("""
    **十次保底必须UR: 清除任意购物车一项!!!**
""")

# 



path_base_data = './data/treat.csv'
test_case = pd.read_csv(path_base_data)
# test_case_2 = pd.read_csv(path_base_data, sht='Sheet2')

path_base_data_json = './data/treat.json'
# 读取json文件
with open(path_base_data_json, 'r') as f:
    test_case_json = json.load(f)
    # print(test_case_json)
    # print(type(test_case_json))
    # print(test_case_json['score'])
    # print(test_case_json['remaining'])

# test_case_json = pd.read_json(path_base_data_json)
score_read = test_case_json['score']
remaining_read = test_case_json['remaining']
remaining = remaining_read



## 设置一个check box



# st.write("## 设置奖励值:")


scores = 0

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
# right_column.button('设置奖励值!')

with left_column:
    st.write("## 奖励项:")
    st.write(test_case)

with right_column:
    if 'button' not in st.session_state:
        st.session_state.button = False

    def click_button():
        st.session_state.button = not st.session_state.button

    st.button('设置奖励值', on_click=click_button)

    if st.session_state.button:
        # The message and nested widget will remain on the page
        # st.write('Button is on!')
        scores = st.slider('本次奖励分数', 1, 10)
    else:
        # st.write('Button is off!')
        pass
    is_add_init = st.checkbox("是否使用之前剩下的奖励分数")
    scores_init = score_read
    if is_add_init:
        scores = scores + scores_init
    # x = st.slider('x')
    # scores_init = st.s
    st.write("已有奖励分数为:", scores_init)

st.write('-'*50)

# 居中
# st.write("## 摇一摇🎲")

# st.button('摇一摇🎲')

# col1, col2, col3 = st.columns([1, 1, 1])
# with col2:
#     st.markdown(
#         """
#         <style>
#         .button {
#             width: 100%;
#             height: 50px;
#             font-size: 20px;
#             color: white;
#             background-color: #4CAF50; /* 绿色背景 */
#             border: none;
#             border-radius: 12px;
#             font-family: 'Arial', sans-serif;
#         }
#         .button:hover {
#             background-color: #45a049; /* 鼠标悬停时的颜色 */
#         }
#         .custom-text {
#             font-size: 24px;
#             color: #FF5733; /* 橙色字体 */
#             font-family: 'Courier New', monospace;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#     st.markdown('<div class="button"><button class="button">摇一摇🎲</button></div>', unsafe_allow_html=True)


# present = '市区放风'
# rate = 'SSR'
# st.write('结果🎁是:', present, "等级", rate)
# st.write("等级:", rate)
def get_present(test_case, scores, remaining, distribution='weight'):
    present = {
        '奖励': '继续学习',
        '等级': 'N'
    }
    if scores == 0:
        return present['奖励'], present['等级']

    if distribution == 'weight':
        # 把分值小于scores的过滤掉
        test_case = test_case[test_case['分值'] <= scores]
        test_case['weight'] = test_case['分值'] / test_case['分值'].sum()
        present_item = test_case.sample(1, weights=test_case['weight']).iloc[0]
        present['奖励'] = present_item['奖励项']
        present['等级'] = present_item['Rate']
        # present['等级'] = test_case[test_case['奖励'] == present['奖励']]['等级'].iloc[0]
        if remaining == 0:
            if scores >= 10:
                present['奖励'] = test_case[test_case['Rate'] == 'UR'].sample(1).iloc[0]['奖励项']
                present['等级'] = 'UR'
            else:
                present['奖励'] = '积分不够，奖励好好学习'
                present['等级'] = 'SSSR'
    return present['奖励'], present['等级']

# scores = 10
# present, rate = get_present(test_case, scores, remaining)
# scores = scores_init + scores - test_case[test_case['奖励项'] == present]['分值'].iloc[0]
# st.markdown(f'<div class="custom-text">结果🎁是: {present}</div>', unsafe_allow_html=True)
# st.markdown(f'<div class="custom-text">等级: {rate}</div>', unsafe_allow_html=True)

# 添加自定义CSS样式
st.markdown(
    """
    <style>
    .custom-shake-button {
        width: 100%;
        height: 50px;
        font-size: 25px;
        color: white;
        background-color: #4CAF50; /* 绿色背景 */
        border: none;
        border-radius: 12px;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 20px;
        color: white;
        background-color: #4CAF50; /* 绿色背景 */
        border: none;
        border-radius: 12px;
        font-family: 'Arial', sans-serif;
    }
    .custom-shake-button:hover {
        background-color: #45a059; /* 鼠标悬停时的颜色 */
    }
    .custom-text {
        font-size: 24px;
        color: #FF5733; /* 橙色字体 */
        font-family: 'Courier New', monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)



col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button('摇一摇🎲', key='shake_button'):
        present, rate = get_present(test_case, scores, remaining)
        # 保存为json文件
        with open('./data/present.json', 'w') as f:
            present_json = {
                'present': present,
                'rate': rate
            }
            json.dump(present_json, f)
            # json.dump(test_case_json, f)
        st.markdown(f'<div class="custom-text">结果🎁是: {present}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="custom-text">等级: {rate}</div>', unsafe_allow_html=True)
        # remaining = remaining - 1
        # st.write("离保底还有:", remaining ,"次")

# 使用自定义CSS样式美化按钮


st.write('-'*50)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
# right_column.button('设置奖励值!')

with left_column:
    # st.button('我想好了（更新数据）')
    ## 保存数据
    if st.button('我想好了（更新数据）'):
        # print('present:', present)
        with open('./data/present.json', 'r') as f:
            present_json = json.load(f)
            present = present_json['present']
            rate = present_json['rate']
        # st.write('scores:', scores)
        # st.write('scores_init:', scores_init)
        scores_use = test_case[test_case['奖励项'] == present]['分值'].iloc[0]
        # st.write('scores_use:', scores_use)
        scores = scores - scores_use
        scores = int(scores)
        remaining = remaining - 1
        if remaining == 0 or remaining < 0:
            remaining = 10

        test_case_json['score'] = scores
        test_case_json['remaining'] = remaining
        st.write(test_case_json)
        with open(path_base_data_json, 'w') as f:
            # json.dump(test_case_json, f)
            # 写入json文件
            json.dump(test_case_json, f)
        st.write("数据已更新")

with right_column:
    # if st.button('再摇一次'):
    #     present, rate = get_present(test_case, scores, remaining)
    #     st.markdown(f'<div class="custom-text">结果🎁是: {present}</div>', unsafe_allow_html=True)
    #     st.markdown(f'<div class="custom-text">等级: {rate}</div>', unsafe_allow_html=True)
    # remaining = remaining - 1
    st.write("离保底还有:", remaining ,"次")


# score 
# print(st.session_state.button)

add_selectbox = st.sidebar.selectbox(
    '选择概率分布?',
    ('均匀', '加权')
)

# Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )