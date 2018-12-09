
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
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'已經儲存成功'))
        return 0


    elif re.match('刪除[0-9]{4}',usespeak): 
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'已經刪除成功'))
        return 0
        
        
    elif re.match('[0-9]{4}',usespeak):
        mongodb.update_temporary_stock(uid,usespeak)
        url = 'https://tw.stock.yahoo.com/q/q?s=' + usespeak 

        list_req = requests.get(url)

        soup = BeautifulSoup(list_req.content, "html.parser")

        getstock= soup.findAll('b')[1].text
        line_bot_api.push_message(uid, TextSendMessage(usespeak + '目前的價格是' + getstock))
        return 0
    
    elif re.match('我的股票',usespeak):
        
        get=mongodb.show_user_stock_fountion()
        msg=''

        if len(get) >0:
            for i in get:  
                msg += i['stock'] + " " + i['bs'] + " " + str(i['price']) +'\n'
            line_bot_api.push_message(uid, TextSendMessage(msg))
            return 0
        else:
            line_bot_api.push_message(uid, TextSendMessage('沒有資料'))
            return 0
        

    elif re.match('籌碼面分析',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
      
        line_bot_api.push_message(uid, TextSendMessage(Institutional_Investors.stockII(usespeak)))
        return 0
    
    elif re.match('KD圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_KD(usespeak)))
        return 0
    
    elif re.match('MA圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MA(usespeak)))
        return 0
    
    elif re.match('MACD圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MACD(usespeak)))
        return 0
    
    elif re.match('OBV圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_OBV(usespeak)))
        return 0
    
    elif re.match('威廉圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_William(usespeak)))
        return 0
    
    elif re.match('ATR圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
       
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ATR(usespeak)))
        return 0
    
    elif re.match('ADX圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
     
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ADX(usespeak)))
        return 0
    
    elif re.match('RSI圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
    
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_RSI(usespeak)))
        return 0
    
    elif re.match('MFI圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
     
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_MFI(usespeak)))
        return 0
    
    elif re.match('ROC圖',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        line_bot_api.push_message(uid, TextSendMessage(Technical_Analysis.stock_ROC(usespeak)))
        return 0
    elif re.match('毛利率大於90％',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        line_bot_api.push_message(uid,TextSendMessage('毛利率大於90％的股票：\n'+Fundamental_Analysis.gpm()))
        return 0
    
    elif re.match('每股淨值大於100',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        line_bot_api.push_message(uid,TextSendMessage('每股淨值大於100的股票：\n'+Fundamental_Analysis.pbr()))
        return 0
    
    elif re.match('每股盈餘大於5',usespeak): 
        usespeak=mongodb.cache_temporary_stock(uid)
        line_bot_api.push_message(uid, TextSendMessage('稍等一下, 雲端運算中...'))
        line_bot_api.push_message(uid,TextSendMessage('每股盈餘大於5的股票：\n'+Fundamental_Analysis.eps()))
        return 0
    elif re.match('技術面分析',usespeak):
        message = TemplateSendMessage(
            alt_text='技術面分析（Technical Analysis）',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/7FwK6MA.png',
                        title='技術面分析',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='ROC圖',
                                text='ROC圖'
                            ),
                            MessageTemplateAction(
                                label='MA圖',
                                text='MA圖'
                            ),
                            MessageTemplateAction(
                                label='MACD圖',
                                text='MACD圖'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/9BlDjoF.png',
                        title='技術面分析',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='OBV圖',
                                text='OBV圖'
                            ),
                            MessageTemplateAction(
                                label='威廉圖',
                                text='威廉圖'
                            ),
                            MessageTemplateAction(
                                label='ATR圖',
                                text='ATR圖'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/OkpeEZ7.png',
                        title='技術面分析',
                        text='Technical Analysis',
                        actions=[
                            MessageTemplateAction(
                                label='ADX圖',
                                text='ADX圖'
                            ),
                            MessageTemplateAction(
                                label='RSI圖',
                                text='RSI圖'
                            ),
                            MessageTemplateAction(
                                label='MFI圖',
                                text='MFI圖'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.push_message(uid, message)
        return 0
    elif re.match('基本面分析',usespeak): 
        buttons_template = TemplateSendMessage(
            alt_text='基本面分析',
            template=ButtonsTemplate(
                title='基本面分析（Fundamental Analysis）',
                text='請選擇',
                actions=[
                    MessageTemplateAction(
                        label='毛利率大於90％',
                        text='毛利率大於90％'
                    ),
                    MessageTemplateAction(
                        label='每股淨值大於100',
                        text='每股淨值大於100'
                    ),
                    MessageTemplateAction(
                        label='每股盈餘大於5',
                        text='每股盈餘大於5'
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

