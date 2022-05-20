from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
import urllib
import json
import requests

from .models import Reply, Translatelog

WEBHOOK_URL = 'https://hooks.slack.com/services/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'
VERIFICATION_TOKEN = 'XtILwDM60IqiCfB6AmiQj37U'
ACTION_DEEPL = 'EN-US'
DEEPL_API_KEY = 'c9dde83d-18ca-df0e-cff2-bdc10b0b424d:fx'

language = {"BG":"ブルガリア語","CS":"チェコ語","DA":"デンマーク語","DE":"ドイツ語","EL":"ギリシャ語","EN-GB":"英語（イギリス）","EN-US":"英語（アメリカ）","ES":"スペイン語","ET":"エストニア語","FI":"フィンランド語","FR":"フランス語","HU":"ハンガリー語","ID":"インドネシア語","IT":"イタリア語","JA":"日本語","LT":"リトアニア語","LV":"ラトビア語","NL":"オランダ語","PL":"ポーランド語","PT-PT":"ポルトガル語（ブラジルポルトガル語を除くすべてのポルトガル語の品種）","PT-BR":"ポルトガル語（ブラジル）","RO":"ルーマニア語","RU":"ロシア語","SK":"スロバキア語","SL":"スロベニア語","SV":"スウェーデン語","TR":"トルコ語","ZH":"中国語"}

def index(request):
    positive_replies = Reply.objects.filter(response=Reply.POSITIVE)
    neutral_replies = Reply.objects.filter(response=Reply.NEUTRAL)
    negative_replies = Reply.objects.filter(response=Reply.NEGATIVE)
    translatelogs = Translatelog.objects.all()

    context = {
        'positive_replies': positive_replies,
        'neutral_replies': neutral_replies,
        'negative_replies': negative_replies,
        'translatelogs': translatelogs
    }
    return render(request, 'index.html', context)

def clear(request):
    Translatelog.objects.all().delete()
    return redirect(index)

def announce(request):
    if request.method == 'POST':
        data = {
            'text': request.POST['message']
        }
        post_message(WEBHOOK_URL, data)

    return redirect(index)

@csrf_exempt
def echo(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    print(request.POST)

    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    content = request.POST['text']
    try:
        target_lang = 'EN-US'
        target_lang_name = language[target_lang]

        params = {
                'auth_key' : DEEPL_API_KEY,
                'text' : content,
                'target_lang': target_lang
        }

        request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
        deepl_result = request.json()["translations"][0]["text"]
        deepl_sourse_result = request.json()["translations"][0]["detected_source_language"]
        source_lang_name = language[deepl_sourse_result]
        translate_log = Translatelog(user_name=user_name, user_id=user_id, origin_text=content, deepl_text=deepl_result, source_lang=source_lang_name, target_lang=target_lang_name)
        translate_log.save()

    except:
        deepl_result = 'error!'

    result = {
        'response_type': 'in_channel',
	    'blocks': [
		    {
			    "type": "divider"
		    },
            {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": '<@{}>'.format(user_id)
				}
			]
		},
		    {
			    "type": "context",
			    "elements": [
				    {
					    "type": "image",
					    "image_url": "https://2.bp.blogspot.com/-5iAeI3keuUc/WQA-LdnYJnI/AAAAAAABD5s/N7JKSqu2EMA52fN1wNgP8GmxGKJ2wkHhwCLcB/s400/pose_atama_kakaeru_man.png",
					    "alt_text": "in trouble"
				    },
				    {
					    "type": "mrkdwn",
					    "text": '「{}」'.format(content) + 'を' + '{}'.format(target_lang_name) + 'に翻訳したい!!'
				    }
			    ]
		    },
		    {
			    "type": "divider"
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": '{}'.format(deepl_result)
			    },
			    "accessory": {
				"type": "image",
				"image_url": "https://i.imgur.com/bGxNjXm.png",
				"alt_text": "robot_ilust"
			    }
		    },
            {
			    "type": "divider"
		    }
	    ]
    }
    return JsonResponse(result)

@csrf_exempt
def hello(request):
    if request.method != 'POST':
        return JsonResponse({})
    
    if request.POST.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    user_name = request.POST['user_name']
    user_id = request.POST['user_id']
    content = request.POST['text']

    result = {
        'blocks': [
            {
                'type' : 'section',
                'text' : {
                    'type': 'mrkdwn',
                    'text': '{}'.format(content)
                },
                'accessory': {
                    'type': 'static_select',
                    'placeholder': {
                        'type': 'plain_text',
                        'text': '翻訳先',
                        'emoji': True
                    },
                    'options': [
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '英語（アメリカ）',
                                'emoji': True
                            },
                            'value': 'EN-US'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '中国語',
                                'emoji': True
                            },
                            'value': 'ZH'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ドイツ語',
                                'emoji': True
                            },
                            'value': 'DE'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ブルガリア語',
                                'emoji': True
                            },
                            'value': 'BG'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'チェコ語',
                                'emoji': True
                            },
                            'value': 'CS'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'デンマーク語',
                                'emoji': True
                            },
                            'value': 'DA'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ギリシャ語',
                                'emoji': True
                            },
                            'value': 'EL'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': '英語（イギリス）',
                                'emoji': True
                            },
                            'value': 'EN-GB'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'スペイン語',
                                'emoji': True
                            },
                            'value': 'DE'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'エストニア語',
                                'emoji': True
                            },
                            'value': 'ET'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'フィンランド語',
                                'emoji': True
                            },
                            'value': 'FI'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'フランス語',
                                'emoji': True
                            },
                            'value': 'FR'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ハンガリー語',
                                'emoji': True
                            },
                            'value': 'HU'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'インドネシア語',
                                'emoji': True
                            },
                            'value': 'ID'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'イタリア語',
                                'emoji': True
                            },
                            'value': 'IT'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'リトアニア語',
                                'emoji': True
                            },
                            'value': 'LT'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ラトビア語',
                                'emoji': True
                            },
                            'value': 'LV'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'オランダ語',
                                'emoji': True
                            },
                            'value': 'NL'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ポーランド語',
                                'emoji': True
                            },
                            'value': 'PL'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ポルトガル語（ブラジルポルトガル語を除くすべてのポルトガル語の品種）',
                                'emoji': True
                            },
                            'value': 'PT-PT'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ポルトガル語（ブラジル）',
                                'emoji': True
                            },
                            'value': 'PT-BR'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ルーマニア語',
                                'emoji': True
                            },
                            'value': 'RO'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'ロシア語',
                                'emoji': True
                            },
                            'value': 'RU'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'スロバキア語',
                                'emoji': True
                            },
                            'value': 'SK'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'スロベニア語',
                                'emoji': True
                            },
                            'value': 'SL'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'スウェーデン語',
                                'emoji': True
                            },
                            'value': 'SV'
                        },
                        {
                            'text': {
                                'type': 'plain_text',
                                'text': 'トルコ語',
                                'emoji': True
                            },
                            'value': 'TR'
                        }
                    ],
                    'action_id': ACTION_DEEPL
                }
            }
        ],
        'response_type': 'in_channel'
    }

    return JsonResponse(result)

@csrf_exempt
def reply(request):
    if request.method != 'POST':
        return JsonResponse({})

    payload = json.loads(request.POST.get('payload'))
    print(payload)
    if payload.get('token') != VERIFICATION_TOKEN:
        raise SuspiciousOperation('Invalid request.')
    
    if payload['actions'][0]['action_id'] != ACTION_DEEPL:
        raise SuspiciousOperation('Invalid request.')
    
    print(payload)
    user = payload['user']['username']
    print(user)
    user_id = payload['user']['id']
    print(user_id)
    selected_value = payload['actions'][0]['selected_option']['value']
    print(selected_value)
    response_url = payload['response_url']
    print(response_url)
    content = payload['message']['blocks'][0]['text']['text']
    print(content)
    try:
        source_lang = 'JA'
        target_lang = selected_value
        source_lang_name = language[source_lang]
        target_lang_name = language[target_lang]

        params = {
                'auth_key' : DEEPL_API_KEY,
                'text' : content,
                'source_lang' : source_lang,
                'target_lang': target_lang
        }

        request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
        deepl_result = request.json()["translations"][0]["text"]
        translate_log = Translatelog(user_name=user, user_id=user_id, origin_text=content, deepl_text=deepl_result, source_lang=source_lang_name, target_lang=target_lang_name)
        translate_log.save()

    except:
        deepl_result = 'error!!'
    
    response = {
        'response_type': 'in_channel',
	    'blocks': [
		    {
			    "type": "divider"
		    },
            {
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": '<@{}>'.format(user_id)
				}
			]
		},
		    {
			    "type": "context",
			    "elements": [
				    {
					    "type": "image",
					    "image_url": "https://2.bp.blogspot.com/-5iAeI3keuUc/WQA-LdnYJnI/AAAAAAABD5s/N7JKSqu2EMA52fN1wNgP8GmxGKJ2wkHhwCLcB/s400/pose_atama_kakaeru_man.png",
					    "alt_text": "in trouble"
				    },
				    {
					    "type": "mrkdwn",
					    "text": '「{}」'.format(content) + 'を' + '{}'.format(target_lang_name) + 'に翻訳したい!!'
				    }
			    ]
		    },
		    {
			    "type": "divider"
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": '{}'.format(deepl_result)
			    },
			    "accessory": {
				"type": "image",
				"image_url": "https://i.imgur.com/bGxNjXm.png",
				"alt_text": "robot_ilust"
			    }
		    },
            {
			    "type": "divider"
		    }
	    ]
    }
    
    post_message(response_url, response)
    return JsonResponse({})

def post_message(url, data):
    headers = {
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read()