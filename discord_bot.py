# 導入Discord.py模組
import discord

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

# 讀取關鍵字與回答對應表的函數
def load_responses(file_path):
    responses = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        current_keyword = None
        for line in lines:
            line = line.strip()
            if line.startswith("#"):  # 關鍵字行
                current_keyword = line[1:].strip()  # 移除 "#"
            elif line.startswith("-") and current_keyword:  # 回答行
                responses[current_keyword] = line[1:].strip()  # 加入字典
    return responses

# 加載關鍵字對應表
responses = load_responses('responses.txt')

# 當機器人啟動時，打印消息
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# 監聽來自頻道中的消息
@client.event
async def on_message(message):
    # 確保機器人不會回應自己的訊息
    if message.author == client.user:
        return
    
    # 檢查消息是否以 "[問] " 開頭
    if message.content.startswith("[問] "):
        # 移除 "[問] " 前綴，留下查詢的關鍵字
        query = message.content[len("[問] "):].strip()
        
        # 將關鍵字以逗號或空格分隔，轉換成清單
        keywords = set([kw.strip() for kw in query.split(" ")])
        
        # 整理回應，遍歷所有關鍵字，檢查是否在訊息內
        response_parts = []
        for keyword in responses:
            if keyword in query:  # 檢查訊息是否包含關鍵字
                answer = responses.get(keyword)
                response_parts.append(f"{keyword}: {answer}")
            
        # 如果有匹配的關鍵字，則組合回應並發送
        if response_parts:
            full_response = "\n".join(response_parts)
            # 回應用戶，並 @ 提及發送訊息的用戶
            await message.channel.send(f'{message.author.mention} \n{full_response}')
        else:
            # 如果沒有找到匹配的關鍵字，可以選擇不回覆或回覆一個預設消息
            await message.channel.send(f'{message.author.mention} 抱歉，未能找到匹配的關鍵字。')

# 使用你的機器人 Token 啟動機器人
client.run('YOUR TOKEN')