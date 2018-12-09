
import requests
import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, abort	
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import mongodb
import re
import json
import mongodb
import Fundamental_Analysis
import Institutional_Investors
#import Standard_Deviation
import Technical_Analysis

app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi('TBZCum8z1Mn+BN49uxzu4JmchnYzwrPptPMR9KKoZGqaJ/26Q6ltvkB9RYdAEuZrJHO8s1pcepjTgkxpRfjR2HTbwnaoDw4wkLLtdoMt7CvCWbAt86KVGEWJH/opS/dADbEPita9DfsfwVK1RRyayAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('24eb4648d2e8bff6711f67fae19d76c8')
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):  
    profile = line_bot_api.get_profile(event.source.user_id)
    nameid = profile.display_name 
    uid = profile.user_id 
    
    if mongodb.show_user(uid):
        mongodb.write_user(nameid,uid)
    
    usespeak=str(event.message.text)


    if re.match('[0-9]{4}[<>][0-9]',usespeak):
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+''))
        return 0


    elif re.match('[0-9]{4}',usespeak): 
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+''))
        return 0
        
        
    elif re.match('[0-9]{4}',usespeak):
        mongodb.update_temporary_stock(uid,usespeak)
        url = 'https://tw.stock.yahoo.com/q/q?s=' + usespeak 

        list_req = requests.get(url)

        soup = BeautifulSoup(list_req.content, "html.parser")

        getstock= soup.findAll('b')[1].text
        line_bot_api.push_message(uid, TextSendMessage(usespeak + '' + getstock))
        return 0
    
    elif re.match('',usespeak):
        
        get=mongodb.show_user_stock_fountion()
        msg=''

        if len(get) >0:
            for i in get:  
                msg += i['stock'] + " " + i['bs'] + " " + str(i['price']) +'\n'
            line_bot_api.push_message(uid, TextSendMessage(msg))
            return 0
        else:
            line_bot_api.push_message(uid, TextSendMessage(''))
            return 0
        

    elif re.match('',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
      
        line_bot_api.push_message(uid, TextSendMessage(Institutional_Investors.stockII(usespeak)))
        return 0
    
    elif re.match('K',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_KD(usespeak)))
        return 0
    
    elif re.match('',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MA(usespeak)))
        return 0
    
    elif re.match('MACD',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MACD(usespeak)))
        return 0
    
    elif re.match('OBV',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_OBV(usespeak)))
        return 0
    
    elif re.match('',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_William(usespeak)))
        return 0
    
    elif re.match('ATR',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ATR(usespeak)))
        return 0
    
    elif re.match('ADX',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
     
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ADX(usespeak)))
        return 0
    
    elif re.match('RSI',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
    
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_RSI(usespeak)))
        return 0
    
    elif re.match('MFI',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
     
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MFI(usespeak)))
        return 0
    
    elif re.match('ROC',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ROC(usespeak)))
        return 0
    elif re.match('90',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        line_bot_api.push_message(uid,TextSendMessage('：\n'+Fundamental_Analysis.gpm()))
        return 0
    
    elif re.match('',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        line_bot_api.push_message(uid,TextSendMessage('：\n'+Fundamental_Analysis.pbr()))
        return 0
    
    elif re.match('5',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage(''))
        line_bot_api.push_message(uid,TextSendMessage('：\n'+Fundamental_Analysis.eps()))
        return 0
    elif re.match(',usespeak):
        message = TemplateSendMessage(
            alt_text='（Technical Analysis）',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/7FwK6MA.png',
                        title='',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='ROC',
                                text='ROC'
                            ),
                            MessageTemplateAction(
                                label='MA',
                                text='MA'
                            ),
                            MessageTemplateAction(
                                label='MACD',
                                text='MACD'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/9BlDjoF.png',
                        title='',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='OBV',
                                text='OBV'
                            ),
                            MessageTemplateAction(
                                label='',
                                text=''
                            ),
                            MessageTemplateAction(
                                label='ATR',
                                text='ATR'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/OkpeEZ7.png',
                        title='',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='ADX',
                                text='ADX'
                            ),
                            MessageTemplateAction(
                                label='RSI',
                                text='RSI'
                            ),
                            MessageTemplateAction(
                                label='MFI',
                                text='MFI'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.push_message(uid, message)
        return 0
    elif re.match('',usespeak): 
        buttons_template = TemplateSendMessage(
            alt_text='',
            template=ButtonsTemplate(
                title='（Fundamental Analysis）',
                text='',
                actions=[
                    MessageTemplateAction(
                        label='90％',
                        text='90％'
                    ),
                    MessageTemplateAction(
                        label='100',
                        text='100'
                    ),
                    MessageTemplateAction(
                        label='',
                        text='5'
                    ),
                    
                ]
            )
        )
        line_bot_api.push_message(uid, buttons_template)
        return 0
        
    else:
        line_bot_api.push_message(uid,message)
        return 0
            
                    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 27017))
    app.run(host='0.0.0.0', port=port)

