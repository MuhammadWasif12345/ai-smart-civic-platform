import logging
from ..models import Complaint

# --------------------------------------------------------------------------------
# NOTIFICATION MANAGER
# This service handles sending alerts to citizens when their complaint status changes.
# For this hackathon, we don't need real SMS/Email integration (like Twilio or SendGrid),
# so this class simulates it by logging to the console. However, the architectural 
# structure is here so it could be easily swapped out for real emails later.
# --------------------------------------------------------------------------------

class NotificationManager:
    
    @staticmethod
    def notify_status_change(complaint: Complaint):
        # We only try to notify if the citizen actually provided contact info
        if not complaint.citizen_contact:
            return
            
        contact = complaint.citizen_contact
        status = complaint.status
        cid = complaint.complaint_id
        
        # Build the message based on the new status
        if status == "Assigned":
            msg = f"Update: Your complaint ({cid}) has been assigned to the {complaint.assigned_department}."
        elif status == "In Progress":
            msg = f"Update: The city is actively working on your complaint ({cid}) right now."
        elif status == "Resolved":
            msg = f"Success! Your complaint ({cid}) has been marked as Resolved by our team."
        else:
            msg = f"Update: Your complaint ({cid}) status is now '{status}'."
            
        # Simulate sending the message by printing it to the server logs
        logging.info(f"--- SIMULATED NOTIFICATION TO {contact} ---")
        logging.info(f"Message: {msg}")
        logging.info("---------------------------------------------")
