import client as ch
import vim
import answer
import cache

def ask(messages):
    machine_id = cache.get_machine_id()
    if machine_id == '':
        machine_id = ch.machine_id()
        cache.cache_machine_id(machine_id)
    client = ch.CopilotChatClient(ch.find_oauth_token(), machine_id, vim.eval('v:version'), '0.0.1')
    token = cache.get_token()
    if token != None:
        client.token = token
        client.session_id = cache.get_session_id()
    messages_dists = list(map(lambda m: {'role': m.role, 'content': m.content}, messages))
    body = {
            'model': 'gpt-4',
            'temperature': 0.1,
            'top_p': 1,
            'n': 1,
            'intent': True,
            'stream': True,
            'messages': messages_dists,
            }
    ans = answer.Answer(client.post_chat_completions(body))
    cache.cache_token(client.token)
    cache.cache_session_id(client.session_id)
    return ans
