import os
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

load_dotenv()

# DB connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="fitness_tracker"
    )

st.title(" Fitness Tracker Dashboard")

# -------- ADD WORKOUT --------
st.header("Add Workout")

with st.form("workout_form"):
    workout_date = st.date_input("Workout Date")
    exercise_type = st.text_input("Exercise Type")
    duration_minutes = st.number_input("Duration (minutes)", min_value=0)
    calories_burned = st.number_input("Calories Burned", min_value=0)

    submit = st.form_submit_button("Add Workout")

    if submit:
        try:
            connection = get_connection()
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO workouts (workout_date, exercise_type, duration_minutes, calories_burned)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                workout_date,
                exercise_type,
                duration_minutes,
                calories_burned
            ))

            connection.commit()
            st.success("Workout added successfully!")

        except mysql.connector.Error as error:
            st.error(f"Error: {error}")

        finally:
            cursor.close()
            connection.close()


# -------- VIEW DATA --------
st.header("Workout Data")

try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM workouts")
    records = cursor.fetchall()

    columns = ['id', 'workout_date', 'exercise_type', 'duration_minutes', 'calories_burned']
    df = pd.DataFrame(records, columns=columns)

    if not df.empty:
        st.dataframe(df)

        # Stats
        st.subheader("Statistics")
        st.write("Total Workouts:", len(df))
        st.write("Total Calories:", df['calories_burned'].sum())
        st.write("Average Duration:", df['duration_minutes'].mean())

        # Chart
        df['workout_date'] = pd.to_datetime(df['workout_date'])

        df_daily = df.groupby('workout_date').agg({
            'calories_burned': 'sum'
        }).reset_index()

        st.subheader(" Daily Calorie Trends")

        fig, ax = plt.subplots()
        ax.plot(df_daily['workout_date'], df_daily['calories_burned'], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories")
        ax.set_title("Daily Calories Burned")

        st.pyplot(fig)

    else:
        st.info("No data available")

except mysql.connector.Error as error:
    st.error(f"Error: {error}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()