import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def fetch_data(address):
    url = f"https://api.multiversx.com/accounts/{address}/nfts?search=BEEF-032185"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Inside the 'if st.button('Fetch Data'):' block
address = st.text_input('Enter the Address:', '')

if st.button('Fetch Data'):
    if len(address) == 62:
        data = fetch_data(address)
        if data:
            body_groups = {}
            for item in data:
                body_value = next((attr['value'] for attr in item['metadata']['attributes'] if attr['trait_type'] == 'BODY'), None)
                if body_value:
                    if body_value not in body_groups:
                        body_groups[body_value] = {'count': 0, 'items': []}
                    body_groups[body_value]['count'] += 1
                    body_groups[body_value]['items'].append(item)

            # Create full-width columns for dropdowns
            for body_type, info in body_groups.items():
                with st.expander(f"{body_type} (Count: {info['count']})", expanded=False):
                    for item in info['items']:
                        # Adjust column widths here
                        img_col, data_col = st.columns([1, 3])  # Adjust the ratio as needed
                        with img_col:
                            response = requests.get(item['url'])
                            # response = requests.get(item['media'][0]['thumbnailUrl'])
                            if response.status_code == 200:
                                img = Image.open(BytesIO(response.content))
                                img.thumbnail((img.width // 5, img.height // 5))
                                st.image(img, use_column_width=True)
                        with data_col:
                            item_number = item['name'].split("#")[-1] if "#" in item['name'] else item['name']
                            st.write(f"BEEF: #{item_number}")
        else:
            st.error("Data not found or API error!")
    else:
        st.error("Invalid address length!")
