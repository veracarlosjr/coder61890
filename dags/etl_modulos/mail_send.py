import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from airflow.models import Variable

def send_email(**context):
    # Get email configurations from Airflow Variables
    subject = Variable.get("subject_mail", default_var="Alerta: Proceso de ETL")
    from_address = Variable.get("email")
    password = Variable.get("email_password")
    to_address = Variable.get("to_address")
    
    # Get the value to check against the threshold
    threshold_value = float(Variable.get("alert_threshold", default_var="1000"))  # Example threshold
    
    # Extract the actual value from XCom
    actual_value_list = context['ti'].xcom_pull(task_ids='transform_task')
    
    # Print actual_value for debugging
    print(f"Actual value from XCom: {actual_value_list}")
    
    if not actual_value_list or not isinstance(actual_value_list, list):
        print("El valor extraído de XCom no es una lista válida.")
        return

    # Asumimos que el primer elemento de la lista interna es el valor necesario
    actual_value = actual_value_list[0][2] if len(actual_value_list[0]) > 2 else None
    
    if actual_value is None:
        print("No se encontró un valor válido en la lista extraída de XCom.")
        return

    try:
        actual_value = float(actual_value)  # Ensure it's a number
    except ValueError:
        print("El valor actual no es un número válido.")
        return

    # Customize the email message based on threshold
    if actual_value > threshold_value:
        message_body = f"""
        <html>
        <body>
            <p>Hola,</p>
            <p>El valor extraído ha sobrepasado el umbral configurado.</p>
            <p>Valor actual: {actual_value} (Umbral: {threshold_value})</p>
        </body>
        </html>
        """
        subject = f"Alerta: Valor superado ({actual_value})"
    else:
        message_body = f"""
        <html>
        <body>
            <p>Hola,</p>
            <p>El proceso de extracción y carga a Redshift ha sido realizado con éxito.</p>
            <p>Valor actual: {actual_value}</p>
        </body>
        </html>
        """
    
    # Create a MIMEText object
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'html'))

    try:
        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

