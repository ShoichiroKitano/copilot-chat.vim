import json
import os
import uuid
import time
import random
import http.client

import cp_token as t

def find_oauth_token():
    return _find_oauth_token_from_config('~/.config/github-copilot/hosts.json')

def _find_oauth_token_from_config(path):
    oauth_token = ''
    with open(os.path.expanduser(path)) as f:
        data = json.load(f)
        oauth_token = data['github.com']['oauth_token']
    return oauth_token

def get_token(oauth_token, vim_version, plugin_version):
    headers = {
            'Authorization': 'token ' + oauth_token,
            'Accept': 'application/json',
            'editor-version': 'vim/' + vim_version,
            'editor-plugin-version': 'CopilotChat.vim/' + plugin_version,
            'user-agent': 'CopilotChat.vim/' + plugin_version,
            }

    conn = http.client.HTTPSConnection('api.github.com')
    conn.request('GET', '/copilot_internal/v2/token', headers=headers)
    response = conn.getresponse()
    j = json.loads(response.read().decode('utf-8'))
    conn.close()
    token = t.Token(j['token'], float(j['expires_at']))
    return token

def machine_id():
    id = ''
    hex = '0123456789abcdef'
    for _ in range(65):
        id = id + hex[1: random.randint(0, 15)]
    return id

class CopilotChatClient:

    def __init__(self, oauth_token, machine_id, vim_version, plugin_version):
        self.oauth_token = oauth_token
        self.machine_id = machine_id
        self.vim_version = vim_version
        self.plugin_version = plugin_version
        self.token = ''
        self.session_id = ''

    def post_chat_completions(self, body):
        if self._needs_token_reflesh():
            self._set_token_and_session_id_from_token_api()
        headers = self._request_chat_headers()
        conn = http.client.HTTPSConnection('api.githubcopilot.com')
        conn.request('POST', '/chat/completions', json.dumps(body), headers)
        response = conn.getresponse()
        if response.status != 200:
            exception = Exception('Error: ' + response.reason)
            raise exception
        message = response.read().decode('utf-8')
        conn.close()
        return message

    def _set_token_and_session_id_from_token_api(self):
        self.token = get_token(self.oauth_token, self.vim_version, self.plugin_version)
        self.session_id = str(uuid.uuid4()) + str(int(time.time() * 1000)) # uuid4 + timestamp

    def _needs_token_reflesh(self):
        if self.token == '' or self.token.expired(time.time()):
            return True
        return False

    def _request_chat_headers(self):
        return {
                'authorization': 'Bearer ' + self.token.token,
                'x-request-id': str(uuid.uuid4()),
                'vscode-sessionid': self.session_id,
                'vscode-machineid': self.machine_id,
                'copilot-integration-id': 'vscode-chat',
                'openai-organization': 'github-copilot',
                'openai-intent': 'conversation-panel',
                'content-type': 'application/json',
                'editor-version': 'vim/' + self.vim_version,
                'editor-plugin-version': 'CopilotChat.vim/' + self.plugin_version,
                'user-agent': 'CopilotChat.vim/' + self.plugin_version,
                }



# oauth_token = find_oauth_token()
# token = get_token(oauth_token, '1.0.0', '1.0.0')
# answer = ask(
#         [
#             Message(SYSTEM_MESSAGE_ASK, MESSAGE_ROLE_SYSTEM),
#             Message("Active selection: `/home/sho/project/tag-explorer.vim/plugin/tag-explorer.vim`\n```vim\n1: vim9script\n2: \n```", MESSAGE_ROLE_SYSTEM),
#             Message('What is the purpose of this code?', MESSAGE_ROLE_USER),
#             ]
#         )
# print(answer.to_message()
