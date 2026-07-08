from msme_generator import generate_msmes
from risk_model import generate_default
from config import NUM_MSMES, PATH
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("MSME data generation pipeline initiated")
# Generate Feature
msme_df = generate_msmes(NUM_MSMES)
logging.info("Synthetic MSME feature generation completed")

# Generate PD and Default
msme_df = generate_default(msme_df)
logging.info("Risk target generation (PD/Default) completed")

msme_df.to_csv(PATH + "msmes.csv", index = False)
logging.info(f"Dataset successfully saved at: {PATH}")
logging.info("MSME data pipeline execution completed successfully")
