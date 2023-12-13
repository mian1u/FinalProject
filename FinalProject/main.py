import streamlit as st
import pandas as pd
import plotly.express as px



StudentAssessment = pd.read_csv("data/studentAssessment.csv")
StudentInfo = pd.read_csv("data/studentInfo.csv")

st.title('Welcome to the analytics board of University')

joinedDataset = StudentInfo.merge(StudentAssessment, on=["id_student"], how="left")
joinedDataset=joinedDataset.dropna(subset=["imd_band", "score"])


joinedDataset['score'] = pd.to_numeric(joinedDataset['score'], errors='coerce')

# Sort the values
joinedDataset.sort_values(by='code_presentation', inplace=True)


grouped = joinedDataset.groupby(['code_module', 'code_presentation'])['score'].mean().reset_index()

# Now plot with Plotly Express
fig = px.line(grouped, x='code_presentation', y='score', color='code_module',
              title='Score Trends of Modules Over Time',
              markers=False)

question = st.sidebar.selectbox(
    "Select a Question",
    ('General Trend', "What is the percentage of the students whose score is higher than 40 in different typical loads?","How many pass in each module?", "What is the distribution rate of different activity type in each module?")
)
if question == "General Trend":
    st.plotly_chart(fig)

elif question == "What is the percentage of the students whose score is higher than 40 in different typical loads?":
    st.header("What is the percentage of the students whose score is higher than 40 in different typical loads?")

    joinedDataset = StudentInfo.merge(StudentAssessment, on=["id_student"], how="left")

    joinedDataset=joinedDataset.dropna(subset=["imd_band", "score"])
    joinedDataset = joinedDataset[joinedDataset["score"] >= 40]

    columns_exclude = ["code_module", "code_presentation", "imd_band", "num_of_prev_attempts", "studied_credits", "final_result", "id_assessment", "is_banked", "score","id_student", "date_submitted"]
    joinedDataset.drop(columns_exclude, axis=1, inplace=True)
    rename_dict = {"gender": "Gender", "region": "Region", "high_education": "Education Level", "age_band": "Age Range", "disability":"Ability Status"}
    joinedDataset.rename(columns=rename_dict, inplace=True)
    modified_column_names = joinedDataset.columns.tolist()

    load_option = st.sidebar.selectbox("Select student load", options=["Region", "Gender", "Ability Status", "Education Level","Age Range"])

    region_counts = joinedDataset['Region']. value_counts().reset_index()
    region_counts.columns = ['Region', 'Counts']

    age_counts = joinedDataset["Age Range"]. value_counts().reset_index()
    age_counts.columns = ["Age Range", "Counts"]

    gender_counts =joinedDataset["Gender"]. value_counts().reset_index()
    gender_counts.columns = ["Gender", "Counts"]

    disability_count =joinedDataset["Ability Status"]. value_counts().reset_index()
    disability_count.columns = ["Ability Status", "Counts"]

    highest_education_counts = (joinedDataset.groupby("highest_education"). size().reset_index(name="EdCounts"))

    if load_option == "Gender":
        fig = px.pie(gender_counts, values="Counts", names="Gender",
                title= "The percentage of the gender of students whose score is higher than 40")
        st.plotly_chart(fig)
    elif load_option == "Region":
        fig2 = px.bar(region_counts, x="Region", y="Counts",
                title= "The percentage of the region of students whose score is higher than 40")
        st.plotly_chart(fig2)
    elif load_option == "Age Range":
        fig3 = px.bar(age_counts, x="Age Range", y="Counts",
                title= "The percentage of age band of students whose score is higher than 40")
        st.plotly_chart(fig3)
    elif load_option == "Ability Status":
        fig4 = px.pie(disability_count, values="Counts", names="Ability Status",
                title= "The percentage of the disability of students whose score is higher than 40")
        st.plotly_chart(fig4)
    else:
        fig5 = px.bar(highest_education_counts, x="highest_education", y="EdCounts",
                title= "The percentage of the highest education of students whose score is higher than 40")
        st.plotly_chart(fig5)

elif question == "How many pass in each module?":
    st.header("How many pass in each module?")
    StudentInfoDataset = StudentInfo.dropna(subset=["imd_band"])


    # filter-module
    module_option = st.sidebar.selectbox("Select module", options=StudentInfoDataset["code_module"].unique().tolist())
    Semester_option = st.sidebar.radio("Select term", StudentInfoDataset["code_presentation"].unique())
    filtered_data = StudentInfoDataset[(StudentInfoDataset['code_presentation'] == Semester_option) & (
                StudentInfoDataset['code_module'] == module_option)]


    if module_option == "AAA":

        categories_to_drop = ["BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig)

    elif module_option == "BBB":
        categories_to_drop = ["AAA", "CCC", "DDD", "EEE", "FFF", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig2 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig2)

    elif module_option == "CCC":
        categories_to_drop = ["AAA", "BBB", "DDD", "EEE", "FFF", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig3 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig3)

    elif module_option == "DDD":
        categories_to_drop = ["AAA", "CCC", "BBB", "EEE", "FFF", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig4 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig4)

    elif module_option == "EEE":
        categories_to_drop = ["AAA", "CCC", "DDD", "BBB", "FFF", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig5 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig5)

    elif module_option == "FFF":

        categories_to_drop = ["AAA", "CCC", "DDD", "EEE", "BBB", "GGG"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig6 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig6)

    else:
        categories_to_drop = ["AAA", "CCC", "DDD", "EEE", "FFF", "BBB"]
        StudentInfoDataset = StudentInfoDataset[~StudentInfoDataset["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('final_result').size().reset_index(name='count')
        fig7 = px.bar(grouped_data, x='final_result', y='count')
        st.plotly_chart(fig7)

else:
    st.header("What is the distribution rate of different activity type in each module?")

    df = pd.read_csv("data/vle.csv")


    # filter
    module_option = st.sidebar.selectbox("Select module", options=df["code_module"].unique().tolist())
    Semester_option = st.sidebar.radio("Select term", df["code_presentation"].unique())
    filtered_data = df[(df['code_presentation'] == Semester_option) & (df['code_module'] == module_option)]

    if module_option == "AAA":
        categories_to_drop = ["BBB", "CCC", "DDD", "EEE", "FFF", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig)

    elif module_option == "BBB":
        categories_to_drop = ["AAA", "CCC", "DDD", "EEE", "FFF", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig2 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig2)
    elif module_option == "CCC":
        categories_to_drop = ["AAA", "BBB", "DDD", "EEE", "FFF", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig3 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig3)
    elif module_option == "DDD":
        categories_to_drop = ["AAA", "BBB", "CCC", "EEE", "FFF", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig3 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig4)
    elif module_option == "EEE":
        categories_to_drop = ["AAA", "BBB", "DDD", "CCC", "FFF", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig5 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig5)
    elif module_option == "FFF":
        categories_to_drop = ["AAA", "BBB", "DDD", "EEE", "CCC", "GGG"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig6 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig6)
    else:
        categories_to_drop = ["AAA", "BBB", "DDD", "EEE", "FFF", "CCC"]
        df = df[~df["code_module"].isin(categories_to_drop)]
        grouped_data = filtered_data.groupby('activity_type').size().reset_index(name='count')
        fig7 = px.bar(grouped_data, x='activity_type', y='count')
        st.plotly_chart(fig7)





