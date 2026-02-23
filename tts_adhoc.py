
import asyncio

import edge_tts


text = """
"""

text = text.replace('*', '').replace('#', '')
communicate = edge_tts.Communicate(text, 'zh-CN-XiaoxiaoNeural')
output_path = "./tao.mp3"
asyncio.run(communicate.save(output_path))