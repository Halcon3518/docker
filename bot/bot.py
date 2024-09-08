import logging
import re
import os
import paramiko
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from dotenv import load_dotenv
from pathlib import Path
import psycopg2
from psycopg2 import Error

#Использование файла param.env с переменными окружения
dotenv_path = Path('param.env')
load_dotenv(dotenv_path=dotenv_path)

host = os.getenv('RM_HOST')
port = os.getenv('RM_PORT')
username = os.getenv('RM_USER')
password = os.getenv('RM_PASSWORD')

pg_user = os.getenv('DB_USER')
pg_password = os.getenv('DB_PASSWORD')
pg_host = os.getenv('DB_HOST')
pg_port = os.getenv('DB_PORT')
pg_database = os.getenv('DB_DATABASE')

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#Ответ на start
def start(update: Update, context):
    logging.info('Reply to start')
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

#Ответ на help
def helpCommand(update: Update, context):
    logging.info('Reply to help')
    update.message.reply_text('Help!')

#Приглашение на ввод текста для поиска номеров телефонов
def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')
    logging.info('Reply to find_phone_number')
    return 'findPhoneNumbers'

#Приглашение на ввод текста для поиска email
def findEmailsCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email: ')
    logging.info('Reply to find_email')
    return 'findEmails'

#Приглашение на ввод пароля
def findPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки: ')
    logging.info('Reply to verify_password')
    return 'findPassword'

#Ответ на get_release
def get_release(update: Update, context):
    logging.info('Reply to get_release')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_uname
def get_uname(update: Update, context):
    logging.info('Reply to get_uname')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_uptime
def get_uptime(update: Update, context):
    logging.info('Reply to get_uptime')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_df
def get_df(update: Update, context):
    logging.info('Reply to get_df')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_free
def get_free(update: Update, context):
    logging.info('Reply to get_free')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_mpstat
def get_mpstat(update: Update, context):
    logging.info('Reply to get_mpstat')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_w
def get_w(update: Update, context):
    logging.info('Reply to get_w')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_auths
def get_auths(update: Update, context):
    logging.info('Reply to get_auths')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('last -n 10')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_critical
def get_critical(update: Update, context):
    logging.info('Reply to get_critical')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('grep "CRITICAL" /var/log/syslog | tail -n 5')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_ps
def get_ps(update: Update, context):
    logging.info('Reply to get_ps')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('ps aux | head -n 15')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_ss
def get_ss(update: Update, context):
    logging.info('Reply to get_ss')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('ss -tuln')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_services
def get_services(update: Update, context):
    logging.info('Reply to get_services')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('systemctl list-units --type=service | head -n 15')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

#Ответ на get_apt_list
def get_apt_listCommand(update: Update, context):
    update.message.reply_text('Введите наименование конкретного пакета или введите "all", если желаете получить вывод всех пакетов.')
    logging.info('Reply to get_apt_list')
    return 'get_apt_list'

#Ответ на get_repl_logs
def get_repl_logs(update: Update, context):
    logging.info('Reply to get_repl_logs')

    #Подключение по ssh к master узлу
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    #Грепаем логи репликации в /var/log/postgresql/postgresql-15-main.log
    stdin, stdout, stderr = client.exec_command('grep "repl_user" /var/log/postgresql/postgresql-15-main.log | tail -n 5')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8"))

    #Получаем список логов
    stdin, stdout, stderr = client.exec_command('ls /home/pt/docker/logs')
    logs = stdout.read().decode('utf-8').split()
    # Определение последнего лога
    sorted_logs = sorted(logs, key=lambda x: x[:19])
    last_log = sorted_logs[-1]
    update.message.reply_text(last_log)
    # Чтение последнего лога и поиск сообщений о репликации
    stdin, stdout, stderr = client.exec_command(f'cat /home/pt/docker/logs/{last_log}')
    data = stdout.read().decode('utf-8')
    # Поиск сообщений о репликации
    replication_messages = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3} UTC .* received replication command: .*', data)
    messages = [message for message in replication_messages]
    update.message.reply_text("\n".join(messages))
    
    #for message in replication_messages:
        #update.message.reply_text(str(message))
        #Вывод сообщения
        #update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    
    client.close()

#Ответ на get_emails
def get_emails(update: Update, context):
    logging.info('Reply to get_emails')
    try:
        connection = psycopg2.connect(user=pg_user, password=pg_password, host=pg_host, port=pg_port, database=pg_database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        getemails = ''
        for row in data:
            getemails += f"{row[0]}. {row[1]}\n"
        update.message.reply_text(getemails)
        logging.info('SELECT FROM Emails was executed')
    except (Exception, Error) as error:
        logging.info('SELECT FROM Emails was executed with error', error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

#Ответ на get_phone_numbers
def get_phone_numbers(update: Update, context):
    logging.info('Reply to get_phone_numbers')
    try:
        connection = psycopg2.connect(user=pg_user, password=pg_password, host=pg_host, port=pg_port, database=pg_database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phonenumbers;")
        data = cursor.fetchall()
        getphonenumbers = ''
        for row in data:
           getphonenumbers += f"{row[0]}. {row[1]}\n"
        update.message.reply_text(getphonenumbers)
        logging.info('SELECT FROM phonenumbers was executed')
    except (Exception, Error) as error:
        logging.info('SELECT FROM phonenumbers was executed with error', error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

#Функция ответа на get_apt_list
def get_apt_list (update: Update, context):
    logging.info('launch dialog for get_apt_list')
    user_input = update.message.text # Получаем текст от пользователя

    aptRegex = re.compile(r'^all$')
    aptList = aptRegex.findall(user_input) #Проверяем, введен ли параметр all

    if not aptList: #Если введен параметр, отличный от all
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password, port=port)

        stdin, stdout, stderr = client.exec_command(f'dpkg -l | grep {user_input} | head -n 15')
        data = stdout.read() + stderr.read()
        update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
        client.close()
        return ConversationHandler.END # Завершаем работу обработчика диалога
    
    #Если введен параметр all
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    stdin, stdout, stderr = client.exec_command('dpkg -l | head -n 15')
    data = stdout.read() + stderr.read()
    update.message.reply_text(str(data, encoding="utf-8").replace('\\n', '\n').replace('\\t', '\t')[2:-1])
    client.close()

    return ConversationHandler.END # Завершаем работу обработчика диалога

#Функция поиска номеров телефонов
def findPhoneNumbers (update: Update, context):
    logging.info('launch dialog for find_phone_number')
    user_input = update.message.text # Получаем текст, содержащий(или нет) номера телефонов
    phoneNumRegex = re.compile(r'(\b8|\+7)((\s|\()-?|\d{3}|-)(\d{3}|\(\d{3})(\d{2}|\)|-|\s)?(\s|\d{3}|\d{2})?(\d{3}|\d{2}|\s|\-)(\d{2}|\s)(\d{2}|\s)?(\d{2}|\-\d{2}|\s\d{2})?')
    phoneNumberList = phoneNumRegex.findall(user_input) # Ищем номера телефонов

    if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return # Завершаем выполнение функции
    
    global phonenumbersforbd
    phonenumbersforbd = [] #Создаём global кортеж, в который запишем номера телефонов для записи в бд
    phoneNumbers = '' # Создаем строку, в которую будем записывать номера телефонов для вывода пользователю
    for i, phoneNumber in enumerate(phoneNumberList, start=1):
        phonenumbersforbd.append(''.join(phoneNumber).replace(" ", "").replace("(", "").replace(")", ""))
        phoneNumbers += f'{i}. {"".join(phoneNumber).replace(" ", "").replace("(", "").replace(")", "")}\n'

    update.message.reply_text(phoneNumbers) # Отправляем сообщение пользователю
    update.message.reply_text('Напишите команду "/write_phone_nubmers", если хотите записать найденные номера в базу данных')
    return ConversationHandler.END # Завершаем работу обработчика диалога

#Запись номеров телефонов в базу
def writePhoneNumbersCommand(update: Update, context):
    logging.info('Run writePhoneNumbersCommand')
    try:
        #Подключаемся к бд
        connection = psycopg2.connect(user=pg_user, password=pg_password, host=pg_host, port=pg_port, database=pg_database)
        cursor = connection.cursor()        
        phoneNumberList = tuple(phonenumbersforbd)

        if not phoneNumberList: # Обрабатываем случай, когда номеров телефонов нет
            update.message.reply_text('Телефонные номера не найдены')
            return # Завершаем выполнение функции

        #Записываем найденные номера телефонов в базу
        for i, phones in enumerate(phoneNumberList, start=1):
            cursor.execute("INSERT INTO phonenumbers (phonenumber) VALUES (%s)", (phones,))
            connection.commit()

        update.message.reply_text('Команда записи в БД успешно выполнена')
    except (Exception, Error) as error:
        logging.info('INSERT INTO phonenumbers was executed with error', error)
        update.message.reply_text('Ошибка записи в БД')
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

#Функция поиска email
def findEmails (update: Update, context):
    logging.info('launch dialog for find_email')
    user_input = update.message.text # Получаем текст, содержащий(или нет) email

    EmailRegex = re.compile(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)')

    emailList = EmailRegex.findall(user_input) #Ищем email

    if not emailList:
        update.message.reply_text('Email не найдены')
        return #Завершаем выполнение функции
    
    global emailsforbd
    emailsforbd = [] #Создаём global кортеж, в который запишем email для записи в бд
    Emails = '' #Строка для вывода в бота
    for i in range(len(emailList)):
        emailsforbd.append(emailList[i])
        Emails += f'{i+1}. {emailList[i]}\n'

    update.message.reply_text(Emails) # Отправляем сообщение пользователю
    update.message.reply_text('Напишите команду "/write_emails", если хотите записать найденные email в базу данных')
    return ConversationHandler.END # Завершаем работу обработчика диалога

#Запись email в базу
def writeEmailsCommand(update: Update, context):
    logging.info('writeEmailsCommand')
    try:
        #Подключаемся к бд
        connection = psycopg2.connect(user=pg_user, password=pg_password, host=pg_host, port=pg_port, database=pg_database)
        cursor = connection.cursor()        
        emailsList = tuple(emailsforbd)

        if not emailsList: # Обрабатываем случай, когда email нет
            update.message.reply_text('Email не найдены')
            return # Завершаем выполнение функции

        #Записываем найденные номера телефонов в базу
        for i, emails in enumerate(emailsList, start=1):
            cursor.execute("INSERT INTO emails (email) VALUES (%s)", (emails,))
            connection.commit()

        update.message.reply_text('Команда записи в БД успешно выполнена')
    except (Exception, Error) as error:
        logging.info('INSERT INTO emails was executed with error', error)
        update.message.reply_text('Ошибка записи в БД')
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

#Функция определения сложности пароля
def findPassword (update: Update, context):
    logging.info('launch dialog for verify_password')
    user_input = update.message.text # Получаем текст, содержащий пароль

    VerifyPasswordRegex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*().]).{8,}$')

    userPassword = VerifyPasswordRegex.findall(user_input) #Определяем сложность пароля

    if not userPassword:
        update.message.reply_text('Пароль простой')
        return #Завершаем выполнение функции
    else:
        update.message.reply_text('Пароль сложный')
        return ConversationHandler.END # Завершаем работу обработчика диалога

#Функция echo
def echo(update: Update, context):
    logging.info('Reply to echo')
    update.message.reply_text(update.message.text)

def main():
    logging.info('Bot has started working')
    updater = Updater(os.environ.get('TOKEN'), use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога поиска номеров телефонов
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )

    # Обработчик диалога поиска email	
    convHandlerFindEmails = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailsCommand)],
        states={
            'findEmails': [MessageHandler(Filters.text & ~Filters.command, findEmails)],
        },
        fallbacks=[]
    )

    # Обработчик диалога проверки пароля
    convHandlerFindPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', findPasswordCommand)],
        states={
            'findPassword': [MessageHandler(Filters.text & ~Filters.command, findPassword)],
        },
        fallbacks=[]
    )

    # Обработчик диалога для списка пакетов
    convHandlerFindPassword = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_listCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

	# Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(CommandHandler("get_release", get_release))
    dp.add_handler(CommandHandler("get_uname", get_uname))
    dp.add_handler(CommandHandler("get_uptime", get_uptime))
    dp.add_handler(CommandHandler("get_df", get_df))
    dp.add_handler(CommandHandler("get_free", get_free))
    dp.add_handler(CommandHandler("get_mpstat", get_mpstat))
    dp.add_handler(CommandHandler("get_w", get_w))
    dp.add_handler(CommandHandler("get_auths", get_auths))
    dp.add_handler(CommandHandler("get_critical", get_critical))
    dp.add_handler(CommandHandler("get_ps", get_ps))
    dp.add_handler(CommandHandler("get_ss", get_ss))
    dp.add_handler(CommandHandler("get_services", get_services))
    dp.add_handler(CommandHandler("get_repl_logs", get_repl_logs))
    dp.add_handler(CommandHandler("get_emails", get_emails))
    dp.add_handler(CommandHandler("get_phone_numbers", get_phone_numbers))
    dp.add_handler(CommandHandler("write_phone_nubmers", writePhoneNumbersCommand))
    dp.add_handler(CommandHandler("write_emails", writeEmailsCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmails)
    dp.add_handler(convHandlerFindPassword)
		
	# Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
		
	# Запускаем бота
    updater.start_polling()

	# Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
