import os
import pymysql
import datetime
from unidecode import unidecode
import subprocess
import time




mysql = pymysql.connect(host='db-produccion-educarsie2-serveless.cluster-cxlnmcx1f2mz.us-east-2.rds.amazonaws.com',
                        user="superadmin_prod",
                        passwd="%Educ4r2020%",
                        db="2018_chm_lms_demo")
mysql2 = pymysql.connect(host='educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com',
                         user="EducarDB",
                         passwd="Db2020!",
                         db="global_sie")

cur1 = mysql2.cursor()
cur2 = mysql2.cursor()
cur3 = mysql2.cursor()
cur4 = mysql2.cursor()
cur5 = mysql2.cursor()
cur6 = mysql2.cursor()
cur7 = mysql2.cursor()
curdwn = mysql2.cursor()
cur1n = mysql.cursor()
cur2n = mysql.cursor()
cur3n = mysql.cursor()
cur4n = mysql.cursor()
cur5n = mysql.cursor()
cur6n = mysql.cursor()
class Saber:
    def saber_kill(self, institucion):
        def Diff(li1, li2):
            return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))
        # get de toda la data
        # exe_exo_id es el id de el ejercicio que encontramos en c quiz
        cur1.execute('SELECT id FROM usuarios WHERE institucion = %s AND rol = %s', (institucion, '4'))
        user_id = cur1.fetchall()
        print(user_id)
        # exe_exo_id es el id de el ejercicio que encontramos en c quiz
        for usuario in user_id:
            try:
                cur2.execute('SELECT curso FROM usuarios WHERE id = %s', (usuario,))
                curso = cur2.fetchall()
                cur3.execute('SELECT id FROM grupos WHERE curso = %s', (curso,))
                grupo = cur3.fetchall()
                grupo = list(grupo)
                print('GRUPO=', grupo)
                cur4.execute('SELECT grupo FROM grupos_estudiantes WHERE estudiante = %s', (usuario,))
                grupos = cur4.fetchall()
                grupos = list(grupos)
                eliminar = Diff(grupo, grupos)
                print('grupos=', grupos)
                print(eliminar)

                if grupos:
                    if len(eliminar) != 0 and eliminar != grupo:
                        for kill in eliminar:
                            cur5.execute('DELETE FROM grupos_estudiantes WHERE grupo = %s', (kill,))
                            mysql2.commit()
                    else:
                        print('ok')
                else:
                    cur6.execute('INSERT into grupos_estudiantes (grupo, estudiante) VALUES (%s, %s)', (grupo, usuario))
                    mysql2.commit()


            except:
                print('Hubo una excepcion')
        return 'todo ok'