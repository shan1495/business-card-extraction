import cv2
import easyocr
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import base64
import utils.utility as util
import utils.mysqlutils as sqlutil
import matplotlib.pyplot as plt
from PIL import Image
import os

st.set_page_config(page_title="Login",layout="centered",page_icon=":business:")
hashed_passwords = stauth.Hasher(['test123']).generate()

def updateValues(df):
        print("update funciton called")
        if 'df_card_data' not in st.session_state:
            print(df)
            #st.session_state.df_card_data = df
        print(st.session_state.df_card_data)
        sqlutil.updateData(df)
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(credentials=
    config['credentials'],
    cookie_expiry_days=config['cookie']['expiry_days'],
    preauthorized=config['preauthorized'],
    cookie_name=config['cookie']['name'],key= config['cookie']['key']    
)
name, authentication_status, username = authenticator.login('Login', 'main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    st.markdown("## Welcome to Biz card extraction demo project")
    with st.sidebar:
        selected = st.selectbox("Select the what to do",("Home","Upload Image","View Details","Modify Details"))
    if selected == "Home":
         st.markdown("## :blue[Technologies used in this project are:]")
         st.markdown("1. Easy OCR\n2. MySQL\n3. CV2\n4. Streamlit")
         st.write("This project demonstrate how to \n1. Extract the texts from the images and store them into MySQL\n2. View the details using Streamlit\n. Modify the user details and update the same into database")
         
    if(selected == "Upload Image"):
            file = st.file_uploader(label="Select the Image to upload",label_visibility="visible")
            col1,col2 = st.columns([2,2],gap="large")            
            if file is not None:
                    bytes_data = file.getbuffer()
                    st.write("filename:", file.name)
                    f = open('./images/'+file.name,'wb')
                    f.write(bytes_data)
                    clicked = st.button("Extract & Save data")
                    f.close()
                    if clicked:
                         with st.spinner("Please wait we are extracting text from image..."):
                                st.set_option('deprecation.showPyplotGlobalUse', False)
                                reader = easyocr.Reader(['en'])
                                savedimg = './images/'+file.name
                                img = cv2.imread(savedimg)
                                result = reader.readtext(img)
                                for (coord, text, prob) in result:
                                    (topleft, topright, bottomright, bottomleft) = coord
                                    tx,ty = (int(topleft[0]), int(topleft[1]))
                                    bx,by = (int(bottomright[0]), int(bottomright[1]))
                                    cv2.rectangle(img, (tx,ty), (bx,by), (0, 0, 255), 2)
                                    text = util.cleanup_text(text)
                                    cv2.putText(img,text,(int(topleft[0]), int(topleft[1])-10), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(128,255,64))
                         textdata = util.recognizeText(result,savedimg)  
                         #print(textdata)      
                         st.image(img)
                         btn = st.button(label="Upload Image")
                         if btn:
                            print('clicked')
                         else:
                              print('not clicked')      
    if selected == "View Details":
         st.markdown("## :green[Business Contact list]")
         records = sqlutil.select_all_channels()
         #print("Now the records from DB ", records)
                  
         df = pd.DataFrame(records,columns=['id','company','contact_name','designation','mobile','email','website','area','city','state','pin_code','image'])
            #fs2.write(tup[-1])
         df['Preview?'] = '' 
         df['Delete?']=''
         if 'df_card_data' not in st.session_state:
            st.session_state.df_company_data = df
            
         edited_df = st.data_editor(df, key="editor", num_rows='dynamic',
                                    column_config={
                                         "ID": st.column_config.NumberColumn("ID"),
                                        #"image": st.column_config.ImageColumn("Image", width='large'),
                                        "Name":st.column_config.TextColumn("Contact Name"),
                                        "Company":st.column_config.TextColumn("Company"),
                                        "Area":st.column_config.TextColumn("Area"),
                                        "City":st.column_config.TextColumn("City"),
                                        "State":st.column_config.TextColumn("State"),
                                        "Pin code":st.column_config.TextColumn("Pin code"),
                                        "Image": st.column_config.LinkColumn("Image", width="large"),
                                        "Preview?":st.column_config.CheckboxColumn("View Card"),
                                        "Delete?":st.column_config.CheckboxColumn("Delete Card")
                                         }, hide_index=True)
         if edited_df is not None:
              print("editor state changed........")
              st.session_state["df_card_data"] = edited_df
              #print("ACTION------>>",edited_df['Action'].values[0])
              if edited_df['Preview?'].values is not None:
                   print('Need to show the umage')
                   #img = Image.open()
                   #print('you selected to view ', edited_df['image'].values)
                   selectedIndex = edited_df["Preview?"].index
                   #print("The selected index is :: ", selectedIndex)
                   #print(edited_df['image'].values[0])
                   
                   #i = 0
                   for ind, is_selected in enumerate(edited_df['Preview?'].values):
                        print("iterating the actions", ind, is_selected)
                        if is_selected:
                             print("is selected is ", is_selected)
                             imagepath = edited_df['image'].values[ind]
                             img = cv2.imread(imagepath)
                             #st.image(img)
                             #imgpath = edited_df['image'].values[i-1]
                   
                             cv2.imshow('image', img)
                             cv2.waitKey(0)
                             cv2.destroyAllWindows()
                        
                   
                   
              updateValues(edited_df)


    