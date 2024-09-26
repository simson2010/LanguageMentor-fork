import gradio as gr  # 导入 Gradio 库，用于构建用户界面
from agents.conversation_agent import ConversationAgent  # 导入对话代理类
from agents.scenario_agent import ScenarioAgent  # 导入场景代理类
from utils.logger import LOG  # 导入日志记录工具

from utils.config import all_models

# 创建对话代理实例
conversation_agent = ConversationAgent() 

current_model = all_models[0]
current_scenario = "job_interview"
# 定义场景代理的选择与调用
agents = {
    "job_interview": ScenarioAgent("job_interview"),  # 求职面试场景代理
    "hotel_checkin": ScenarioAgent("hotel_checkin"),  # 酒店入住场景代理
    # "salary_negotiation": ScenarioAgent("salary_negotiation"),  # 薪资谈判场景代理（注释掉）
    "renting": ScenarioAgent("renting"),  # 租房场景代理（注释掉）
    "travel_planning": ScenarioAgent("travel_planning")  # 旅行规划场景代理
}


def update_current_scenario(scenario_name):
    global current_scenario
    current_scenario = scenario_name
    LOG.info(f"[SCENARIO]: {current_scenario}")
    return (get_scenario_intro(current_scenario), start_new_scenario_chatbot(current_scenario))
    

def update_current_model(model_name):
    global current_model
    current_model = model_name
    LOG.info(f"[ChatModel]: {current_model}")
    agents[current_scenario].update_model(current_model)
    get_scenario_intro(current_scenario)
    start_new_scenario_chatbot(current_scenario)

def clear_history():
    LOG.info(f"[Clear]: Begin clear history for {current_scenario}")
    current_agent = agents[current_scenario]
    current_agent.clear_history()
    print(scenario_chatbot)
    return start_new_scenario_chatbot(current_scenario)

# 处理用户对话的函数
def handle_conversation(user_input, chat_history):
    bot_message = conversation_agent.chat_with_history(user_input)  # 获取聊天机器人的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录聊天机器人的回复
    return bot_message  # 返回机器人的回复

# 获取场景介绍的函数
def get_scenario_intro(scenario):
    with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:  # 打开对应场景的介绍文件
        scenario_intro = file.read().strip()  # 读取文件内容并去除多余空白
    return scenario_intro  # 返回场景介绍内容

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario, clear):
    LOG.info(f"[user_input]: {user_input}")
    LOG.info(f"[Clear]: {clear}")
    LOG.info(f"[scenario]: {scenario}")
    LOG.info(f"[chat_history]: {chat_history}") 

    bot_message = agents[scenario].chat_with_history(user_input)  # 获取场景代理的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录场景代理的回复
    return bot_message  # 返回场景代理的回复

# Gradio 界面构建
with gr.Blocks(title="LanguageMentor 英语私教") as language_mentor_app:
    with gr.Tab("场景训练"):  # 场景训练标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        scenario_radio = gr.Radio(
            choices=[
                ("求职面试", "job_interview"),  # 求职面试选项
                ("酒店入住", "hotel_checkin"),  # 酒店入住选项
                # ("薪资谈判", "salary_negotiation"),  # 薪资谈判选项（注释掉）
                ("租房", "renting"),  # 租房选项（注释掉）
                ("旅行规划", "travel_planning")  # 旅行规划选项
            ], 
            label="场景"  # 单选框标签
        )

        scenario_intro = gr.Markdown()  # 场景介绍文本组件
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>选择场景后开始对话吧！",  # 聊天机器人的占位符
            height=350,  # 聊天窗口高度
        )

        # 获取场景介绍并启动新会话的函数
        def start_new_scenario_chatbot(scenario):
            LOG.info(f"[Start]: Begin start new scenario chatbot for {scenario}")
            initial_ai_message = agents[current_scenario].start_new_session()  # 启动新会话并获取初始AI消息

            return gr.Chatbot(
                value=[(None, initial_ai_message)],  # 设置聊天机器人的初始消息
                height=350,  # 聊天窗口高度
            )
        
        # 更新场景介绍并在场景变化时启动新会话
        scenario_radio.change(
            fn=lambda s: (update_current_scenario(s)),  # 更新场景介绍和聊天机器人
            inputs=scenario_radio,  # 输入为选择的场景
            outputs=[scenario_intro, scenario_chatbot],  # 输出为场景介绍和聊天机器人组件
        )

        btn_clear = gr.Button("清除历史记录")
        btn_clear.click(fn=lambda: clear_history(), inputs=None, outputs=[scenario_chatbot])
        # 场景聊天界面
        gr.ChatInterface(
            fn=handle_scenario,  # 处理场景聊天的函数
            chatbot=scenario_chatbot,  # 聊天机器人组件
            additional_inputs= [scenario_radio,btn_clear] ,  # 额外输入为场景选择
            retry_btn=None,  # 不显示重试按钮
            undo_btn=None,  # 不显示撤销按钮
            clear_btn=None,  # 清除历史记录按钮文本
            submit_btn="发送",  # 发送按钮文本
        )
        # clearButton.click(fn=lambda: clear_history(), inputs=None, outputs=None)


    with gr.Tab("对话练习"):  # 对话练习标签
        gr.Markdown("## 练习英语对话 ")  # 对话练习说明
        conversation_chatbot = gr.Chatbot(
            placeholder="<strong>你的英语私教 DjangoPeng</strong><br><br>想和我聊什么话题都可以，记得用英语哦！",  # 聊天机器人的占位符
            height=800,  # 聊天窗口高度
        )

        gr.ChatInterface(
            fn=handle_conversation,  # 处理对话的函数
            chatbot=conversation_chatbot,  # 聊天机器人组件
            retry_btn=None,  # 不显示重试按钮
            undo_btn=None,  # 不显示撤销按钮
            clear_btn="清除历史记录",  # 清除历史记录按钮文本
            submit_btn="发送",  # 发送按钮文本
        )

    with gr.Tab("模型列表配置"):
        gr.Markdown("## 模型列表配置")
        model_list = gr.Radio(
            choices=[model.name for model in all_models],
            label="模型列表"
        )

        model_list.change(
            fn=lambda s: (update_current_model(s)),  # 更新场景介绍和聊天机器人
            inputs=model_list,  # 输入为选择的场景
        )

# 启动应用
if __name__ == "__main__":
    language_mentor_app.launch(share=True, server_name="0.0.0.0")  # 启动 Gradio 应用并共享