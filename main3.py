#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove , InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

BAISCOPE, NEXT_PAGE, SUBZLK  , SELECTOR , RESULT= range(5)

data = {'title': ""}

# --- states use in conversation ---

TITLE = 1

next_count = 1

m = 0




# --- functions use in conversation ---


def add(update: Update, _: CallbackContext) -> int:
    global data3
    data3 = {'title': ""}
    update.message.reply_text("ENTER SEARCH TITLE")
    return SELECTOR


def get_selector(update: Update, _: CallbackContext) -> int:
    data3['title'] = update.message.text
    update.message.reply_text("++++++++++++++++++++")
    keyboard = [
                        [InlineKeyboardButton("Baiscope", callback_data=("Baiscopelk"))],
                        [InlineKeyboardButton("Subzlk", callback_data=("SubzLk"))]
                        # [InlineKeyboardButton("Zoom (NOT AVAILABLE)", callback_data=("SubzLk"))]
                        # [InlineKeyboardButton("Subsinhalen (NOT AVAILABLE)", callback_data=("SubzLk"))]
                    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Please choose a site :', reply_markup=reply_markup)
    return RESULT



def get_result(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.message.reply_text("++++++++++++++++++++")
    query.answer()
    if "Baiscopelk" == query.data:
        #print (data3['title'])   
        try:
            page = requests.get("https://www.baiscopelk.com/?s="+data3['title'])
            global soup
            soup = BeautifulSoup(page.content , "html.parser")
        except:
            query.message.reply_text("CANT LOAD LINK. HIT /cancel TO STOP ")
            #print("failed")
        ti_num = 1
        titles = []
        lin_num = 0
        links = []
        try:
            title = soup.find_all("h2" , class_="post-box-title")
            more_link = soup.find_all("a" , class_="more-link")

            for ti_link , data in zip(more_link , title): 
                titles.append(data.text)
                datalinks = ti_link.get('href')
                links.append(ti_link.get('href'))


                mylink = datalinks
                newlink = mylink.replace('https://www.baiscopelk.com/', "")
                

                query.message.reply_text("++++++++++++++++++++")
                try:
                    keyboard = [
                                [InlineKeyboardButton("Download", callback_data=newlink)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                    reply_markup = InlineKeyboardMarkup(keyboard)
            
                    query.message.reply_text(f"{ti_num} : {data.text}", reply_markup=reply_markup)
                except :
                    keyboard = [
                                [InlineKeyboardButton("Download", url=datalinks)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                    reply_markup = InlineKeyboardMarkup(keyboard)
            
                    query.message.reply_text(f"{ti_num} : {data.text}", reply_markup=reply_markup)
                    

                lin_num += 1
                ti_num += 1   
            print(ti_num)
            if 21 == ti_num:
                keyboardq = [
                                [
                                InlineKeyboardButton("   Previous Page   ", callback_data="Previous"),
                                InlineKeyboardButton("     Next Page     ", callback_data="Next"),
                                ]
                            ]
                
                reply_markupq = InlineKeyboardMarkup(keyboardq)
                
                query.message.reply_text("Choose Page", reply_markup=reply_markupq)
                return NEXT_PAGE
            elif 0 == ti_num:
                query.message.reply_text("NO RESULT FOR THIS KEYWORD")

        except Exception as e:
            query.message.reply_text("CANT LOAD LINK.")
    if "SubzLk" == query.data:
        page_s = requests.get(f"https://subz.lk/?s={data3['title']}")
        soup_s = BeautifulSoup(page_s.content, 'html.parser')

        tiltle = soup_s.find("div" ,class_="spost-content").find_all("h4")

        link = soup_s.find("div" ,class_="spost-content").find_all("a" , class_="more-link" , href=True)
        num = 1
        for links,data in zip( link , tiltle):
            # print(links.get("href"))
            # print(data.text)
            mylink = links.get("href")
            newlink = mylink.replace('https://subz.lk/', "")

            query.message.reply_text("++++++++++++++++++++")
            try:
                keyboard = [
                                [InlineKeyboardButton("Download", callback_data=newlink)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                reply_markup = InlineKeyboardMarkup(keyboard)
            
                query.message.reply_text(f"{num} : {data.text}", reply_markup=reply_markup)
            except :
                    keyboard = [
                                [InlineKeyboardButton("Download", url=links.get("href"))],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                    reply_markup = InlineKeyboardMarkup(keyboard)
            
                    query.message.reply_text(f"{num} : {data.text}", reply_markup=reply_markup)
            num +=1
        return SUBZLK

#--------------Baiscope----------------------

def get_next_pages(update: Update, _: CallbackContext) -> None:
    global m
    print(m)
    query = update.callback_query
    query.answer()
    try:
        next_page = []

        next_link = soup.find_all("a" , class_="page")
        for dat in next_link:
            next_page.append(dat.get('href'))
            global next_count
            next_count =  next_count + 1
    except:
        print("faild")
   
    ti_num = 1
    lin_num = 0
    titles = []
    links = []

    if "Next" == query.data:
        page2 = requests.get(next_page[m])
        soup2 = BeautifulSoup(page2.content , "html.parser")
        title2 = soup2.find_all("h2" , class_="post-box-title")
        more_link2 = soup2.find_all("a" , class_="more-link")
        
        for ti_link2 , datas in zip(more_link2 , title2): 

            links.append(ti_link2.get('href'))
            lin_num += 1

            titles.append(datas.text)
            ti_num += 1
            datalinks2 = ti_link2.get('href')
            mylink2 = datalinks2
            newlink2 = mylink2.replace('https://www.baiscopelk.com/', "")

            try:
                keyboard = [
                                [InlineKeyboardButton("Download", callback_data=newlink2)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                reply_markup = InlineKeyboardMarkup(keyboard)
            
                query.message.reply_text(f"{lin_num} : {datas.text}", reply_markup=reply_markup)
                query.message.reply_text("++++++++++++++++++++")
            except :
                keyboard = [
                                [InlineKeyboardButton("Download", url=datalinks2)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]

                reply_markup = InlineKeyboardMarkup(keyboard)
            
                query.message.reply_text(f"{ti_num} : {datas.text}", reply_markup=reply_markup)
                query.message.reply_text("++++++++++++++++++++")

        if 21 == ti_num:

            keyboardq = [
                            [
                                InlineKeyboardButton("   Previous Page   ", callback_data="Previous"),
                                InlineKeyboardButton("     Next Page     ", callback_data="Next"),
                            ]
                        ]
                
            reply_markupq = InlineKeyboardMarkup(keyboardq)
                
            query.message.reply_text(f"Choose Page", reply_markup=reply_markupq)
            try:
                return NEXT_PAGE 
            finally:
                m += 1
        elif 0 == ti_num:
            query.message.reply_text("NO RESULTS")
        

    elif "Previous" == query.data:
        page2 = requests.get(next_page[m-2])
        soup2 = BeautifulSoup(page2.content , "html.parser")
        title2 = soup2.find_all("h2" , class_="post-box-title")
        more_link2 = soup2.find_all("a" , class_="more-link")

        for ti_link2 , datas in zip(more_link2 , title2): 
                    #print(f"{lin_num} : {ti_link2.get('href')}")
                    links.append(ti_link2.get('href'))
                    lin_num += 1
                    #print(f"{ti_num} : {datas.text}")
                    #query.message.reply_text(f"{ti_num} : {datas.text}")
                    titles.append(datas.text)
                    ti_num += 1
                    datalinks2 = ti_link2.get('href')
                    mylink2 = datalinks2
                    newlink2 = mylink2.replace('https://www.baiscopelk.com/', "")

                    try:
                        keyboard = [
                                        [InlineKeyboardButton("Download", callback_data=newlink2)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                                    ]
                    
                        reply_markup = InlineKeyboardMarkup(keyboard)
                    
                        query.message.reply_text(f"{lin_num}: {datas.text}", reply_markup=reply_markup)
                        query.message.reply_text("++++++++++++++++++++")
                    except :
                        keyboard = [
                                [InlineKeyboardButton("Download", url=datalinks2)],  #https://www.baiscopelk.com/game-of-thrones-s7e06-beyond-the-wall-with-sinhala-subtitle/
                            ]
            
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.message.reply_text(f"{ti_num} : {datas.text}", reply_markup=reply_markup)
                        query.message.reply_text("++++++++++++++++++++")
        if 21 == ti_num:
            keyboardc = [
                            [
                                InlineKeyboardButton("   Previous Page   ", callback_data="Previous"),
                                InlineKeyboardButton("     Next Page     ", callback_data="Next"),
                            ]
                        ]
                
            reply_markupc = InlineKeyboardMarkup(keyboardc)
            query.message.reply_text(f"Choose Page", reply_markup=reply_markupc)
            try:
                return NEXT_PAGE 
            finally:
                m -= 1
        elif 0 == ti_num:
            query.message.reply_text("NO RESULTS")
    else:
        query.answer()
        down = f"https://www.baiscopelk.com/{query.data}"
            
        sup_page_soup = requests.get(down)
        
        sup_page_soup = BeautifulSoup(sup_page_soup.content, 'html.parser')

        for data in sup_page_soup.find("p" ,style="padding: 0px; text-align: center;"):
            sub_links = data.get('href')
        print(sub_links)
        try:
            query.message.reply_document(sub_links)
        except:
            x = soup.find("title")
            keyboard = [
                                [InlineKeyboardButton("Download", url=sub_links)], 
                            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            query.message.reply_text(x.text, reply_markup=reply_markup)

#--------------subzlk-------------------

def subzlkupload(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    query.message.reply_text("PLEASE WAIT...")
    downlink = f"https://subz.lk/{query.data}"
    page = requests.get(downlink)
    soup = BeautifulSoup(page.content, 'html.parser')

    x = soup.find("a", class_="czdown blue elax")
    mainlink = (x.get("href"))
    y = soup.find("div" , class_="spost-title")
    y = y.text

    try:
        query.message.reply_document(mainlink)
    except:
        keyboard = [
                                [InlineKeyboardButton("Download", url=mainlink)], 
                            ]
            
        reply_markup = InlineKeyboardMarkup(keyboard)
            
        query.message.reply_text(y, reply_markup=reply_markup)


    
#--------------Upload by link-------------------

def link_uploader(update: Update, _: CallbackContext) -> None:
    text = update.message.text

    baiscope_ptn = r'https://www.baiscopelk\.com/[a-z0-9\-]+'
    baiscope_regex = re.compile(baiscope_ptn, flags=re.I)

    zoom_ptn = r'https://zoom\.lk/[a-z0-9\-]+'  
    zoom_regex = re.compile(zoom_ptn, flags=re.I)

    subsinhalen_ptn = r'https://www.subsinhalen\.com/[a-z0-9\-]+'
    subsinhalen_regex = re.compile(subsinhalen_ptn, flags=re.I)

    subzlk_ptn = r'https://subz\.lk/[a-z0-9\-]+'
    subzlk_regex = re.compile(subzlk_ptn, flags=re.I)

    if baiscope_regex.match(text):
        page = requests.get(text)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            try:
                rows = []
                trs = soup.find("table" , class_="aligncenter").find_all("tr")
                for idx, tr in enumerate(trs):
                    tds = tr.find_all('td')
                    if idx == 0:
                        columns = [td.text.strip() for td in tds]
                    else:
                        row = [td.find('a')['href'] if td.find('a') else td.text for td in tds]
                        rows.append(row)
                
                got_dict = pd.DataFrame(rows, columns=columns).to_dict('list')
                for k, v in got_dict.items():
                    v = [x for x in v if x != None and x != '']
                    got_dict[k] = v



                for k, v in got_dict.items():
                    update.message.reply_text(k)
                    for episode in v:
                        sup_page = requests.get(episode)
                        sup_soup = BeautifulSoup(sup_page.content, 'html.parser')

                        for data in sup_soup.find("p" ,style="padding: 0px; text-align: center;"):
                            main_links = data.get('href')
                            bb = sup_soup.find("title").text
                        
                        try:
                            update.message.reply_document(main_links)
                        except:
                            keyboard = [
                                    [InlineKeyboardButton(bb, url=main_links)], 
                                ]
                
                            reply_markup = InlineKeyboardMarkup(keyboard)
                
                            update.message.reply_text(bb, reply_markup=reply_markup)

                update.message.reply_text("successfully uploaded !")
            except Exception as e:
                update.message.reply_text(f"{e} failed")

        except:
            try:
                text = update.message.text
                sup_page_soup = requests.get(text)
                sup_page_soup = BeautifulSoup(sup_page_soup.content, 'html.parser')

                x = soup.find("title")

                for data in sup_page_soup.find("p" ,style="padding: 0px; text-align: center;"):
                    sub_links = data.get('href')
                    
                    
                try:
                    update.message.reply_document(sub_links)
                except:
                    keyboard = [
                                [InlineKeyboardButton("Download", url=sub_links)], 
                            ]
            
                reply_markup = InlineKeyboardMarkup(keyboard)
            
                update.message.reply_text(x.text, reply_markup=reply_markup)
            except:
                update.message.reply_text("Failed !")

    elif zoom_regex.match(text):
        page = requests.get(text)
        soup = BeautifulSoup(page.content , "html.parser")
        x = soup.find_all(class_="aligncenter download-button")
        y = soup.find("h1" , class_="tdb-title-text")

        for link in soup.find_all('a', class_= "aligncenter download-button" , attrs={'href': re.compile("^https://")}):
            #print(link.get('href'))
            mainlink = link.get('href')
            try:
                update.message.reply_document(mainlink)
            except:
                keyboard = [
                                [InlineKeyboardButton("Download", url=mainlink)], 
                            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(y.text, reply_markup=reply_markup)

    elif subsinhalen_regex.match(text):
        page = requests.get(text)
        soup = BeautifulSoup(page.content, 'html.parser')

        x = soup.find("a" , class_="download-link filetype-icon filetype-srt")
        mainlink =  x.get("href")
        y = soup.find("h1" , class_="name post-title entry-title")
        y = (y.text)
        try:
            update.message.reply_document(mainlink)
        except:
            keyboard = [
                                [InlineKeyboardButton("Download", url=mainlink)], 
                            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(y, reply_markup=reply_markup)
        
    elif subzlk_regex.match(text):
        update.message.reply_text("PLEASE WAIT...")
        page = requests.get(text)
        soup = BeautifulSoup(page.content, 'html.parser')

        x = soup.find("a", class_="czdown blue elax")
        mainlink = (x.get("href"))
        y = soup.find("div" , class_="spost-title")
        y = y.text

        try:
            update.message.reply_document(mainlink)
        except:
            keyboard = [
                                [InlineKeyboardButton("Download", url=mainlink)], 
                            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(y, reply_markup=reply_markup)

    else:
        update.message.reply_text("THIS SITE NOT SUPPORTED")

def start(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f'Welcome {user.first_name}')
                
def help(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("""welcome to ✨ 𝚂𝚒𝚗𝚑𝚊𝚕𝚊 𝚂𝚞𝚋-𝚙𝚊𝚕 ✨

**Supported web sites**

💠 https://www.baiscopelk.com/
💠 https://www.baiscopelk.com/tv-series 
💠 https://subz.lk/

💠 https://www.subsinhalen.com/
💠 https://zoom.lk/

ඉහත sites අතරින් ඔබට subs download කර ගැනීමට අවශ්‍ය  Link එක මෙහි paste කර හෝ /search මගින් search කර පහසුවෙන් download කර ගත හැක.

ඔබගෙ විධානය නතර කිරීමට /cancel බාවිතා කරන්න. ( විධානයන් ක්‍රියාත්මක නොවේ නම් /cancel ලබා දී උත්සහ කරන්න. )

අපගේ චැනලය : https://t.me/sinhalasubpal""")

def cancel(update, context):

    update.message.reply_text('canceled')

    # end of conversation
    return ConversationHandler.END

# --- create conversation ---

my_conversation_handler = ConversationHandler(
   entry_points=[CommandHandler('search', add , run_async=True)],
   states={
       SELECTOR: [
           CommandHandler('cancel', cancel),  
           MessageHandler(Filters.text & ~Filters.command, get_selector , run_async=True)
       ],
       RESULT : [
           CommandHandler('cancel', cancel , run_async=True),
           CallbackQueryHandler(get_result , run_async=True)
       ],
       NEXT_PAGE : [CallbackQueryHandler(get_next_pages , run_async=True),
                    CommandHandler('cancel', cancel , run_async=True),
        ],
        SUBZLK : [ CallbackQueryHandler(subzlkupload , run_async=True),
                    CommandHandler('cancel', cancel , run_async=True),

                    ]

   },
   fallbacks=[CommandHandler('cancel', cancel , run_async=True)]
)                

def main() -> None:

    updater = Updater("1573987680:AAExIujkEjLtoiG9PobysV33jjl9Mb6ixIM")


    dispatcher = updater.dispatcher 
    dispatcher.add_handler(my_conversation_handler)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command , link_uploader , run_async=True))
    dispatcher.add_handler(CommandHandler("start", start , run_async=True))
    dispatcher.add_handler(CommandHandler("help", help , run_async=True))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
