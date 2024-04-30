import vim

copilot_chat_buffer = None

def selected_text_from_current_buffer(start, end):
    # start = vim.current.range.start
    # end = vim.current.range.end
    # return vim.current.buffer[start:end+1]
    return vim.current.buffer[start-1:end]

def current_file_path():
    return vim.current.buffer.name

def open_window_with_buffer(bufffe_name, split="vsplit"):
    vim.command(split)
    vim.command("e " + bufffe_name)
    vim.command("setlocal buftype=nofile bufhidden=hide noswapfile")

def append_text_to_buffer(buffer_name, text):
    for buffer in vim.buffers:
        if buffer.name.endswith(buffer_name):
            for t in text.split('\n'):
                if buffer[0] == '':
                    buffer[0] = t
                else:
                    buffer.append(t)
            buffer.append('')
            break

# open_window_with_buffer("[CopilotChat]")
# append_text_to_buffer("[CopilotChat]", "Hello World")
# append_text_to_buffer("[CopilotChat]", "")
