import vim
import message as m
import cp_token as t

def delete_messages():
    vim.vars['copilot_chat_message_histories'] = []

def cache_message(message):
    vim.vars['copilot_chat_message_histories'].extend({'content': message.content, 'role': message.role})

def get_messages():
    messages = []
    for h in vim.vars['copilot_chat_message_history']:
        messages.append(
                m.Message(
                    h.get('content').decode('utf-8'),
                    h.get('role').decode('utf-8')
                    )
                )
    return messages

def cache_machine_id(machine_id):
    vim.vars['copilot_chat_machine_id'] = machine_id

def get_machine_id():
    return vim.vars['copilot_chat_machine_id'].decode('utf-8')

def cache_token(token):
    vim.vars['copilot_chat_token'] = {'token': token.token, 'expires_at': token.expires_at}

def get_token():
    dict_token = vim.vars['copilot_chat_token']
    if not dict_token.has_key('token'):
        return None
    return t.Token(dict_token['token'].decode('utf-8'), float(dict_token['expires_at']))

def cache_session_id(session_id):
    vim.vars['copilot_chat_session_id'] = session_id

def get_session_id():
    return vim.vars['copilot_chat_session_id'].decode('utf-8')
