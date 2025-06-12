import streamlit as st
import pandas as pd  

df = pd.read_csv(r"./Input_Sales_Data_v2.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce') 
agg_df = df.groupby(['Date', 'Manufacturer']).agg({'Volume': 'sum', 
                                                   'Value': 'sum'}
                                                  ).reset_index()


def slide_change():
    filtered_Df = agg_df[(agg_df['Date'] >= st.session_state.dateslider[0]) & 
                         (agg_df['Date'] <= st.session_state.dateslider[1])]
    
    top5 = filtered_Df.groupby(['Manufacturer'])[['Volume']].sum().sort_values(
        by='Volume', 
        ascending=False).head(5).reset_index()['Manufacturer'].to_list()
    
    return filtered_Df, top5


date_Sldier = st.slider(label='date_range', 
                        min_value=df['Date'].min().to_pydatetime(),
                        max_value=df['Date'].max().to_pydatetime(),
                        value=(df['Date'].min().to_pydatetime(),
                               df['Date'].max().to_pydatetime()),
                        key="dateslider",
                        on_change=slide_change
                        )

display_df, top5 = slide_change()
st.dataframe(display_df)
st.line_chart(display_df[display_df['Manufacturer'].isin(top5)], 
              x="Date", y="Volume", color="Manufacturer")