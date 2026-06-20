from app.models.appointment import Appointment
from datetime import datetime

class AppointmentService:
    """Service layer validating schedules, bounds checks, and booking constraints"""

    @staticmethod
    def book_new(user_id: int, motorcycle_name: str, plate_number: str, reason: str, appointment_date: str, appointment_time: str):
        """Validates input fields and commits appointment parameters"""
        # Mandatory validation check
        if not motorcycle_name or not reason or not appointment_date or not appointment_time:
            return {"success": False, "message": "Motorcycle details, reason, date, and target time are required."}

        try:
            # 1. Parse and ensure appointment date matches valid format
            target_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            today = datetime.now().date()

            # 2. Block booking sessions on back-dated or historic timestamps
            if target_date < today:
                return {"success": False, "message": "Cannot schedule appointments for past dates."}

            # 3. Clean and sanitize plate indicators
            sanitized_plate = plate_number.strip().upper() if plate_number else "N/A"

            # Create Record
            Appointment.create(
                user_id=user_id,
                motorcycle_name=motorcycle_name.strip(),
                plate_number=sanitized_plate,
                reason=reason.strip(),
                appointment_date=appointment_date,
                appointment_time=appointment_time
            )
            return {"success": True, "message": "Your service appointment has been booked successfully!"}

        except ValueError:
            return {"success": False, "message": "Invalid date or time parameter structure received."}
        except Exception as e:
            return {"success": False, "message": f"Service booking failure: {str(e)}"}

    @staticmethod
    def cancel(appointment_id: int, user_id: int):
        """Validates ownership and handles cancellations"""
        appointment = Appointment.find_by_id(appointment_id)
        if not appointment:
            return {"success": False, "message": "Appointment not found."}

        if appointment['user_id'] != user_id:
            return {"success": False, "message": "Unauthorized access request."}

        if appointment['status'] != 'Pending':
            return {"success": False, "message": "Only pending appointments can be cancelled."}

        try:
            Appointment.cancel_appointment(appointment_id, user_id)
            return {"success": True, "message": "Appointment cancelled successfully."}
        except Exception as e:
            return {"success": False, "message": f"Action failed: {str(e)}"}