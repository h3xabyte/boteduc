import pymysql
import uuid
import datetime
import os
import base64
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self): # Objeto de base de datos
        self.global_sie = pymysql.connect(host="educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com", user="EducarDB", passwd="Db2020!", db="global_sie")
        self.sie_cur = self.global_sie.cursor()
        ######chm
        self.chamilo = pymysql.connect(host="educar2020db.c6r9vkodxz44.us-east-1.rds.amazonaws.com", user="EducarDB", passwd="Db2020!", db="2018_chm_lms_demo")
        self.chm_cur = self.chamilo.cursor()
        ##aula2
        self.chm2 = pymysql.connect(host='db-produccion-educarsie2-serveless.cluster-cxlnmcx1f2mz.us-east-2.rds.amazonaws.com',
                         user="superadmin_prod",
                         passwd="%Educ4r2020%",
                         db="2018_chm_lms_demo")
        self.chm2_cur = self.chm2.cursor()




 # Insercion de grados 1, 2 ,3 ,P, J, T
    def grados_insert(self, institucion, grado):



     try:
         consulta = self.sie_cur.execute('INSERT INTO cursos (grado, institucion) VALUES (%s, %s)', (grado, institucion))
         self.global_sie.commit()



         return {
        "ok": 'insercion correcta',


    }
     except:
           return {
        "fail": 'insercion fallida',


    }

 # Obtener lista de grados
    def grados_obtener(self, institucion):


         consulta = self.sie_cur.execute('SELECT grado FROM cursos WHERE institucion =%s', (institucion,))
         resultado = self.sie_cur.fetchall()
         print(resultado)


         return resultado

 # Insercion de cursos en los grados = '1-A', '2-B', '1-01'.
    def grado_y_curso(self, institucion, curso):


        combo = curso.split("-")
        param={
        "grado": combo[0],
        "grupo": combo[1]
        }
        consulta1 = self.sie_cur.execute('SELECT id FROM cursos WHERE grado =%s AND institucion =%s', (combo[0], institucion))
        idgrado=self.sie_cur.fetchall()

        try:
             consulta2 = self.sie_cur.execute('INSERT INTO grupos (curso, grupo) VALUES (%s, %s)', (idgrado, combo[1]))
             self.global_sie.commit()



             return {
            "ok": 'insercion de grados correcta',


             }
        except:
            return "fallo la insercion de grados"

    #obtener grados --------
    def get_grados(self, institucion):



     consulta = self.sie_cur.execute('SELECT a.grado, b.grupo FROM cursos as a, grupos as b WHERE a.institucion = %s AND a.id = b.curso', (institucion,))
     grados = self.sie_cur.fetchall()



     return grados

    #Crear materias----
    def crear_materias(self, institucion, materia):

     try:
         insercion = self.sie_cur.execute('INSERT into materias (materia, institucion) VALUES (%s, %s)', (materia, institucion))
         self.global_sie.commit()


         return "Materia creada"





     except:
         return "fallo la creacion"


    #Obtener materias----
    def obtener_materias(self, institucion):

     self.sie_cur.execute('SELECT materia FROM materias WHERE institucion =%s', (institucion,))
     materias = self.sie_cur.fetchall()



     return materias

    #quitar botones----
    def quitar_botones(self, institucion):

     self.chm2_cur.execute('SELECT id FROM course WHERE category_code =%s', (institucion,))
     c_ids = self.chm2_cur.fetchall()
     for curso in c_ids:

         curso = ''.join(map(str, curso))
         curso = curso.replace('(','').replace(')', '').replace(',', '')
         names = ['bbb', 'course_maintenance', 'course_setting', 'blog_management', 'tracking', 'survey', 'user']
         for nombre in names:

             try:
                 self.chm2_cur.execute('DELETE FROM c_tool WHERE c_id=%s AND name=%s', (curso, nombre))

                 status = 'OK'
             except:
                 status = 'fallo'

     self.chm2.commit()

     return 'Botones Ajustados', status
