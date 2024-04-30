py3file <sfile>:h:h/python3/copilot-chat.py
python3 import vim

let g:copilot_chat_message_histories = []
let g:copilot_chat_machine_id = ''
let g:copilot_chat_token = {}
let g:copilot_chat_session_id = ''

" Actually, I want to use vim9script,
" but vim.eval('a:prompt') doesn't work (other scopes also don't work).
function! CopilotChatStartAsking(prompt)
  let start = line("'<")
  let end = line("'>")
  python3 copilot_chat_start_asking(vim.eval('a:prompt'), vim.eval('l:start'), vim.eval('l:end'))
endfunction

function! CopilotChatReask(prompt)
  python3 copilot_chat_reask(vim.eval('a:prompt'))
endfunction

command! -range -nargs=1 CS :call CopilotChatStartAsking(<f-args>)
command! -range -nargs=1 CR :call CopilotChatReask(<f-args>)
