import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="EWF League Movement Analysis")

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

def prepare_movement_data(df):
    if df.empty:
        return pd.DataFrame()
    moves = df[df['season_outcome'] != 'No change'].copy()
    moves['season_year'] = moves['season'].str[:4]
    def movetype(x):
        if 'Promoted' in x:
            return 'Promotion'
        elif 'Relegated' in x:
            return 'Relegation'
        else:
            return 'Other'
    moves['movement_type'] = moves['season_outcome'].apply(movetype)
    return moves.groupby(['season_year', 'movement_type']).size().reset_index(name='count')

def create_chart(data):
    if data.empty:
        return None
    chart = alt.Chart(data).mark_bar().encode(
        x='season_year:O',
        y='count:Q',
        color='movement_type:N',
        tooltip=['season_year', 'movement_type', 'count']
    ).properties(title="Promotions and Relegations by Season")
    return chart

def main():
    st.title("EWF League Movement")
    st.write("This shows how many teams got promoted or relegated each season.")
    df = load_data('data/ewf_standings.csv')
    if not df.empty:
        plot_data = prepare_movement_data(df)
        chart = create_chart(plot_data)
        if chart:
            st.altair_chart(chart, use_container_width=True)
        st.write("Data Table:")
        st.dataframe(plot_data)

if __name__ == "__main__":
    main()