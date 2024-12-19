import streamlit as st
from models.task import Task, Step
from models.scheduler import TaskScheduler
import pandas as pd
import plotly.express as px


def main():
    st.title("多任务时间分配工具")

    st.header("设置总体目标")
    overall_goal = st.text_input("请输入您的总体目标")

    tasks = []

    # 动态添加任务
    num_tasks = st.number_input("任务数量", min_value=1, value=1)

    for i in range(num_tasks):
        st.subheader(f"任务 {i + 1}")
        task_name = st.text_input(f"任务{i + 1}名称", key=f"task_{i}")

        steps = []
        num_steps = st.number_input(f"任务{i + 1}的步骤数量",
                                    min_value=1,
                                    value=1,
                                    key=f"steps_{i}")

        for j in range(num_steps):
            st.markdown(f"##### 步骤 {j + 1}")
            col1, col2, col3 = st.columns(3)

            with col1:
                step_name = st.text_input("步骤名称",
                                          key=f"step_name_{i}_{j}")
            with col2:
                duration = st.number_input("所需时间（分钟）",
                                           min_value=1,
                                           value=10,
                                           key=f"duration_{i}_{j}")
            with col3:
                needs_focus = st.checkbox("需要专注",
                                          key=f"focus_{i}_{j}")

            steps.append(Step(step_name, duration, needs_focus))

        tasks.append(Task(task_name, steps))

    if st.button("生成时间安排"):
        scheduler = TaskScheduler()
        for task in tasks:
            scheduler.add_task(task)

        timeline = scheduler.schedule()

        st.header("时间安排")

        # 创建表格数据
        table_data = []
        total_time = 0
        group_counter = 1

        for slot in timeline:
            start_time = slot['start_time']
            duration = slot['duration']
            end_time = start_time + duration
            total_time = end_time

            if slot['needs_focus']:
                # 串行任务：每个任务单独一行
                for task_name, step_name in slot['tasks']:
                    table_data.append({
                        "并行组": "",
                        "时间": f"{start_time} - {end_time}分钟",
                        "任务名称": f"{task_name}的{step_name}"
                    })
            else:
                # 并行任务：分别显示但标记同一组
                for task_name, step_name in slot['tasks']:
                    table_data.append({
                        "并行组": f"组{group_counter}",
                        "时间": f"{start_time} - {end_time}分钟",
                        "任务名称": f"{task_name}的{step_name}"
                    })
                group_counter += 1

        # 转换为 DataFrame
        df = pd.DataFrame(table_data)

        # 使用 Streamlit 显示表格，添加颜色
        def color_group(val):
            color = 'background-color: #e0f7fa' if val.startswith('组') else ''
            return color

        st.dataframe(
            df.style.applymap(color_group, subset=['并行组']),
            column_config={
                "并行组": st.column_config.TextColumn("并行组", width=80),
                "时间": st.column_config.TextColumn("时间", width=150),
                "任务名称": st.column_config.TextColumn("任务名称", width=300),
            },
            hide_index=True,
        )

        # 显示总用时
        st.info(f"总计用时：{total_time}分钟")

if __name__ == "__main__":
    main()