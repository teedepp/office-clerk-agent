from backend.database import get_db
from backend.models import LeaveRequestDB, CertificateRequestDB

class LeaveAgent:
    def __init__(self, db):
        self.db = db

    def get_leave_requests(self, employee_id):
        """Fetch leave requests for a specific employee."""
        leave_requests = self.db.query(LeaveRequestDB).filter(LeaveRequestDB.employee_id == employee_id).all()
        if not leave_requests:
            return "No leave records found for this employee."
        return [{"id": leave.id, "leave_type": leave.leave_type, "start_date": leave.start_date, "end_date": leave.end_date, "reason": leave.reason} for leave in leave_requests]

class CertificateAgent:
    def __init__(self, db):
        self.db = db

    def generate_certificate(self, cert_data):
        """Process certificate generation request."""
        new_cert = CertificateRequestDB(**cert_data)
        self.db.add(new_cert)
        self.db.commit()
        self.db.refresh(new_cert)
        return {"message": "Certificate request submitted successfully", "certificate": new_cert}

def get_agents(db):
    return {
        "leave_agent": LeaveAgent(db),
        "cert_agent": CertificateAgent(db),
    }
