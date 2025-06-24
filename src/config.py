URL = "https://lalafo.kg/kyrgyzstan/avtomobili-s-probegom"
BASE_URL = "https://lalafo.kg"

import logging
logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger: logging.Logger = logging.getLogger(__name__)