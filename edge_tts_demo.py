import asyncio
import edge_tts
import os

# --- 配置区域 ---
TEXT_TO_SAY = "你好，这是一个由 Python 脚本生成的测试音频。你可以随意修改这段文字。"
# 常用角色：zh-CN-XiaoxiaoNeural (女), zh-CN-YunxiNeural (男), zh-CN-XiaoyiNeural (女)
VOICE_NAME = "zh-CN-XiaoxiaoNeural" 
OUTPUT_FILENAME = "local_audio.mp3"
# ----------------

async def generate_audio():
    try:
        # 1. 初始化通信对象
        communicate = edge_tts.Communicate(TEXT_TO_SAY, VOICE_NAME)
        
        # 2. 执行并保存
        print(f"正在转换语音，请稍候...")
        await communicate.save(OUTPUT_FILENAME)
        
        # 3. 确认结果
        full_path = os.path.abspath(OUTPUT_FILENAME)
        print(f"✅ 生成成功！")
        print(f"📍 存放位置: {full_path}")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    # 运行异步任务
    asyncio.run(generate_audio())