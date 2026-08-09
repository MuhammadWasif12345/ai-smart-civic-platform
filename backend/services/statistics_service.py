import pandas as pd
import numpy as np
import statistics
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List, Any

from ..models import Complaint

# --------------------------------------------------------------------------------
# STATISTICS ENGINE
# This class fulfills the Batch 4 requirements by using pandas, numpy, and 
# Python's built-in statistics module to calculate meaningful metrics about 
# how quickly the city is resolving complaints.
# --------------------------------------------------------------------------------

class StatisticsEngine:
    
    @staticmethod
    def get_overview_stats(db: Session) -> Dict[str, int]:
        # Simple count queries directly against the database
        total = db.query(Complaint).count()
        open_count = db.query(Complaint).filter(Complaint.status == "Open").count()
        critical_count = db.query(Complaint).filter(Complaint.priority == "Critical").count()
        
        # Calculate how many were resolved in the last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        resolved_recent = db.query(Complaint).filter(
            Complaint.status == "Resolved",
            Complaint.resolved_at >= seven_days_ago
        ).count()
        
        return {
            "total_complaints": total,
            "open_complaints": open_count,
            "critical_priority": critical_count,
            "resolved_this_week": resolved_recent
        }

    @staticmethod
    def get_category_distribution(db: Session) -> List[Dict[str, Any]]:
        # We load the data into a pandas DataFrame because pandas is fantastic
        # at grouping and summarizing data.
        complaints = db.query(Complaint.category).all()
        if not complaints:
            return []
            
        # Create a DataFrame (like a virtual Excel spreadsheet)
        df = pd.DataFrame(complaints, columns=["category"])
        
        # Group by category, count them, and reset the index to make it a flat table again
        counts = df.groupby("category").size().reset_index(name='count')
        
        # Calculate the percentage for each row
        total = counts['count'].sum()
        counts['percentage'] = (counts['count'] / total * 100).round(1)
        
        # Convert the DataFrame back into a list of dictionaries for our API to send out
        return counts.to_dict('records')

    @staticmethod
    def get_priority_distribution(db: Session) -> List[Dict[str, Any]]:
        # Same approach as categories, but simpler since we don't need percentages
        complaints = db.query(Complaint.priority).all()
        if not complaints:
            return []
            
        df = pd.DataFrame(complaints, columns=["priority"])
        counts = df.groupby("priority").size().reset_index(name='count')
        return counts.to_dict('records')

    @staticmethod
    def get_resolution_time_stats(db: Session) -> Dict[str, Any]:
        """
        The core of the Batch 4 requirement. Calculates central tendency, spread,
        and quartiles for how long it takes to resolve a complaint.
        """
        # We only care about complaints that are actually finished
        resolved_complaints = db.query(Complaint.created_at, Complaint.resolved_at).filter(
            Complaint.status == "Resolved",
            Complaint.resolved_at != None
        ).all()
        
        # If there aren't enough finished complaints yet, we can't do meaningful math
        if len(resolved_complaints) < 2:
            return {
                "mean_hours": 0.0, "median_hours": 0.0, "mode_hours": 0.0,
                "std_dev_hours": 0.0, "variance": 0.0, "min_hours": 0.0,
                "max_hours": 0.0, "range_hours": 0.0, "q1_hours": 0.0,
                "q3_hours": 0.0, "iqr_hours": 0.0,
                "interpretation": "Not enough resolved complaints to calculate statistics yet."
            }
            
        # Calculate the time taken (in hours) for each complaint
        resolution_times = []
        for c in resolved_complaints:
            time_diff = c.resolved_at - c.created_at
            hours = time_diff.total_seconds() / 3600
            # We round to 1 decimal place to keep the numbers readable
            resolution_times.append(round(hours, 1))
            
        # Convert our list into a numpy array for advanced mathematical operations
        arr = np.array(resolution_times)
        
        # --- CENTRAL TENDENCY ---
        # Mean (Average): The sum of all times divided by the count. Can be skewed by outliers.
        mean_val = round(np.mean(arr), 1)
        # Median: The exact middle value. Good because it's not affected by extreme outliers.
        median_val = round(np.median(arr), 1)
        
        # Mode: The most common value. We use Python's built-in statistics module for this.
        try:
            mode_val = round(statistics.mode(resolution_times), 1)
        except statistics.StatisticsError:
            # If all values are unique, there is no single mode
            mode_val = mean_val 
            
        # --- SPREAD / VARIANCE ---
        # Standard Deviation: How much the values typically stray from the mean.
        # ddof=1 means we treat this as a sample of a larger population.
        std_dev = round(np.std(arr, ddof=1), 1)
        # Variance: Standard deviation squared.
        variance = round(np.var(arr, ddof=1), 1)
        
        min_val = round(np.min(arr), 1)
        max_val = round(np.max(arr), 1)
        range_val = round(max_val - min_val, 1)
        
        # --- QUARTILES (IQR) ---
        # Percentiles divide the data into 4 equal chunks
        q1 = round(np.percentile(arr, 25), 1)
        q3 = round(np.percentile(arr, 75), 1)
        iqr = round(q3 - q1, 1) # Interquartile range (the middle 50% of the data)
        
        # --- PLAIN ENGLISH INTERPRETATION ---
        # The prompt requires us to explain what these numbers actually mean to a human.
        if mean_val > median_val * 1.5:
            # If the mean is way higher than the median, a few terrible outliers are dragging it up
            interp = f"While most complaints are resolved around {median_val} hours, a few extremely delayed cases are pulling our overall average up to {mean_val} hours."
        elif iqr < 5.0:
            # If the IQR is tight, the team is very consistent
            interp = f"The service team is highly consistent. Most complaints are resolved within a tight window of {q1} to {q3} hours (average {mean_val} hours)."
        else:
            interp = f"The typical resolution time is {median_val} hours. 50% of all issues are handled between {q1} and {q3} hours."
            
        return {
            "mean_hours": float(mean_val),
            "median_hours": float(median_val),
            "mode_hours": float(mode_val),
            "std_dev_hours": float(std_dev),
            "variance": float(variance),
            "min_hours": float(min_val),
            "max_hours": float(max_val),
            "range_hours": float(range_val),
            "q1_hours": float(q1),
            "q3_hours": float(q3),
            "iqr_hours": float(iqr),
            "interpretation": interp
        }
