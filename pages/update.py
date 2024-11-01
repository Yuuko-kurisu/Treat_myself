import streamlit as st
import pandas as pd


# 主页名字

import streamlit as st
import pandas as pd

# 主页名字
st.set_page_config(layout="wide")
st.markdown("# 编辑奖励项")

# 文件路径
path_base_data = './data/treat.csv'

# 读取数据
test_case = pd.read_csv(path_base_data)

# 显示可编辑的 DataFrame
edited_df = st.data_editor(test_case, num_rows="dynamic")

# 保存按钮
if st.button('保存更改'):
    try:
        # 将编辑后的 DataFrame 保存回 CSV 文件
        edited_df.to_csv(path_base_data, index=False)
        st.success("数据已成功保存")
    except Exception as e:
        st.error(f"保存数据时出错: {e}")

# 显示编辑后的 DataFrame
st.write(edited_df)