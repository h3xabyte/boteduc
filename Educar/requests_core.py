from bs4 import BeautifulSoup as bs
import requests
import re
import shutil
import os
import time
import MySQLdb
import logging
from urllib.parse import urlparse
import string
import random
import sys
import time
import numpy as np

class Requests:



 ## Se crea un profesor utilizando el API de chamilo
 def crear_profesor(self, nombre, apellido, usuario):
     ##generador de IDs , contraseñas (cryptograph)
        def generador_ids(size=8, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        URL = 'https://aula.educar.com.co/'
        LOGIN_ROUTE = ''


        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()

        """ csrf_token = s.get(URL).cookies['csrftoken'] """
        user = 'admin'
        password = '$%EDUC4R2020.it'

        login_payload = {
            'login': user,
            'password': password,

        }

        login_req = s.post(URL, headers=HEADERS, data=login_payload)

        print(login_req.status_code)

        cookies = login_req.cookies

        soup3 = bs(
            s.get('https://aula.educar.com.co/main/admin/user_add.php').text, 'html.parser')

        soup3.find('input', {"name": "sec_token"})
        sp3 = soup3.find('input', {"name": "sec_token"})
        sec_token = sp3['value']
        print(sec_token)
        cookies = login_req.cookies
        user1 = usuario
        pass1 = generador_ids()
        print('datos de usuario', nombre, apellido)
        usuario_payload = {
            'lastname': apellido,
            'firstname': nombre,
            'official_code': '',
            'email': 'sie@educar.com.co',
            'phone': '',
            'username': user1,
            'password[password_auto]': '0',
            'password[password]': '$%EDUC4R2020.it',
            'status': '1',
            'admin[platform_admin]': '0',
            'language': 'spanish2',
            'mail[send_mail]': '0',
            'radio_expiration_date': '0',
            'expiration_date': '2030-08-31 20:29',
            'active': '1',
            'extra_legal_accept': '',
            'extra_already_logged_in': '',
            'extra_update_type': '',
            'extra_rssfeeds': '',
            'extra_dashboard': '',
            'extra_timezone': '',
            'extra_mail_notify_invitation': '1',
            'extra_mail_notify_group_message': '1',
            'extra_user_chat_status': '',
            'extra_google_calendar_url': '',
            'extra_captcha_blocked_until_date': '',
            'extra_skype': '',
            'extra_linkedin_url': '',
            'extra_mail_notify_message': '1',
            'extra_request_for_legal_agreement_consent_removal_justification': '',
            'extra_request_for_delete_account_justification': '',
            'extra_request_for_legal_agreement_consent_removal': '',
            'extra_request_for_delete_account': '',
            'submit': '',
            '_qf__user_add': '',
            'item_id': '0',
            'sec_token': sec_token,
        }
        user_req = s.post('https://aula.educar.com.co/main/admin/user_add.php',
                        headers=HEADERS, data=usuario_payload)
        return user1, pass1

 def cursos_y_matricula(self, institucion, firstname, curso, grupo, usuario):
        x = np.random.randint(10000, 10000000)
        print(x)


        nombre = firstname + ' ' + curso + grupo
        URL = 'https://aula.educar.com.co/'
        LOGIN_ROUTE = ''
        URL_CURSOS = 'https://aula.educar.com.co/main/admin/course_add.php'

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()

        """ csrf_token = s.get(URL).cookies['csrftoken'] """
        user = 'admin'
        password = '$%EDUC4R2020.it'

        login_payload = {
            'login': user,
            'password': password,

        }

        login_req = s.post(URL, headers=HEADERS, data=login_payload)

        print(login_req.status_code)

        cookies = login_req.cookies
        r = s.get('https://aula.educar.com.co/main/admin/course_list.php')

        mysql = MySQLdb.connect(host='educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com',
                                # mysql = MySQLdb.connect(host='dev-serverless-educar.cluster-cxlnmcx1f2mz.us-east-2.rds.amazonaws.com',
                                user="2018_chm_lms_demo",
                                passwd="fq1Wn6Z2J8KjRmFG",
                                db="global_sie")

        mysql2 = MySQLdb.connect(host='educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com',
                                user="2018_chm_lms_demo",
                                passwd="fq1Wn6Z2J8KjRmFG",
                                db="2018_chm_lms_demo")
        mysql3 = MySQLdb.connect(host='db-produccion-educarsie2-serveless.cluster-cxlnmcx1f2mz.us-east-2.rds.amazonaws.com',
                         user="superadmin_prod",
                         passwd="%Educ4r2020%",
                         db="2018_chm_lms_demo")

        """ # Mysql Connection
        app.config['MYSQL_HOST'] = 'educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com'
        app.config['MYSQL_USER'] = '2018_chm_lms_demo'
        app.config['MYSQL_PASSWORD'] = 'fq1Wn6Z2J8KjRmFG'
        app.config['MYSQL_DB'] = 'global_sie'
        mysql = MySQL(app)
        """
        curunk = mysql3.cursor()
        curunk.execute('SELECT id FROM user WHERE username=%s', (usuario,))
        profe_id = curunk.fetchone()
        print(profe_id)
        timstamp2 = str(time.time())
        codigo = institucion + str(x)
        curso_payload = {
            'title': nombre,
            'visual_code': codigo,
            'category_code': institucion,
            'course_teachers[]': '1',
            'course_teachers[]': profe_id,
            'department_name': '',
            'department_url': '',
            'visibility': '1',
            'subscribe': '1',
            'unsubscribe': '0',
            'disk_quota': '250',
            'extra_video_url': '',
            'submit': '',
            '_qf__update_course': '',
            'course_language': 'spanish2',
            'item_id': '0'
        }

        curso_req = s.post(URL_CURSOS, headers=HEADERS, data=curso_payload)

        print(curso_req.status_code)
        print('curso', nombre, 'creado')
        cookies = curso_req.cookies
        print('CURSO CREADO')

        cur1 = mysql.cursor()
        cur2 = mysql.cursor()
        cur3 = mysql.cursor()
        cur4 = mysql.cursor()
        cur5 = mysql2.cursor()
        cur1.execute(
            'SELECT id FROM cursos WHERE institucion=%s AND grado=%s', (institucion, curso))
        id_curso = cur1.fetchall()
        id_curso = ''.join(map(str, id_curso))
        id_curso = id_curso.replace('(', '').replace(
            "'", "").replace(',', '').replace(')', '')
        cur2.execute('SELECT id FROM grupos WHERE curso=%s AND grupo=%s',
                    (id_curso, grupo))
        print('curso y grupo', id_curso, grupo)
        grupo_id = cur2.fetchall()

        cur3.execute(
            'SELECT estudiante FROM grupos_estudiantes WHERE grupo=%s', (grupo_id))
        estudiantesx = cur3.fetchall()

        for estudiante in estudiantesx:
            cur4.execute('SELECT usuario FROM usuarios WHERE id=%s', (estudiante))
            nombreusuario = cur4.fetchall()

            cur5.execute('SELECT id from user WHERE username=%s', (nombreusuario))
            estudiante = cur5.fetchall()

            estudiante = ''.join(map(str, estudiante))
            estudiante = estudiante.replace('(', '').replace(
                "'", "").replace(',', '').replace(')', '')
            inscribir = 'https://aula.educar.com.co/main/user/subscribe_user.php?cidReq={}&id_session=0&gidReq=0&gradebook=0&origin=&register=yes&type=5&user_id={}'.format(
                codigo, estudiante)
            s.get(inscribir)

            nombreusuariox = ''.join(map(str, nombreusuario))
            nombreusuariox = nombreusuariox.replace('(', '').replace(
                "'", "").replace(',', '').replace(')', '')
            print('ESTUDIANTE', nombreusuariox, 'INSCRITO CON EXITO EN EL NUEVO CURSO', codigo)
        mysql.close()
        mysql2.close()
        return  'curso creado con exito'

 def matricular_vn(self, usuario, password):

        mysql = MySQLdb.connect(host='educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com',
                                user="EducarDB",
                                passwd="Db2020!",
                                db="global_sie")
        mysql2 = MySQLdb.connect(host='educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com',
                                user="EducarDB",
                                passwd="Db2020!",
                                db="2018_chm_lms_demo")
        mysql3 = MySQLdb.connect(host='db-produccion-educarsie2-serveless.cluster-cxlnmcx1f2mz.us-east-2.rds.amazonaws.com',
                                user="superadmin_prod",
                                passwd="%Educ4r2020%",
                                db="2018_chm_lms_demo")
        logger = logging.getLogger('try_Log')

        URL = 'https://sie.educar.com.co/cas/login?service=http%3A%2F%2Fsie.educar.com.co%2F'
        LOGIN_ROUTE = ''

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()
        soup = bs(s.get('https://sie.educar.com.co/cas/login?service=http%3A%2F%2Fsie.educar.com.co%2Fsie%2F').text, 'html.parser')
        soup.find('input', {"name": "lt"})
        sp = soup.find('input', {"name": "lt"})
        cas_token = sp['value']


        user1 = usuario
        password1 = password


        login_payload = {
            'lt': cas_token,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'username': user1,
            'password': password1,
            'submit': 'ENTRAR'
        }

        login_req = s.post(URL, headers=HEADERS, data=login_payload)


        cookies = login_req.cookies

        r = s.get('https://sie.educar.com.co/cas/login?service=http%3A%2F%2Fsie.educar.com.co:8080%2FLMS%2Findex.php%2Fgateway=true')

        soup = bs(s.get(
            'http://sie.educar.com.co:8080/LMS/user_portal.php').text, 'html.parser')

        links = soup.find_all(
            "a", href=lambda href: href and "index.php?id_session=0" in href)
        # login a el aula
        URL = 'https://aula.educar.com.co/'
        LOGIN_ROUTE = ''


        HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'origin': URL, 'referer': URL + LOGIN_ROUTE}

        s = requests.session()

        """ csrf_token = s.get(URL).cookies['csrftoken'] """
        user = 'admin'
        password = '$%EDUC4R2020.it'

        login_payload = {
            'login': user,
            'password': password,

        }

        login_req = s.post(URL, headers=HEADERS, data=login_payload)

        print(login_req.status_code)
        curreg = mysql3.cursor()
        curreg2 = mysql3.cursor()
        curreg3 = mysql3.cursor()
        curprofe = mysql3.cursor()

        res = []

        for link in links:


            link = link['href']
            curso = link.replace('http://sie.educar.com.co:8080/LMS/courses/',
                                '').replace('/index.php?id_session=0', '')
            print(curso)
            res.append(curso)
        print('//////////////////////////////')
        lista = []
        [lista.append(x) for x in res if x not in lista]
        for curso in lista:
                print(curso)
                curreg.execute('SELECT id FROM course WHERE code=%s', (curso,))
                curso_id = curreg.fetchall()
                curreg2.execute('SELECT category_code FROM course WHERE code=%s', (curso,))
                cat_code = curreg2.fetchall()
                curreg3.execute('SELECT title FROM course WHERE code=%s', (curso,))
                title = curreg3.fetchall()
                curprofe.execute('SELECT id from user WHERE username=%s', (usuario,))
                id_profe = curprofe.fetchall()

                curso_id = ''.join(map(str, curso_id))
                curso_id = curso_id.replace('(', '').replace(
                    "'", "").replace(',', '').replace(')', '')
                title = ''.join(map(str, title))
                title = title.replace('(', '').replace(
                    "'", "").replace(',', '').replace(')', '')
                cat_code = ''.join(map(str, cat_code))
                cat_code = title.replace('(', '').replace(
                    "'", "").replace(',', '').replace(')', '')
                id_profe = ''.join(map(str, id_profe))
                id_profe = id_profe.replace('(', '').replace(
                    "'", "").replace(',', '').replace(')', '')
                curprofes = mysql2.cursor()
                curprofes.execute('SELECT user_id FROM course_rel_user WHERE c_id=%s AND status=%s', (curso_id, '1'))
                profes = curprofes.fetchall()
                listaprof = []
                for teacher in profes:
                    teacher = ''.join(map(str, teacher))
                    teacher = teacher.replace('(', '').replace(
                    "'", "").replace(',', '').replace(')', '')
                    listaprof.append(teacher)

                listaprof.append(id_profe)
                print(listaprof)

                profesor_payload = {

                    'title': title,
                    'real_code': curso,
                    'visual_code': curso,
                    'category_code': '2090',
                    'course_teachers[]': listaprof,
                    'department_name': '',
                    'department_url': '',
                    'course_language': 'spanish2',
                    'visibility': '1',
                    'subscribe': '0',
                    'unsubscribe': '0',
                    'disk_quota': '512',
                    'extra_video_url': '',
                    'submit': '',
                    '_qf__update_course': '',
                    'code': curso,
                    'item_id': curso_id,


                }
                print(profesor_payload)
                print('profesor matriculado con exito en el curso', title)
                profesor_req = s.post('https://aula.educar.com.co/main/admin/course_edit.php?id={}'.format(curso_id),
                                    headers=HEADERS, data=profesor_payload)
                print(profesor_req)

        mysql.close()
        mysql2.close()
        mysql3.close()
        return 'Profesor matriculado en los cursos'
