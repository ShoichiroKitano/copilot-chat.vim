import vim
import os
import os.path
import threading

# setup the python path
current_file_path = vim.eval('expand("<sfile>")') # sfile is plugin/copilot-chat.vim
current_dir = os.path.dirname(os.path.abspath(current_file_path))
python3_dir = os.path.dirname(current_dir) + '/python3'
sys.path.append(python3_dir)

import ask
import buffer
import const
import message as m
import cache

BUFFER_NAME = "[CopilotChat]"

def copilot_chat_start_asking(prompt, start_range, end_range):
    cache.delete_messages()
    messages = [
            m.Message(const.SYSTEM_MESSAGE_ASK, const.MESSAGE_ROLE_SYSTEM),
            active_section_message(
                buffer.current_file_path(),
                buffer.selected_text_from_current_buffer(int(start_range), int(end_range))
                ),
            m.Message(prompt, const.MESSAGE_ROLE_USER),
            ]
    buffer.open_window_with_buffer(BUFFER_NAME, "vsplit")
    answer = ask.ask(messages)
    message = answer.to_message()
    buffer.append_text_to_buffer(BUFFER_NAME, message.content)
    cache.cache_message(message)

def copilot_chat_reask(prompt):
    messages = cache.get_messages()
    messages.append(m.Message(prompt, const.MESSAGE_ROLE_USER))
    answer = ask.ask(messages)
    message = answer.to_message()
    buffer.append_text_to_buffer(BUFFER_NAME, message.content)
    cache.cache_message(message)

def active_section_message(file_path, selected_text):
    content = ""
    content += "Active section: `" + file_path + "`\n"
    extensoin = os.path.splitext(file_path)[1]
    content += "```" + extensoin + "\n"
    for i, line in enumerate(selected_text):
        content += str(i+1) + ": " + line + "\n"
    content += "```"
    return m.Message(content, const.MESSAGE_ROLE_SYSTEM)

