from celery import shared_task
from mail_service import send_email
from models import Milestones, Users, MilestoneSubmissions
from datetime import datetime, timedelta

@shared_task(ignore_result=True)
def send_deadline_reminder():
    today = datetime.today().date()
    reminder_date = today + timedelta(days=2)

    milestones = Milestones.query.filter(Milestones.deadline == reminder_date).all()
    
    for milestone in milestones:
        users = Users.query.all()
        for user in users:
            message = f"""
                <html>
                    <body>
                        <h2 style="color: #2C3E50; font-family: Arial, sans-serif;">Hello {user.first_name},</h2>
                        <p style="font-family: Arial, sans-serif; font-size: 16px;">
                            We hope you're doing well! We wanted to remind you that the following milestone is due tomorrow:
                        </p>

                        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                            <tr>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Milestone</th>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Description</th>
                                <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Deadline</th>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.title}</td>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.description}</td>
                                <td style="padding: 10px; border: 1px solid #BDC3C7;">{milestone.deadline}</td>
                            </tr>
                        </table>

                            <p style="font-family: Arial, sans-serif; font-size: 16px; margin-top: 20px;">
                                Please make sure to complete it on time. If you have any questions, feel free to reach out.
                            </p>
    
                            <p style="font-family: Arial, sans-serif; font-size: 16px;">
                                Best regards,<br>
                                <strong>Collabspace</strong>
                            </p>
                    </body>
                </html>
                """
            send_email(user.email, "Reminder: Your Book deadline is near", message)
    
    return "Done!"

@shared_task(ignore_result=True)
def send_instructor_report():
    today = datetime.today().date()

    milestones = Milestones.query.filter(Milestones.deadline < today).all()

    for milestone in milestones:
        submissions = MilestoneSubmissions.query.filter_by(milestone_id=milestone.id).all()
        total_students = Users.query.filter_by(role="student").count()

        submitted_students = {submission.student_id for submission in submissions}
        missed_count = total_students - len(submitted_students)

        table_rows = ""
        for student in Users.query.filter_by(role="student").all():
            submission_status = "Submitted" if student.id in submitted_students else "Missed"
            table_rows += f"""
                <tr>
                    <td style="padding: 10px; border: 1px solid #BDC3C7;">{student.first_name} {student.last_name}</td>
                    <td style="padding: 10px; border: 1px solid #BDC3C7;">{student.email}</td>
                    <td style="padding: 10px; border: 1px solid #BDC3C7;">{submission_status}</td>
                </tr>
            """

        message = f"""
            <html>
                <body>
                    <h2 style="color: #2C3E50; font-family: Arial, sans-serif;">Instructor,</h2>
                    <p style="font-family: Arial, sans-serif; font-size: 16px;">
                        Here is the summary of submissions for the milestone: <strong>{milestone.title}</strong>
                    </p>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <tr>
                            <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Student Name</th>
                            <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Email</th>
                            <th style="padding: 10px; text-align: left; background-color: #ECF0F1; border: 1px solid #BDC3C7;">Status</th>
                        </tr>
                        {table_rows}
                    </table>

                    <p style="font-family: Arial, sans-serif; font-size: 16px; margin-top: 20px;">
                        Total Students: {total_students}<br>
                        Submitted: {len(submitted_students)}<br>
                        Missed: {missed_count}
                    </p>

                    <p style="font-family: Arial, sans-serif; font-size: 16px;">
                        Best regards,<br>
                        <strong>Collabspace</strong>
                    </p>
                </body>
            </html>
        """

        # Send the email to the instructor
        instructor_email = "instructor@example.com"  # Replace with actual instructor email
        send_email(instructor_email, f"Summary of Submissions: {milestone.title}", message)

    return "Instructor Emails Sent!"
