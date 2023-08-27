import schedule,sys
from pathlib import Path
from topic_grab import backend
from ai_category import xhs_tesla_notes_backend as note_backend
from ai_category import fill_blank
import asyncio, time
sys.path.append(str(Path(__file__).resolve().parent.parent))

if __name__ == "__main__":
    # schedule.every().day.at("15:06").do(backend.main)
    asyncio.run(backend.main())
    # note_backend.main()
    # fill_blank.fill()
