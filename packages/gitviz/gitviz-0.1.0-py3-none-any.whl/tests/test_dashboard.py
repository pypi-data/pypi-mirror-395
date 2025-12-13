import pandas as pd
from datetime import datetime
import tempfile
import os

from gitviz.dashboard import create_activity_gif


def test_create_activity_gif_basic():
    data = [
        {"commit":"a","author_name":"Alice","date":datetime(2022,1,1,12,0),"message":"fix"},
        {"commit":"b","author_name":"Bob","date":datetime(2022,1,2,12,0),"message":"add"},
        {"commit":"c","author_name":"Alice","date":datetime(2022,1,3,12,0),"message":"update"},
    ]
    df = pd.DataFrame(data)
    # ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])
    tmp = tempfile.gettempdir()
    gif_path = os.path.join(tmp, "test_gitviz_activity.gif")
    if os.path.exists(gif_path):
        os.remove(gif_path)
    create_activity_gif(df, gif_path)
    assert os.path.exists(gif_path)
*** End Patch