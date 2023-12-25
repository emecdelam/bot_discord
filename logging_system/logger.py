from .coloring import Colors
from .log_level import Level
from datetime import datetime
from typing import Optional
__all__ = ['log']
async def log(message_content:str,level:str,text_color:Optional[Colors]="") -> None:
    if level == Level.CRITICAL:
        text_color += Colors.black+Colors.bg.orange
    elif level == Level.ERROR:
        text_color += Colors.black+Colors.bg.red
    if text_color != "":
        print(f'{text_color}[{str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")).ljust(19)}] [{str(level).ljust(8)}] {message_content}{Colors.reset}')
    else:
        print(f'[{str(datetime.now()).ljust(19)}] [{str(level).ljust(8)}] {message_content}{Colors.reset}')
