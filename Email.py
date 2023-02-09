import smtplib
from email.mime.text import MIMEText


def send_email(message):
    sender = "botvvvvtrt@gmail.com"
    password = "BOT228007"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    data = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="900" height="230">
    <center>
        <h1 style="font-size: 400%;">Получение рассылки в ...</h1>
    </center>
    </td>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="900" height="230">
    <center>
        <h1 style="font-size: 400%;">Получение рассылки в ...</h1>
        <p>как дела?</p>
    </center>
    </td>
</body>
</html>"""


    try:
        server.login(sender, password)

        msg = MIMEText(data, "html")
        msg["Subject"] = "hello"

        server.sendmail(sender, "sleim2000@gmail.com", msg.as_string())

        return "ok"
    except Exception as _ex:
        return f"{_ex}\n"


def confirm_email(recipient, code):
    sender = "botvvvvtrt@gmail.com"
    password = "BOT228007"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1 style="font-size: 300%;">Получение рассылки</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#FFFFFF" style="padding: 40px 0 30px;" 0 width="750" height="40">
    <center>
        <h1 style="font-size: 200%;">Код подтверждения: {code}</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1>Если вы хотите получать рассылки, то введите этот код в чат-бота. Иначе проигнорируйте это письмо.</h1>
    </center>
    </td>
    </tr>
</body>
</html>"""


    try:
        server.login(sender, password)

        msg = MIMEText(data, "html")
        msg["Subject"] = "Рассылка в ..."

        server.sendmail(sender, recipient, msg.as_string())

        return "ok"
    except Exception as _ex:
        return f"{_ex}\n"


def mailing_email(recipient, number, header, text):
    sender = "botvvvvtrt@gmail.com"
    password = "BOT228007"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1 style="font-size: 300%;">Рассылка №{number}: {header}</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#FFFFFF" style="padding: 40px 0 30px;" 0 width="750" height="40">
    <center>
        <h1 style="font-size: 200%;">{text}</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1></h1>
    </center>
    </td>
    </tr>
</body>
</html>"""


    try:
        server.login(sender, password)

        msg = MIMEText(data, "html")
        msg["Subject"] = f"Рассылка №{number}"

        server.sendmail(sender, recipient, msg.as_string())

        return "ok"
    except Exception as _ex:
        return f"{_ex}\n"



def survey_email(recipient, number, header, text, ans, id):
    sender = "botvvvvtrt@gmail.com"
    password = "BOT228007"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    ans_= ""

    for i, ot in enumerate(ans):
        ans_ += f'<p><a href="https://helperbotvvvvtrt.pythonanywhere.com/voice/{id}_{number}_{i}" class="btn">{i + 1}. {ot}</a></p>\n'


    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

    <style>
   .btn {"{"}
    display: inline-block; /* Строчно-блочный элемент */
    background: #70bbd9; /* Серый цвет фона */
    font-size: 200%;
    color: #fff; /* Белый цвет текста */
    padding: 1rem 1.5rem; /* Поля вокруг текста */
    text-decoration: none; /* Убираем подчёркивание */
    border-radius: 30px; /* Скругляем уголки */
   {"}"}
  </style>
</head>
<body>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1 style="font-size: 300%;">Опрос №{number}: {header}</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#FFFFFF" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1 style="font-size: 200%;">{text}</h1>
        {ans_}
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1></h1>
    </center>
    </td>
    </tr>
</body>
</html>"""


    try:
        server.login(sender, password)

        msg = MIMEText(data, "html")
        msg["Subject"] = f"Рассылка №{number}"

        server.sendmail(sender, recipient, msg.as_string())

        return "ok"
    except Exception as _ex:
        return f"{_ex}\n"


def end_surve_email(recipient, number, header, text, ans):
    sender = "botvvvvtrt@gmail.com"
    password = "BOT228007"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    data = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1 style="font-size: 300%;">Рассылка №{number}: {header}</h1>
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#FFFFFF" style="padding: 40px 0 30px;" 0 width="750" height="40">
    <center>
        <h1 style="font-size: 200%;">{text}</h1>
        {ans}
    </center>
    </td>
    </tr>
    <tr>
    <td align="center" bgcolor="#70bbd9" style="padding: 40px 0 30px;" 0 width="750" height="80">
    <center>
        <h1></h1>
    </center>
    </td>
    </tr>
</body>
</html>"""


    try:
        server.login(sender, password)

        msg = MIMEText(data, "html")
        msg["Subject"] = f"Рассылка №{number}"

        server.sendmail(sender, recipient, msg.as_string())

        return "ok"
    except Exception as _ex:
        return f"{_ex}\n"



def main():
    print(confirm_email("sleim2000@gmail.com", 1234))

if __name__ == '__main__':
    main()