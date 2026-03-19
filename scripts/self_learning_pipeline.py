import asyncio
import csv
from datetime import datetime
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Setup path so we can import app
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import get_db, async_session_maker
from app.db.models import UncertaintyPool, UserFeedback, DatasetRegistry


def generate_synthetic_fakes(text: str) -> list[str]:
    """
    Placeholder function for Data Augmentation (Phase 3).
    In a full version, this uses an LLM (GPT-4 or LLaMA) to automatically 
    generate paraphrases of confirmed fakes to enlarge the dataset.
    """
    return [
        f"Synthetic variation 1 of: {text[:50]}...",
        f"Synthetic variation 2 of: {text[:50]}..."
    ]


async def run_pipeline():
    """
    1. Queries `UncertaintyPool` where confidence is between 0.35 and 0.65.
    2. Merges verified `UserFeedback`.
    3. Exports to CSV for auto-retraining.
    """
    print("Starting Self-Learning Pipeline...")
    
    async with async_session_maker() as session:
        # Fetch items from UncertaintyPool with their feedback
        stmt = select(UncertaintyPool, UserFeedback).join(
            UserFeedback, UncertaintyPool.id == UserFeedback.pool_id
        ).where(
            UncertaintyPool.confidence >= 0.35,
            UncertaintyPool.confidence <= 0.65
        )
        
        result = await session.execute(stmt)
        records = result.all()
        
        if not records:
            print("No verified feedback found in the uncertainty pool to process.")
            return

        print(f"Found {len(records)} feedback items for retraining.")
        
        # Prepare dataset
        dataset_path = os.path.join("data", f"retrain_dataset_{datetime.now().strftime('%Y%m%d')}.csv")
        os.makedirs("data", exist_ok=True)
        
        added_count = 0
        with open(dataset_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["text", "verdict", "source_confidence", "augmented"])
            
            for pool_item, feedback in records:
                # If user disagrees with 'SUSPICIOUS', we might need logic to decide if it's REAL or FAKE.
                # Assuming simple setup: 'Agree' means it's FAKE, 'Disagree' means it's REAL.
                final_label = "FAKE" if feedback.user_validation == "Agree" else "REAL"
                
                writer.writerow([pool_item.text, final_label, pool_item.confidence, False])
                added_count += 1
                
                # If we confirmed it's FAKE, generate synthetic data to augment
                if final_label == "FAKE":
                    synthetic_texts = generate_synthetic_fakes(pool_item.text)
                    for stext in synthetic_texts:
                        writer.writerow([stext, "FAKE", 0.99, True])
                        added_count += 1
        
        print(f"Generated {added_count} samples for retraining. Saved to {dataset_path}")
        
        # Register dataset in DB
        registry_entry = DatasetRegistry(
            version=f"v_{datetime.now().strftime('%Y%m%d')}",
            samples_count=added_count
        )
        session.add(registry_entry)
        await session.commit()
        print("Pipeline execution completed successfully.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
