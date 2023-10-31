import mysql.connector

def create_connection():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",database='research'
    )

def insert_data(data):
    mydb = create_connection()
    mycursor = mydb.cursor()
    if len(data['website'])>0:
        website = data['website'][0]
    else:
        website=""
    if len(data['state'])>0:
        state = data['state'][0]
    else:
        state = ""
    if len(data['pin_code'])>0:
        pin_code = data['pin_code'][0]
    else:
        pin_code = ""
    print(data['company_name'][0],data['card_holder'][0],data['designation'][0],data['mobile_number'][0],data['email'][0],website,data['area'][0],data['city'][0],state,pin_code)
    rec_tup = (0,data['company_name'][0],data['card_holder'][0],data['designation'][0],data['mobile_number'][0],data['email'][0],website,data['area'][0],data['city'][0],state,pin_code,data['image'][0],data['file_name'])
    print(type(rec_tup))
    print(rec_tup)
    insert_query = '''insert into biz_card_details values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    mycursor.execute(insert_query,rec_tup)   
    mydb.commit()
    mycursor.close()

def select_all_channels():
    mydb = create_connection()
    mycursor = mydb.cursor()
    query = "select id,company,contact_name,designation,mobile,email,website,area,city,state,pincode,filename from biz_card_details"
    mycursor.execute(query)   
    data = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    return data

def updateData(dataframe):
    print('Trying to update the Values in DB')
    print(dataframe['id'].values)
    mydb = create_connection()
    mycursor = mydb.cursor()
    dllist = []
    reclis = []
    for i in range(0,len(dataframe['id'].values)):
        id = dataframe['id'].values[i]
        name = dataframe['contact_name'].values[i]
        company = dataframe['company'].values[i]
        design = dataframe['designation'].values[i]
        area = dataframe['area'].values[i]
        city = dataframe['city'].values[i]
        state = dataframe['state'].values[i]
        pin = dataframe['pin_code'].values[i]
        fname = dataframe['image'].values[i]
        mobile = dataframe['mobile'].values[i]
        email = dataframe['email'].values[i]
        website = dataframe['website'].values[i]
        isDelete = dataframe['Delete?'].values[i]
        if isDelete:
            dllist.append(id)
        rec = (id,company,name,design,mobile,email,website,area,city,state,pin,fname)
        reclis.append(rec)
    if len(isDelete)>0:
        for i in dllist:
            mycursor.execute("delete from biz_card_details where id="+str(i))
            print('Record deleted successfully')
    for t in reclis:
        print("Now the name is ::: ",t[1])
        mycursor.execute("update biz_card_details set contact_name=%s,designation=%s, company=%s,  mobile=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pincode=%s,filename=%s where id=%s",(t[2],t[3],t[1],t[4],t[5],t[6],t[7],t[8],t[9],t[10],t[11],int(t[0])))
        print('Record updated successfully.')
    mydb.commit()
    mycursor.close()
    mydb.close()

