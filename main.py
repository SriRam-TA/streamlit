import streamlit as st
import pandas as pd 

st.sidebar.image("./logo.png")
col1, col2 = st.columns(2)


df = pd.read_csv(r"./Input_Sales_Data_v2.csv")
df['Date'] = pd.to_datetime(df['Date'], errors='coerce') 
agg_df = df.groupby(['Date', 'Manufacturer', 'Category']).agg({'Volume': 'sum',
                                                               'Value': 'sum'}
                                                              ).reset_index()


def slide_change():
    if st.session_state.drop_down == 'ALL':
        filtered_Df = agg_df[(agg_df['Date'] >= st.session_state.dateslider[0]
                              ) &
                             (agg_df['Date'] <= st.session_state.dateslider[1])
                             ]
    else:
        filtered_Df = agg_df[((agg_df['Date'] >= st.session_state.dateslider[0]
                               ) &
                             (agg_df['Date'] <= st.session_state.dateslider[1])
                              ) &
                             (agg_df['Category'] == st.session_state.drop_down)
                             ]
        
    display_df = filtered_Df.drop(columns='Category', axis=1)
    display_df = display_df.groupby(['Date', 'Manufacturer']).agg({
                                                              'Volume': 'sum',
                                                              'Value': 'sum'}
                                                              ).reset_index()
    
    top5 = display_df.groupby(['Manufacturer']
                              )[['Value']].sum().sort_values(
        by='Value', 
        ascending=False).head(5).reset_index()['Manufacturer'].to_list()
    
    return display_df, top5


with col1:    
    date_Sldier = st.slider(label='date_range', 
                            min_value=df['Date'].min().to_pydatetime(),
                            max_value=df['Date'].max().to_pydatetime(),
                            value=(df['Date'].min().to_pydatetime(),
                                   df['Date'].max().to_pydatetime()),
                            key="dateslider",
                            on_change=slide_change
                            )
       
with col2:
    cat_list = list(df['Category'].unique())
    cat_list.append('ALL')
    default_ix = cat_list.index('ALL')
    st.selectbox(
                    "Select the category",
                    cat_list,
                    key="drop_down",
                    index=default_ix
                )

display_df, top5 = slide_change()
final_display_df = display_df.groupby('Manufacturer').agg({
                                                            'Volume': 'sum',
                                                            'Value': 'sum'}
                                                          ).reset_index(
                                                          ).sort_values(
                                                              by='Value',
                                                              ascending=False
                                                          ).reset_index(
                                                              drop=True
                                                                        )
final_display_df['%'] = (final_display_df['Value'] / 
                         final_display_df['Value'].sum()) * 100


final_display_df['Value'] = final_display_df['Value'].apply(
    lambda x: f"{x:,.0f}")
final_display_df['Volume'] = final_display_df['Volume'].apply(
    lambda x: f"{x:,.2f}")

final_display_df = final_display_df.style.background_gradient(
                                                    subset=['%'],
                                                    cmap='Greens')


st.dataframe(final_display_df)
st.line_chart(display_df[display_df['Manufacturer'].isin(top5)], 
              x="Date", y="Volume", color="Manufacturer")