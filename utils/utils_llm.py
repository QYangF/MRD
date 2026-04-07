def llm_qianfan(massage):
    MODEL = "ERNIE Speed"
    chat_comp = qianfan.ChatCompletion(model=MODEL)
    
    resp = chat_comp.do(
        messages=massage,
        top_p=0.8,
        temperature=0.3,
        penalty_score=1.0
    )
    return resp

def send_message(role,user_input):

    MODEL = "ernie-bot-4"
    chat_comp = qianfan.ChatCompletion(model=MODEL)
    message=[{"role":role,"content":user_input}]
    resp={}
    try:
        resp = chat_comp.do(
        messages=message,
        top_p=0.8,
        temperature=0.3,
        penalty_score=1.0
        )
 
        return resp
    except Exception as e :
   
        return resp

