import pandas as pd
import streamlit as st


def main():
    st.beta_set_page_config(
        page_title = 'SPI',
        page_icon = '🔍',
    )
    
    st.title('Shopify Product Images')
    
    url = st.text_input('Website URL:', '')

    if url:
        try:
            if not url.startswith('http'):
                url = 'https://' + url
            if not url.endswith('/'):
                url += '/'
            json_url = url + 'products.json?limit=500'
            df = pd.read_json(json_url)
        except:
            df = None
            

        if df is None:
            st.warning('Please check the input website url is valid.')
        else:
            st.markdown(f'Data source: <a href="{json_url}">{json_url[:-10]}</a>', unsafe_allow_html=True)
            df = df['products'].apply(pd.Series)
            if st.checkbox('Show raw data'):
                st.write(df)

            products = st.multiselect('Display Products', ['ALL'] + list(df['title'].unique()))
            if products:
                if 'ALL' in products:
                    selected = df.copy()
                else:
                    selected = df.loc[df.title.isin(products)]
                
                with st.spinner('Loading images...'):
                    for i in selected.index:
                        st.subheader(df.iloc[i].title)
                        st.write(f'{url}products/{df.iloc[i].handle}')
                        try:
                            price = df.iloc[i]['variants'][0]['price']
                        except:
                            price = None
                        if price is not None:
                            st.write(f'Price: ${price}')
                        st.write(df.iloc[i]['body_html'], unsafe_allow_html=True)
                        for img in df.iloc[i].images:
                            st.image(img['src'], use_column_width=True)
                        st.markdown('---')

                if st.checkbox('Show Image Links'):
                    for i in selected.index:
                        st.subheader(df.iloc[i].title)
                        for j, img in enumerate(df.iloc[i].images):
                            st.write(img['src'])
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
