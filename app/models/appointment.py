# project/app/models/appointment.py
from app.database import Database

class Appointment:
    """Model mapping database operations on the 'appointments' table"""

    @staticmethod
    def create(user_id: int, motorcycle_name: str, plate_number: str, appointment_date: str, appointment_time: str, reason: str):
        """Creates a new pending appointment request in the database"""
        query = """
            INSERT INTO appointments (user_id, motorcycle_name, plate_number, appointment_date, appointment_time, reason, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Pending')
        """
        params = (user_id, motorcycle_name, plate_number, appointment_date, appointment_time, reason)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def find_by_id(appointment_id: int):
        """Finds a single appointment detail by its ID"""
        query = "SELECT * FROM appointments WHERE id = %s"
        results = Database.execute_query(query, (appointment_id,))
        return results[0] if results else None

    @staticmethod
    def find_by_user_id(user_id: int):
        """Fetches all appointments booked by a specific client, joining mechanic names if assigned"""
        query = """
            SELECT a.*, u.first_name AS mechanic_first, u.last_name AS mechanic_last
            FROM appointments a
            LEFT JOIN users u ON a.mechanic_id = u.id AND u.role_id = 2
            WHERE a.user_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        return Database.execute_query(query, (user_id,))

    @staticmethod
    def find_all():
        """Fetches all shop appointments for administrative review"""
        query = """
            SELECT a.*, 
                   c.first_name AS client_first, c.last_name AS client_last, c.phone AS client_phone,
                   m.first_name AS mechanic_first, m.last_name AS mechanic_last
            FROM appointments a
            JOIN users c ON a.user_id = c.id
            LEFT JOIN users m ON a.mechanic_id = m.id AND m.role_id = 2
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        return Database.execute_query(query)

    @staticmethod
    def find_by_mechanic_id(mechanic_id: int):
        """Fetches all jobs assigned to a specific mechanic"""
        query = """
            SELECT a.*, 
                   c.first_name AS client_first, c.last_name AS client_last, c.phone AS client_phone
            FROM appointments a
            JOIN users c ON a.user_id = c.id
            WHERE a.mechanic_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
        return Database.execute_query(query, (mechanic_id,))

    @staticmethod
    def update_status(appointment_id: int, status: str):
        """Modifies status state of an appointment (e.g. Approved, Cancelled)"""
        query = "UPDATE appointments SET status = %s WHERE id = %s"
        return Database.execute_query(query, (status, appointment_id), commit=True)
    
    @staticmethod
    def delete(appointment_id: int):
        """Permanently purges an appointment record from the database table"""
        query = "DELETE FROM appointments WHERE id = %s"
        return Database.execute_query(query, (appointment_id,), commit=True)
    
    @staticmethod
    def assign_mechanic(appointment_id: int, mechanic_id: int, status: str = 'Approved'):
        """Assigns a mechanic to an appointment and sets status to Approved"""
        query = "UPDATE appointments SET mechanic_id = %s, status = %s WHERE id = %s"
        return Database.execute_query(query, (mechanic_id, status, appointment_id), commit=True)

    @staticmethod
    def submit_report(appointment_id: int, service_report: str, parts_replaced: str = None):
        """Closes a job ticket with diagnostics reporting info"""
        query = """
            UPDATE appointments 
            SET service_report = %s, parts_replaced = %s, status = 'Completed' 
            WHERE id = %s
        """
        return Database.execute_query(query, (service_report, parts_replaced, appointment_id), commit=True)

    @staticmethod
    def check_mechanic_schedule_conflict(mechanic_id: int, appointment_date: str, appointment_time: str, exclude_appointment_id: int = None) -> bool:
        """
        Verifies if a specific mechanic is already committed to an approved or completed job 
        for a specific date and time slot.
        """
        query = """
            SELECT COUNT(*) AS count 
            FROM appointments 
            WHERE mechanic_id = %s 
              AND appointment_date = %s 
              AND appointment_time = %s 
              AND status IN ('Approved', 'Completed')
        """
        params = [mechanic_id, appointment_date, appointment_time]
        if exclude_appointment_id:
            query += " AND id != %s"
            params.append(exclude_appointment_id)
            
        result = Database.execute_query(query, tuple(params))
        return result[0]['count'] > 0 if result else False

    @staticmethod
    def get_all_active_mechanics():
        """Fetches all registered mechanics with an active account status"""
        query = "SELECT id, first_name, last_name, email FROM users WHERE role_id = 2 AND status = 'active'"
        return Database.execute_query(query)

    @staticmethod
    def get_badge_count(user_id: int) -> int:
        """Counts appointments with state 'Approved' or 'Cancelled' for the client's header notification badge"""
        query = "SELECT COUNT(*) as count FROM appointments WHERE user_id = %s AND status IN ('Approved', 'Cancelled')"
        result = Database.execute_query(query, (user_id,))
        return result[0]['count'] if result else 0