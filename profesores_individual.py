from bs4 import BeautifulSoup as bs
import requests
import re
import shutil
import os
import time
import MySQLdb
import logging
from urllib.parse import urlparse
from Educar import requests_core

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
usuario = input("Introduce el Usuario")
password = input("Introduce la contraseña")
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
        profesor_payload = {

            'title': title,
            'real_code': curso,
            'visual_code': curso,
            'category_code': '2141',
            'course_teachers[]': id_profe,
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

        print('profesor matriculado con exito en el curso', title)
        profesor_req = s.post('https://aula.educar.com.co/main/admin/user_add.php?id={}'.format(curso_id),
                            headers=HEADERS, data=profesor_payload)
        print(profesor_req)
        grupo_curso = title[-3:]
        print(grupo_curso)
        ren = re.split(', |_|-|!', grupo_curso)
        print(grupo_curso[0])
        print(grupo_curso[1])
        curso = grupo_curso[0]
        grupo = grupo_curso[1] + grupo_curso[2]
        firstname = title.replace(grupo_curso, '')
        rq = requests_core.Requests()
        crear = rq.cursos_y_matricula('2141', firstname, curso, grupo, usuario)