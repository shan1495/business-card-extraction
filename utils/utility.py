import easyocr
import re
import cv2
import utils.mysqlutils as sqlutil

def recognizeText(res,image):
    print('parsing text..........')
    processedIndexs = []
    data = {"company_name" : [],
                "card_holder" : [],
                "designation" : [],
                "mobile_number" :[],                
                "email" : [],
                "website" : [],
                "area" : [],
                "city" : [],
                "state" : [],
                "pin_code" : [],
                "file_name":image,
                "image" : img_to_binary(image)
                

               }
    for ind,i in enumerate(res):
        # To get WEBSITE_URL
                print("Now text--------------------->>"+i[1])
                if "www " in i[1].lower() or "www." in i[1].lower():
                    #print("matchhhhhhhhhh small"+i[1])
                    data["website"].append(i[1])
                elif "WWW " in i[1] or "WWW" in i[1]:
                    #print("MATTTTTTTTTTTTTTTTT capital"+i[1])
                    data["website"].append(res[4][1]+"."+res[5][1])
                    print("Now the website iss ::: " + "www."+res[4][1]+"."+res[5][1]) 

                
                # To get EMAIL ID
                elif "@" in i[1]:
                    data["email"].append(i[1])

                # To get MOBILE NUMBER
                elif "-" in i[1]:
                    data["mobile_number"].append(i[1])
                    if len(data["mobile_number"]) ==2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get COMPANY NAME  
                elif ind == len(res)-1:
                    data["company_name"].append(i[1])

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i[1])

                # To get DESIGNATION
                elif ind == 1:
                    data["designation"].append(i[1])

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+',i[1]):
                    data["area"].append(i[1].split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+',i[1]):
                    data["area"].append(i[1])

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i[1])
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i[1])
                match3 = re.findall('^[E].*',i[1])
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]',i[1])
                if state_match:
                     data["state"].append(i[1][:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);',i[1]):
                    data["state"].append(i[1].split()[-1])
                if len(data["state"])== 2:
                    data["state"].pop(0)

                # To get PINCODE        
                if len(i[1])>=6 and i[1].isdigit():
                    data["pin_code"].append(i[1])
                elif re.findall('[a-zA-Z]{9} +[0-9]',i[1]):
                    data["pin_code"].append(i[1][10:])
    print('Inserting the data.........')
    return sqlutil.insert_data(data)
                            

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def img_to_binary(image):
      # Convert image data to binary format
     with open(image, 'rb') as file:
          binaryData = file.read()
     return binaryData    

