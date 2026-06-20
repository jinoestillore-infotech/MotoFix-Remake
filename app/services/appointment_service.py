from app.models.appointment import Appointment
from datetime import datetime

class AppointmentService:
    """Service Layer governing appointments verification and scheduling validations"""

    @staticmethod
    def book_appointment(user_id: int, motorcycle_name: str, plate_number: str, appointment_date: str, appointment_time: str, reason: str):
        """Processes and validates client-side booking requests"""
        if not motorcycle_name or not appointment_date or not appointment_time or not reason:
            return {"success": False, "message": "All fields except Plate Number are required."}

        # Verify date is in the future
        try:
            target_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            if target_date < datetime.today().date():
                return {"success": False, "message": "Appointments cannot be booked on past dates."}
        except ValueError:
            return {"success": False, "message": "Invalid date format submitted."}

        try:
            Appointment.create(
                user_id=user_id,
                motorcycle_name=motorcycle_name,
                plate_number=plate_number,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason
            )
            return {"success": True, "message": "Appointment booked successfully! Awaiting assignment."}
        except Exception as e:
            return {"success": False, "message": f"Scheduling failed: {str(e)}"}

    @staticmethod
    def approve_and_assign_mechanic(appointment_id: int, mechanic_id: int):
        """Alias for assign_mechanic to support controller mapping compatibilities"""
        return AppointmentService.assign_mechanic(appointment_id, mechanic_id)

    @staticmethod
    def assign_mechanic(appointment_id: int, mechanic_id: int):
        """
        Validates mechanic schedule limits before confirming a booking assignment.
        Ensures a single mechanic cannot have more than one job at the same date and time.
        """
        appointment = Appointment.find_by_id(appointment_id)
        if not appointment:
            return {"success": False, "message": "Appointment not found."}

        # Enforce conflict schedule checks (only 1 approved/completed appointment per mechanic per time slot)
        is_double_booked = Appointment.check_mechanic_schedule_conflict(
            mechanic_id=mechanic_id,
            appointment_date=appointment['appointment_date'],
            appointment_time=appointment['appointment_time'],
            exclude_appointment_id=appointment_id
        )

        if is_double_booked:
            return {
                "success": False, 
                "message": "This mechanic is already booked for another active or approved repair ticket on this date and time slot!"
            }

        try:
            Appointment.assign_mechanic(appointment_id, mechanic_id, status='Approved')
            return {"success": True, "message": "Appointment successfully approved and assigned to the mechanic!"}
        except Exception as e:
            return {"success": False, "message": f"Assignment failed: {str(e)}"}

    @staticmethod
    def complete_service(appointment_id: int, mechanic_id: int, service_report: str, parts_replaced: str = None):
        """Processes repair completion logs from the mechanic, updating database record status"""
        if not service_report:
            return {"success": False, "message": "Service diagnostic report cannot be empty."}

        appt = Appointment.find_by_id(appointment_id)
        if not appt or appt['mechanic_id'] != mechanic_id:
            return {"success": False, "message": "Ticket assignment mismatch or unauthorized request."}

        try:
            Appointment.submit_report(appointment_id, service_report, parts_replaced)
            return {"success": True, "message": "Service report submitted successfully! Ticket marked as completed."}
        except Exception as e:
            return {"success": False, "message": f"Submission failed: {str(e)}"}

    @staticmethod
    def cancel_appointment(appointment_id: int, user_id: int):
        """Cancels a pending appointment requested by a client"""
        appt = Appointment.find_by_id(appointment_id)
        if not appt or appt['user_id'] != user_id:
            return {"success": False, "message": "Appointment not found or unauthorized access."}

        if appt['status'] != 'Pending':
            return {"success": False, "message": "Only pending appointments can be cancelled."}

        try:
            Appointment.update_status(appointment_id, 'Cancelled')
            return {"success": True, "message": "Your appointment request has been cancelled."}
        except Exception as e:
            return {"success": False, "message": f"Cancellation failed: {str(e)}"}