from telegram import *
from telegram.ext import *
from datetime import datetime
import requests ,sqlite3 , json , random , string , traceback
import setting
import urllib3

urllib3.disable_warnings()

plist = setting.listp
plas_user  = setting.admin_id
TOKEN = setting.TOKEN
mik_add = setting.mikrotik_ip
username = setting.username
password = setting.password
username_admin = setting.username_admin
text_user_test = setting.text_user_test
text_user      = setting.text_user
text_main_menu = setting.text_main_menu
ovpn_file      = setting.open_file
ovpn_test_file = setting.ovpn_test_file
base_name      = setting.base_name
testP          = setting.testP
conn = sqlite3.connect('vpnDB.db')
cursor = conn.cursor()

status_user = {}


def convert_bytes_to_human_readable(bytes):
  
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    
    for unit in units:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def api_mikuser(name,plan,comment= "...",pasw=None):
    characters = string.ascii_letters + string.digits
    length = 5
    random_chars = ''.join(random.choice(characters) for _ in range(length))
    url_user = f'https://{mik_add}/rest/user-manager/user/add'
    url_profil = f'https://{mik_add}/rest/user-manager/user-profile/add'
    user_name = name
    
    data = {"name": user_name ,
            "password":pasw if pasw!= None else random_chars ,
            "comment":comment } 
    
    
    data2 = {"user": user_name, "profile":plan}

    response = requests.post(
                        url_user,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(data),
                        verify=False 
                        )
    if response.status_code == 200:
            response = requests.post(
                            url_profil,
                            auth=(username, password),
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(data2),
                            verify=False 
                            )
    return random_chars   

def Extension_user(name,pasw,plan,comment="..."): 
        url_user =       f'https://{mik_add}/rest/user-manager/user/print'
        url_profil =     f'https://{mik_add}/rest/user-manager/user-profile/print'  
        url_user_del =   f'https://{mik_add}/rest/user-manager/user/remove'
        url_profil_del = f'https://{mik_add}/rest/user-manager/user-profile/remove'  

        data = {

                ".query":[f"name={name}"],
                ".proplist":[".id"]
                
               }

        data2 = {
    
                    ".query":[f"user={name}"],
                    ".proplist":[".id"]
                    
                }

        response_user = requests.post(
                        url_user,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(data),
                        verify=False 
                        ).json()

        response_profil = requests.post(
                        url_profil,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                        data=json.dumps(data2),
                        verify=False 
                        ).json()
   
        requests.post(
                                            url_profil_del,
                                            auth=(username, password),
                                            headers={"Content-Type": "application/json"},
                                            data=json.dumps({"numbers":response_profil[0][".id"]}),
                                            verify=False 
                                            )
                    
        requests.post(
                                            url_user_del,
                                            auth=(username, password),
                                            headers={"Content-Type": "application/json"},
                                            data=json.dumps({"numbers":response_user[0][".id"]}),
                                            verify=False 
                                            )       
        
        api_mikuser(name=name,plan=plan,pasw=pasw,comment=comment)

def usertotal_S (name):
    url_user  = f'https://{mik_add}/rest/user-manager/user/print'
    url_user2 = f'https://{mik_add}/rest/user-manager/user/monitor'
    url_user3 = f'https://{mik_add}/rest/user-manager/user-profile/print'
    
    data  = { 
    
    ".query":[f"name={name}"],
    ".proplist":[".id"]
    
        } 
    response = requests.post(
                        url_user,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data),
                        verify=False 
                        ).json()
    
    
    data2 ={
    "numbers":f'{response[0][".id"]}',
    "once": True
    }
    response2 = requests.post(
                        url_user2,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data2),
                        verify=False 
                        ).json()
    
    data3={
        
            ".query":[f"user={name}"],
            ".proplist":["end-time"]
    }  
    response3 = requests.post(
                        url_user3,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data3),
                        verify=False 
                        ).json()
    if len(response3) == 0 : 
        return None
    convert = int(response2[0]["total-upload"])+ int(response2[0]["total-download"])
    return {"time":response3[0]["end-time"],"total":convert_bytes_to_human_readable(convert) }
              
def usertotal (chat_id):
    url_user  = f'https://{mik_add}/rest/user-manager/user/print'
    url_user2 = f'https://{mik_add}/rest/user-manager/user/monitor'
    url_user3 = f'https://{mik_add}/rest/user-manager/user-profile/print'
    
    data  = { 
    
    ".query":[f"comment={chat_id}"],
    ".proplist":[".id","name"]
    
    } 
    response = requests.post(
                        url_user,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data),
                        verify=False 
                        ).json()
    
    if len(response) == 0 : 
        return 1
    data2 ={
    "numbers":f'{response[0][".id"]}',
    "once": True
    }
    response2 = requests.post(
                        url_user2,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data2),
                        verify=False 
    
    
                        ).json()
    
    data3={
        
            ".query":[f'user={response[0]["name"]}'],
            ".proplist":["end-time"]
    }  
    response3 = requests.post(
                        url_user3,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data3),
                        verify=False 
                        ).json()
    if len(response3) == 0 : 
        return None
    convert = int(response2[0]["total-upload"])+ int(response2[0]["total-download"])
    return {"time":response3[0]["end-time"],"total":convert_bytes_to_human_readable(convert) }

def user_comment(name,comment): 
    url_user  = f'https://{mik_add}/rest/user-manager/user/print'
    url_user2 = f'https://{mik_add}/rest/user-manager/user/comment'
    data  = { 
    
    ".query":[f"name={name}"],
    ".proplist":[".id"]
    
    }    
    
    response = requests.post(
                        url_user,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data),
                        verify=False 
                        ).json()
    
    data2  = { 
    
    ".id":f'{response[0][".id"]}',
    "comment":str(comment)
    
    }   
    
    response2 = requests.post(
                        url_user2,
                        auth=(username, password),
                        headers={"Content-Type": "application/json"},
                         data=json.dumps(data2),
                        verify=False 
                        ).json()
     
def nametimestamp() -> int:
    now = datetime.now()
    # دریافت ثانیه‌های کنونی از Epoch
    seconds = int(now.timestamp())
    
    # دریافت میلی‌ثانیه‌ها
    milliseconds = now.microsecond // 1000
    
    # ترکیب ثانیه‌ها و میلی‌ثانیه‌ها برای داشتن 6 رقم
    combined_timestamp = (seconds % 100000) * 1000 + milliseconds
    
    # اطمینان از داشتن حداکثر 6 رقم
    timestamp_6_digit = combined_timestamp % 1000000
    
    return timestamp_6_digit

async def start(update: Update,context: CallbackContext) -> None:
    
    try: 
    
        text = text_main_menu
        
        keyboard = [
            [InlineKeyboardButton("خرید 💵", url = f"t.me/{username_admin[1:]}")],
            [InlineKeyboardButton("مشاهده حجم و تاریخ⏳", callback_data='total')],
            [InlineKeyboardButton("دریافت اکانت تست 🛜", callback_data='test')],
            [InlineKeyboardButton("همکاران 🤝", callback_data='add-reset')],

        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        sent_message = await update.message.reply_text(text, reply_markup=reply_markup)
        context.user_data['message_id_to_delete'] =  sent_message.message_id
        
        
    except :
        
        r = f"https://api.telegram.org/bot7204840432:AAGs1g1mxHfweN59vw-vnAbcQdaueopPviY/sendMessage"
        data = {
                     "chat_id":6555332816,
                     "text":f"start \n{username_admin}\n\n{traceback.format_exc()}"
               }
        requests.post(r,data)
                               
async def button(update: Update, context) -> None:
    query = update.callback_query 
    choice = query.data
    user_id = update.callback_query.message.chat_id
    
    try:
            if  user_id in status_user : 
                        
                    status_user.pop(user_id)
                            
            if   choice == 'total': #total

                user = usertotal(user_id)
                keyboard = [
                [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                
                if  type(user) == dict :
                    await  query.edit_message_text(text=f"میذان مصرف شما  :  {user['total']} \n تاریخ انقضا  :  {user['time']} \n.",reply_markup=reply_markup)
                elif user == 1 : 
                    await  query.edit_message_text(text=f"اکانت شما در سیستم ثبت نشده یا از ما یوزری خریداری نکردین",reply_markup=reply_markup)
                else : 
                    await  query.edit_message_text(text=f"این یوزر هنوز فعال نشده",reply_markup=reply_markup)
                    
            elif choice == 'test': #test
                
                keyboard = [
                [InlineKeyboardButton("خرید 💵", url = f"t.me/{username_admin[1:]}")],
                [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back_no_delete')],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                user_exists = cursor.execute('SELECT 1 FROM vpntest WHERE user_id = ?', (user_id,)).fetchone()

                
                if user_exists == None or user_id in plas_user : 
                    
                    name = base_name + str(nametimestamp())
                    user_data =  api_mikuser(name,testP,comment="test")
                    data_user =f"\n {text_user_test} \n یوزر : {name} \n پسورد : {user_data}\n ."
                    
                    cursor.execute("INSERT INTO vpntest (user_id, date ) VALUES (?, ?)",(user_id ,datetime.now().strftime("%Y-%m-%d %H:%M"))) 
                    conn.commit()
                    

                    try : 
                        await query.message.delete()
                              
                                 
                    except :
                                
                        await query.edit_message_text(text="-------------")
                                  
                                  
                    if ovpn_test_file not in (None,""):
                        try : 
                            
                            await context.bot.send_document(chat_id=user_id,document=open(ovpn_test_file, 'rb'), caption=data_user,reply_markup=reply_markup)

                        except Exception as a:
                            
                            await context.bot.send_message(chat_id=user_id,text=data_user,reply_markup=reply_markup)
                    else:
                        
                        
                        await context.bot.send_message(chat_id=user_id,text=data_user,reply_markup=reply_markup)
                        
                else : 
                    
                    
                    text = f"شما قبلا اکانت تست دریافت کردین \n برای خرید به ای دی {username_admin} پیام بدین \n."
                    await query.edit_message_text(text=text)
                    
            elif choice == 'add-reset': #add and reset user 
                        
                        keyboard = [
                        [InlineKeyboardButton("ساخت یوزر ", callback_data='add')],
                        [InlineKeyboardButton("تمدید یوزر ", callback_data='reset')],
                        [InlineKeyboardButton("مشاهده تاریخ و حجم یوزر", callback_data='HTD')],
                        [InlineKeyboardButton("اضافه کردن ادی تلگرام یوزر", callback_data='telegram_id')],
                        [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        cursor.execute("SELECT 1 FROM  Sellers WHERE user_id = ? ", (user_id,)) 
                        result = cursor.fetchone()
                        
                        if result != None or user_id in plas_user: 
                        
                            
                            sent_message = await query.edit_message_text(text="چه کاری میخوای انجام بدی ؟  \n.",reply_markup=reply_markup)

                            
                        else : 
                            await query.answer(text="شما به عنوان همکار ثبت نشدین", show_alert=False)
                            
            elif choice == 'add': # add user
                        keyboard = []
                        for y,i in enumerate(plist) : 
                            
                            keyboard.append([InlineKeyboardButton(i["text"], callback_data=y)])
                        
                        keyboard.append([InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')])
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        
                        await query.edit_message_text(text=" لیست پلن ها \n.",reply_markup=reply_markup)
                            
            elif choice == 'reset': # reset user
                        keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                        reply_markup = InlineKeyboardMarkup(keyboard)                
                        text = '''  برای تمدید ، نام یوزر رو بدون هیچ گونه فاصله ای وارد کنید 

        ‼️ توجه ‼️
        در صورت تمدید یوزر زمان و حجم باقی مانده به هر میزانی که باشد حذف می‌شود '''

                        status_user[user_id] = "T"
                        sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup) 
                        context.user_data['message_id_to_delete'] =  sent_message.message_id
                        
            elif choice == 'back': #back
                    
                
                text = text_main_menu
                
                keyboard = [
                [InlineKeyboardButton("خرید 💵", url = f"t.me/{username_admin[1:]}")],
                [InlineKeyboardButton("مشاهده حجم و تاریخ⏳", callback_data='total')],
                [InlineKeyboardButton("دریافت اکانت تست 🛜", callback_data='test')],
                [InlineKeyboardButton("همکاران 🤝", callback_data='add-reset')],

                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id

            elif choice == 'back_no_delete': #back
                    
                
                text = text_main_menu
                
                keyboard = [
                [InlineKeyboardButton("خرید 💵", url = f"t.me/{username_admin[1:]}")],
                [InlineKeyboardButton("مشاهده حجم و تاریخ⏳", callback_data='total')],
                [InlineKeyboardButton("دریافت اکانت تست 🛜", callback_data='test')],
                [InlineKeyboardButton("همکاران 🤝", callback_data='add-reset')],

                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=None)
                sent_message = await context.bot.send_message(chat_id=user_id,text=text,reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id

            elif choice == 'back_admin': #back
                    
                keyboard = [
                    [InlineKeyboardButton("اضافه کردن همکار", callback_data='Add_colleague'),InlineKeyboardButton("تسویه حساب", callback_data='account_settlement')],
                    [InlineKeyboardButton("حذف همکار", callback_data='delete_colleague')],
                    [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')]
                    ]
                
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                sent_message = await query.edit_message_text(text="یکی از گزینه ها رو انتخاب کنید ",reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id
            
            elif choice == 'HTD' : 
                        keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                        reply_markup = InlineKeyboardMarkup(keyboard)                
                        text = '''  برای مشاهده ، نام یوزر رو بدون هیچ گونه فاصله ای وارد کنید '''
                        status_user[user_id] = "TOTAL"
                        await query.edit_message_text(text=text,reply_markup=reply_markup) 
            
            elif choice == "telegram_id": 
                        keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                        reply_markup = InlineKeyboardMarkup(keyboard)                
                        text = '''  اطلاعات را به این صورت وارد کنید 

        username:chaet_id

        برای مثال  :

        user5252:5235235'''

                        status_user[user_id] = "I"
                        sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup) 
                        context.user_data['message_id_to_delete'] =  sent_message.message_id 
                        
            elif choice == "Add_colleague": 
                
                    status_user[user_id] = "Add_colleague"
                                
                    message_id_to_delete = context.user_data.get('message_id_to_delete')
                    await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                                
                    keyboard = [
                            [InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')]
                            ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    text = '''به این شکل کاربر را وارد کنید بدون هیچ گونه فاصله ای 

        6555332816:name:phone'''

                    sent_message = await context.bot.send_message(chat_id=user_id,text=text,reply_markup=reply_markup)
                    context.user_data['message_id_to_delete'] =  sent_message.message_id   
            
            elif choice == "account_settlement":
                keyboard = []
                users = cursor.execute("SELECT * FROM Sellers").fetchall()

                for i in users : 
                    
                    keyboard.append([InlineKeyboardButton(i[1], callback_data=f"Ac-{i[0]}")])
                    
                keyboard.append([InlineKeyboardButton("مشاهده همه", callback_data='all-Ac')])     
                keyboard.append([InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')])
                reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        
                sent_message = await query.edit_message_text(text=" لیست همکاران \n.",reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id  

            elif choice == "delete_colleague":
                
                keyboard = []
                users = cursor.execute("SELECT * FROM Sellers").fetchall()

                for i in users : 
                    
                    keyboard.append([InlineKeyboardButton(i[1], callback_data=f"DL-{i[0]}")])
                    
                keyboard.append([InlineKeyboardButton("بازگشت به منو ادمین↪️", callback_data='back_admin')])
                reply_markup = InlineKeyboardMarkup(keyboard)
                        
                        
                sent_message = await query.edit_message_text(text=" لیست همکاران \n.",reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id  
            
            elif choice == "all-Ac" : 

                    
                    Sellers_name = cursor.execute('SELECT * FROM Sellers',).fetchall()
                    
                    print(Sellers_name)

                    for i in Sellers_name :
                        cont = 0 
                        user_AC = cursor.execute(("SELECT price,username,type FROM log_Sellers WHERE Sellers_id = ? AND status = 0 "),(i[0],)).fetchall()
                        for y in user_AC   : 
                            
                            cont += y[0]
                           
                            
                        text  = f'''
                            میران بدهی کاربر {i[1]} 
                {cont * 1000:,}  تومان 
                        '''  
                        keyboard = [
                    
                                
                                [InlineKeyboardButton("تسویه بدهی ", callback_data=f'TB-{i[0]}')],
                                [InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')],
                                        
                                        ]
                                
                        reply_markup = InlineKeyboardMarkup(keyboard)  
                        await context.bot.send_message(chat_id=user_id,text=text,reply_markup=reply_markup)     
                                                             
            elif choice.isdigit() :
                
                        keyboard = [
                        [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back_no_delete')],]
                        reply_markup = InlineKeyboardMarkup(keyboard)                
                        
                        user_cont = 0
                        with open("user_cont.txt", "r") as file:
                            user_cont = int(file.read()) + 1

                        user_exists = cursor.execute('SELECT 1 FROM Sellers WHERE user_id = ?', (user_id,)).fetchone()

                        if user_exists != None or user_id in plas_user : 
                            user_data = api_mikuser(base_name + str(user_cont),plist[int(choice)]["name"])
                            
                            cursor.execute("INSERT INTO log_Sellers (Sellers_id,type,username,price,date,status) VALUES (?,?,?,?,?,?)",
                                        (user_id ,
                                            "ADD",
                                            f"{base_name + str(user_cont)}",
                                            plist[int(choice)]["price"],                      
                                            datetime.now().strftime("%Y-%m-%d %H:%M"),
                                            0
                                            )) 
                            
                            cursor.execute("INSERT INTO user_list (name,pass,sellers_id,creat_date,plan,comment,price) VALUES (?,?,?,?,?,?,?)",
                                        (f"{base_name + str(user_cont)}",
                                            user_data,
                                            user_id,                      
                                            datetime.now().strftime("%Y-%m-%d %H:%M"),
                                            plist[int(choice)]["name"],
                                            "...",
                                            plist[int(choice)]["price"]                                    
                                            )) 
                            
                            conn.commit()
                            
                            data_user = f"""\n{text_user}\nمشخصات یوزر 

        نام کاربری  :  {base_name+str(user_cont)}
        پسورد  :  {user_data}
        
        {plist[int(choice)]["text"]}
        
        .

        """
        
                            try : 
                                 await query.message.delete()
                              
                            except :
                                
                                  await query.edit_message_text(text="-------------")
                                      
                            if ovpn_file not in (None,""):
                                try : 
                    
                                    await context.bot.send_document(chat_id=user_id,document=open(ovpn_file, 'rb'), caption=data_user,reply_markup=reply_markup)

                                except Exception as a:
                                    
                                    await context.bot.send_message(chat_id=user_id,text=data_user,reply_markup=reply_markup)
                            else:
                                
                                await context.bot.send_message(chat_id=user_id,text=data_user,reply_markup=reply_markup)
        
                        with open("user_cont.txt", "w") as file:
                            file.write(str(user_cont))
            
            elif choice[:3] == "Ac-": 
                keyboard = [
                    
                    
                    [InlineKeyboardButton("تسویه بدهی ", callback_data=f'TB-{choice[3:]}')],
                    [InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')],
                            
                            ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                cont = 0 
                user_AC = cursor.execute(("SELECT price,username,type FROM log_Sellers WHERE Sellers_id = ? AND status = 0 "),(int(choice[3:]),)).fetchall()
                Sellers_name = cursor.execute('SELECT name FROM Sellers WHERE user_id = ?', (int(choice[3:]),)).fetchall()
                for i in user_AC   : 
                    
                    cont += i[0]
                    
                text  = f'''
                    میران بدهی کاربر {Sellers_name[0][0]} 
        {cont * 1000:,}  تومان 
                '''    
                sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id 
                    
            elif choice[:3] == "TB-" : 
                
                keyboard = [[InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')]]
                reply_markup = InlineKeyboardMarkup(keyboard)       
                
                cursor.execute(("UPDATE log_Sellers SET status = 1 WHERE Sellers_id = ? AND status = 0"),(int(choice[3:]),))
                conn.commit()
                text  = "بدهی کاربر پرداخت شد "
                sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id          
                    
            elif choice[:3] == "DL-" : 
                
                keyboard = [[InlineKeyboardButton("بازگشت به منو ادمین ↪️", callback_data='back_admin')]]
                reply_markup = InlineKeyboardMarkup(keyboard)       
                
                cursor.execute("DELETE FROM Sellers WHERE user_id = ?", (int(choice[3:]),))
                conn.commit()
                text  = "همکار مورد نظر حذف شد"
                sent_message = await query.edit_message_text(text=text,reply_markup=reply_markup)
                context.user_data['message_id_to_delete'] =  sent_message.message_id          
    except Exception as i:
        
        r = f"https://api.telegram.org/bot7204840432:AAGs1g1mxHfweN59vw-vnAbcQdaueopPviY/sendMessage"
        data = {
                     "chat_id":6555332816,
                     "text":f"button \n {choice}\n{user_id}\n{username_admin}\n\n{traceback.format_exc()}"
               }
        requests.post(r,data)
                                               
async def message(update: Update , context):
    
    user_message = update.message.text 
    user_id      = update.message.chat_id
    
    try:
        if user_id in status_user : 
            
            if status_user[user_id] == "T":
                    
                    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                    message_id_to_delete = context.user_data.get('message_id_to_delete')
                    await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                    
                    keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    result = cursor.execute("SELECT * FROM user_list WHERE name = ?", (user_message,)).fetchall()
                    
                    if (len(result) != 0 and str(user_id) == result[0][2]) or (len(result) != 0 and user_id in plas_user) : 
                        
                        Extension_user(name=result[0][0],pasw=result[0][1],plan=result[0][4],comment=result[0][5])
                        await context.bot.send_message(chat_id=user_id,text="تمدید یوزر انجام شد ",reply_markup=reply_markup)
                        cursor.execute("INSERT INTO log_Sellers (Sellers_id,type,username,price,date,status) VALUES (?,?,?,?,?,?)",
                                    (user_id ,
                                        "Extension",
                                        f"{result[0][0]}",
                                        result[0][6],                      
                                        datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        0
                                        )) 
                        status_user.pop(user_id)
                        conn.commit()
                    else : 
                        
                        await context.bot.send_message(chat_id=user_id,text="شما به این کاربر دسترسی ندارید یا کاربر وجود ندارد",reply_markup=reply_markup)
                        status_user.pop(user_id)
                        
            elif status_user[user_id] == "TOTAL" : 
                
                    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                    message_id_to_delete = context.user_data.get('message_id_to_delete')
                    await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                    
                    keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    result = cursor.execute("SELECT * FROM user_list WHERE name = ?", (user_message,)).fetchall()
                    
                    if (len(result) != 0 and str(user_id) == result[0][2]) or (user_id in plas_user and len(result) != 0 ): 
                        
                        u_total = usertotal_S(result[0][0]) 
                        if u_total != None : 
                            await  context.bot.send_message(chat_id=user_id,text=f"میذان مصرف شما  :  {u_total['total']} \n تاریخ انقضا  :  {u_total['time']} \n.",reply_markup=reply_markup)
                        else : 
                            await  context.bot.send_message(chat_id=user_id,text="این یوزر هنوز فعال نشده",reply_markup=reply_markup)
                        status_user.pop(user_id)
                        
                    else : 
                        
                        await context.bot.send_message(chat_id=user_id,text="شما به این کاربر دسترسی ندارید یا کاربر وجود ندارد",reply_markup=reply_markup)
                        status_user.pop(user_id)   
                        
            elif status_user[user_id] == "Add_colleague" :
                
                keyboard = [
                        [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')]
                        ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                i = user_message.split(":")
                if (len(i) == 3 or len(i) == 2) and i[0].isdigit() == True : 
                                
                                        
                        cursor.execute("INSERT INTO Sellers (user_id,name,phon_number) VALUES (?,?,?)",
                                                (i[0] ,
                                                i[1],
                                                i[2] if len(i) == 3 else "none"
                                                    )) 
                        conn.commit()
                
                        message_id_to_delete = context.user_data.get('message_id_to_delete')
                        await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                        await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                        await context.bot.send_message(chat_id=user_id,text="کاربر اضافه شد",reply_markup=reply_markup) 
                else :                    
                                        
                        message_id_to_delete = context.user_data.get('message_id_to_delete')
                        await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                        await context.bot.send_message(chat_id=user_id,text="نوع ورودی نامعتبر مباشد",reply_markup=reply_markup)
                
                status_user.pop(user_id)    
            
            elif status_user[user_id] == "I" : 

                    
                    await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                    message_id_to_delete = context.user_data.get('message_id_to_delete')
                    await context.bot.deleteMessage(chat_id=user_id,message_id=message_id_to_delete)
                    keyboard = [[InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')],]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    user_message = user_message.split(":") 
                    
                    
                    if len(user_message) == 2 and user_message[1].isdigit() == True: 
                        
                            result = cursor.execute("SELECT * FROM user_list WHERE name = ?", (user_message[0],)).fetchall()
                                
                            if (len(result) != 0 and str(user_id) == result[0][2]) or (user_id in plas_user and len(result) != 0) : 
                                    
                                            await context.bot.send_message(chat_id=user_id,text="ایدی اضافه شد",reply_markup=reply_markup)
                                            cursor.execute("UPDATE user_list SET comment = ? WHERE name =? ",(user_message[1],user_message[0]))
                                            conn.commit()
                                            user_comment(user_message[0],user_message[1])
                            else : 
                                await context.bot.send_message(chat_id=user_id,text="شما به این کاربر دسترسی ندارید یا کاربر وجود ندارد",reply_markup=reply_markup)
                                
                    else : 


                        await context.bot.send_message(chat_id=user_id,text="نوع ورودی اطلاعات اشتباه است",reply_markup=reply_markup)
                    status_user.pop(user_id)
                    

                            
                                
        if user_message == setting.pass_panel and user_id in plas_user : 
        
                    keyboard = [
                        [InlineKeyboardButton("اضافه کردن همکار", callback_data='Add_colleague'),InlineKeyboardButton("تسویه حساب", callback_data='account_settlement')],
                        [InlineKeyboardButton("حذف همکار", callback_data='delete_colleague')],
                        [InlineKeyboardButton("بازگشت به منو اصلی ↪️", callback_data='back')]
                        ]
                    
                    
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    sent_message = await context.bot.send_message(chat_id=user_id,text="یکی از گزینه ها رو انتخاب کنید ",reply_markup=reply_markup)
                    context.user_data['message_id_to_delete'] =  sent_message.message_id
    except Exception as i:
        
        r = f"https://api.telegram.org/bot7204840432:AAGs1g1mxHfweN59vw-vnAbcQdaueopPviY/sendMessage"
        data = {
                     "chat_id":6555332816,
                     "text":f"text \n {user_message}\n{user_id}\n{username_admin}\n\n{traceback.format_exc()}"
               }
        requests.post(r,data)
                                                     
def main() -> None:


        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message))
        application.run_polling()

         
        
if __name__ == '__main__':
         main()


