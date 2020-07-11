import os
import base64
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st


def main():
    st.title('Shopify Product Images')
    
    url = st.text_input('Input website:', '')

    if url:
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            url += '/products.json?limit=500' if url[-1] != '/' else 'products.json?limit=500'
            df = pd.read_json(url)
        except:
            df = None
            

        if df is None:
            st.warning('Please check the input website is valid.')
        else:
            df = df['products'].apply(pd.Series)
            if st.checkbox('Show raw data'):
                st.write(df)

            products = st.multiselect('Display products', ['ALL'] + list(df['title'].unique()))
            if products:
                if 'ALL' in products:
                    selected = df
                else:
                    selected = df.loc[df.title.isin(products)]
                
                with st.spinner('Loading plots...'):
                    for i in selected.index:
                        st.subheader(df.iloc[i].title)
                        for img in df.iloc[i].images:
                            st.image(img['src'], use_column_width=True)
                        st.markdown('---')



    # Hide footer
    hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    """
    # Hide hamburger menu
    st.markdown(hide_footer_style, unsafe_allow_html=True)
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
