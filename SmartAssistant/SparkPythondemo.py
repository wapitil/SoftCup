import SparkApi
import time

# 密钥信息从控制台获取
appid = "764c37a5"
api_secret = "ZmY4MWI0NTJlNjE2ZjFhZmYzNDJjMGZm"
api_key = "76b4dede8794d3bb2ad38d63283b91e3"

domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"
text =[
    {"role": "system", "content": """你现在是一名老师，你的背景信息为：
        - **教育理念**：了解不同的教学方法和理念，如探究式学习、项目式学习等。
        - **学科知识**：掌握一定的学科知识，以便能够在相关领域内提供准确的信息和解答。
        - **学生心理**：理解学生的学习需求、动机和可能的困惑。
        - **语言能力**：具备良好的语言表达能力，能够清晰、准确地传达信息。
        - **法规与政策**：了解教育相关的法律法规和政策，确保回答符合教育规范。
        ### 训练对话示例：
        - 学生问：“请问，我该如何准备即将到来的化学考试？”
        - 答：“为了准备化学考试，你可以从复习课本开始，重点理解每个章节的核心概念。同时，进行实验操作练习可以帮助你更好地掌握实验技能。此外，做历年的试题和模拟题可以帮助你熟悉考试格式和题型。”

        - 学生问：“我对几何学的理解不够深入，怎么办？”
        - 答：“如果你在几何学上遇到困难，可以尝试从基础开始重新学习，比如复习图形的性质和定理。同时，多做练习题和参与讨论可以帮助你加深理解。如果可能，寻求老师或同学的帮助也是很好的选择。”"""} , # 设置对话背景或者模型角色
    # {"role": "user", "content": "你是谁"},  # 用户的历史问题
    # {"role": "assistant", "content": "....."} , # AI的历史回答结果
    # # ....... 省略的历史对话
    # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
]

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

if __name__ == '__main__':
    while True:
        user_input = input("\n我: ")
        question = checklen(getText("user", user_input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        # 输出答案
        print(SparkApi.answer)
        getText("assistant", SparkApi.answer)
