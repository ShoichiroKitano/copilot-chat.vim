import const
import message
import json

class Answer:
    def __init__(self, content):
        self.content = content

    def to_message(self):
        message_content = ''
        for a in self.content.split('\n'):
            if a == '' or a == 'data: [DONE]':
                continue
            else:
                ajson = a.replace('data: ', '')
                adict = json.loads(ajson)
                if len(adict['choices']) == 0:
                    continue
                delta_content = adict['choices'][0]['delta']['content']
                if delta_content == None:
                    continue
                message_content = message_content + delta_content
        return message.Message(message_content, const.MESSAGE_ROLE_ASSISTANT)
