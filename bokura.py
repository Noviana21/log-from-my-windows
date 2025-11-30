import streamlit as st
import pandas as pd
import os

st.title("Analisis Log Game (BOKURA)")
# harusnya Log Game Analysis (BOKURA) hiks, biar konsisten english

# nama file log
nama_file_log = "Player.log"

if os.path.exists(nama_file_log):
    try:
        with open(nama_file_log, "r", encoding="utf-8") as f:
            lines = f.readlines()

        parsed_data = []

        for index, line in enumerate(lines):
            line = line.strip()

            if "Exception" in line or "Timeout" in line or "Failed" in line or "Disconnect" in line:
                parsed_data.append({
                    "Row": index,
                    "Category": "Network Error",
                    "Note": "Network Error"
                })
            
            elif "Jump!!!!!!!!!!!" in line:
                parsed_data.append({"Row": index, "Category": "Player Action", "Note": "Jump"})
                
            elif "interact" in line.lower() or "Button indicator" in line:
                parsed_data.append({"Row": index, "Category": "Player Action", "Note": "Interact"})
                
            elif "DOTWEEN" in line:
                parsed_data.append({"Row": index, "Category": "Warning", "Note": "Graphics Warning"})

        # dataframe
        if len(parsed_data) > 0:
            df = pd.DataFrame(parsed_data)

            st.subheader("Player Activity & Network Status")

            chart_data = df['Note'].value_counts()
            st.bar_chart(chart_data)

            st.subheader("Event Distribution")
            st.scatter_chart(
                df,
                x='Row',
                y='Category',
                color='Category',
                size=20
            )

            st.divider()

            st.subheader("Data log")
            st.dataframe(df.head(5), use_container_width=True) 

            col1, col2, col3, col4 = st.columns(4)
            
            total_jump = len(df[df['Note'] == 'Jump'])
            total_interact = len(df[df['Note'] == 'Interact'])
            total_error = len(df[df['Category'] == 'Network Error']) 
            total_warn = len(df[df['Category'] == 'Warning'])
            
            col1.metric("Jump Total", total_jump)
            col2.metric("Interact Total", total_interact)
            col3.metric("Network Error Total", total_error, delta_color="inverse") 
            col4.metric("Warning Total", total_warn)
        else:
            st.warning("No data.")

    except Exception as e:
        st.error(f"Cannot read file: {e}")

else:
    st.error(f"File '{nama_file_log}' not found!")