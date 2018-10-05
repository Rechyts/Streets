# encoding: utf8
import arcpy
import os
import pyodbc



sk_42 = "GEOGCS['GCS_Pulkovo_1942',DATUM['D_Pulkovo_1942',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.9830007334435E-09;0.001;0.001;IsHighPrecision"
sk63_1 = "PROJCS['CK1963(c)1',GEOGCS['GCS_Pulkovo_1942',DATUM['D_Pulkovo_1942',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',1250000.0],PARAMETER['False_Northing',-12900.568],PARAMETER['Central_Meridian',24.95],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-0.01666666666],UNIT['Meter',1.0]]"
sk63_2 = "PROJCS['CK1963(c)2',GEOGCS['GCS_Pulkovo_1942',DATUM['D_Pulkovo_1942',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',2250000.0],PARAMETER['False_Northing',-12900.568],PARAMETER['Central_Meridian',27.95],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-0.01666666666],UNIT['Meter',1.0]];-3373300 -10013300 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"
sk63_3 = "PROJCS['CK1963(c)3',GEOGCS['GCS_Pulkovo_1942',DATUM['D_Pulkovo_1942',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],PARAMETER['False_Easting',3250000.0],PARAMETER['False_Northing',-12900.568],PARAMETER['Central_Meridian',30.95],PARAMETER['Scale_Factor',1.0],PARAMETER['Latitude_Of_Origin',-0.01666666666],UNIT['Meter',1.0]]"
wgs84 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
district = {'Барановичский': 104,  'Берёзовский': 108,  'Брестский': 112,  'Ганцевичский': 116,  'Дрогичинский': 120,  'Жабинковский': 125,  'Ивановский': 130,  'Ивацевичский': 134,  'Каменецкий': 140,  'Кобринский': 143,  'Лунинецкий': 147,  'Ляховичский': 150,  'Малоритский': 152,  'Пинский': 154,  'Пружанский': 156,  'Столинский': 158,  'Бешенковичский': 205,  'Браславский': 208,  'Верхнедвинский': 210,  'Витебский': 212,  'Глубокский': 215,  'Городокский': 218,  'Докшицкий': 221,  'Дубровенский': 224,  'Лепельский': 227,  'Лиозненский': 230,  'Миорский': 233,  'Оршанский': 236,  'Полоцкий': 238,  'Поставский': 240,  'Россонский': 242,  'Сенненский': 244,  'Толочинский': 246,  'Ушачский': 249,  'Чашникский': 251,  'Шарковщинский': 255,  'Шумилинский': 258,  'Брагинский': 303,  'Буда-Кошелевский': 305,  'Ветковский': 308,  'Гомельский': 310,  'Добрушский': 312,  'Ельский': 314,  'Житковичский': 316,  'Жлобинский': 318,  'Калинковичский': 323,  'Кормянский': 325,  'Лельчицкий': 328,  'Лоевский': 330,  'Мозырский': 335,  'Наровлянский': 338,  'Октябрьский': 340,  'Петриковский': 343,  'Речицкий': 345,  'Рогачёвский': 347,  'Светлогорский': 350,  'Хойникский': 354,  'Чечерский': 356,  'Берестовицкий': 404,  'Волковысский': 408,  'Вороновский': 413,  'Гродненский': 420,  'Дятловский': 423,  'Зельвенский': 426,  'Ивьевский': 429,  'Кореличский': 433,  'Лидский': 436,  'Мостовский': 440,  'Новогрудский': 443,  'Островецкий': 446,  'Ошмянский': 449,  'Свислочский': 452,  'Слонимский': 454,  'Сморгонский': 456,  'Щучинский': 458,  'Березинский': 604,  'Борисовский': 608,  'Вилейский': 613,  'Воложинский': 620,  'Дзержинский': 622,  'Клецкий': 625,  'Копыльский': 628,  'Крупский': 630,  'Логойский': 632,  'Любанский': 634,  'Минский': 636,  'Молодечненский': 638,  'Мядельский': 640,  'Несвижский': 642,  'Пуховичский': 644,  'Слуцкий': 646,  'Смолевичский': 648,  'Солигорский': 650,  'Стародорожский': 652,  'Столбцовский': 654,  'Узденский': 656,  'Червенский': 658,  'Белыничский': 704,  'Бобруйский': 708,  'Быховский': 713,  'Глусский': 717,  'Горецкий': 720,  'Дрибинский': 723,  'Кировский': 725,  'Климовичский': 728,  'Кличевский': 730,  'Костюковичский': 735,  'Краснопольский': 738,  'Кричевский': 740,  'Круглянский': 742,  'Могилевский': 744,  'Мстиславский': 746,  'Осиповичский': 748,  'Славгородский': 750,  'Хотимский': 752,  'Чаусский': 754,  'Чериковский': 756,  'Шкловский': 758}
district_soato = {r'Барановичский': ('1204%', '1410%'),
                                r'Берёзовский': ('1208%', '0%'),
                                r'Брестский': ('1212%', '1401%'),
                                r'Ганцевичский': ('1216%', '0%'),
                                r'Дрогичинский': ('1220%', '0%'),
                                r'Жабинковский': ('1225%', '0%'),
                                r'Ивановский': ('1230%', '0%'),
                                r'Ивацевичский': ('1234%', '0%'),
                                r'Каменецкий': ('1240%', '0%'),
                                r'Кобринский': ('1243%', '0%'),
                                r'Лунинецкий': ('1247%', '0%'),
                                r'Ляховичский': ('1250%', '0%'),
                                r'Малоритский': ('1252%', '0%'),
                                r'Пинский': ('1254%', '1445%'),
                                r'Пружанский': ('1256%', '0%'),
                                r'Столинский': ('1258%', '0%'),
                                r'Бешенковичский': ('2205%', '0%'),
                                r'Браславский': ('2208%', '0%'),
                                r'Верхнедвинский': ('2210%', '0%'),
                                r'Витебский': ('2212%', '2401%'),
                                r'Глубокский': ('2215%', '0%'),
                                r'Городокский': ('2218%', '0%'),
                                r'Докшицкий': ('2221%', '0%'),
                                r'Дубровенский': ('2224%', '0%'),
                                r'Лепельский': ('2227%', '0%'),
                                r'Лиозненский': ('2230%', '0%'),
                                r'Миорский': ('2233%', '0%'),
                                r'Оршанский': ('2236%', '0%'),
                                r'Полоцкий': ('2238%', '2418%'),
                                r'Поставский': ('2240%', '0%'),
                                r'Россонский': ('2242%', '0%'),
                                r'Сенненский': ('2244%', '0%'),
                                r'Толочинский': ('2246%', '0%'),
                                r'Ушачский': ('2249%', '0%'),
                                r'Чашникский': ('2251%', '0%'),
                                r'Шарковщинский': ('2255%', '0%'),
                                r'Шумилинский': ('2258%', '0%'),
                                r'Брагинский': ('3203%', '0%'),
                                r'Буда-Кошелевский': ('3205%', '0%'),
                                r'Ветковский': ('3208%', '0%'),
                                r'Гомельский': ('3210%', '3401%'),
                                r'Добрушский': ('3212%', '0%'),
                                r'Ельский': ('3214%', '0%'),
                                r'Житковичский': ('3216%', '0%'),
                                r'Жлобинский': ('3218%', '0%'),
                                r'Калинковичский': ('3223%', '0%'),
                                r'Кормянский': ('3225%', '0%'),
                                r'Лельчицкий': ('3228%', '0%'),
                                r'Лоевский': ('3230%', '0%'),
                                r'Мозырский': ('3235%', '0%'),
                                r'Наровлянский': ('3238%', '0%'),
                                r'Октябрьский': ('3240%', '0%'),
                                r'Петриковский': ('3243%', '0%'),
                                r'Речицкий': ('3245%', '0%'),
                                r'Рогачевский': ('3247%', '0%'),
                                r'Светлогорский': ('3250%', '0%'),
                                r'Хойникский': ('3254%', '0%'),
                                r'Чечерский': ('3256%', '0%'),
                                r'Берестовицкий': ('4204%', '0%'),
                                r'Волковысский': ('4208%', '0%'),
                                r'Вороновский': ('4213%', '0%'),
                                r'Гродненский': ('4220%', '4401%'),
                                r'Дятловский': ('4223%', '0%'),
                                r'Зельвенский': ('4226%', '0%'),
                                r'Ивьевский': ('4229%', '0%'),
                                r'Кореличский': ('4233%', '0%'),
                                r'Лидский': ('4236%', '0%'),
                                r'Мостовский': ('4240%', '0%'),
                                r'Новогрудский': ('4243%', '0%'),
                                r'Островецкий': ('4246%', '0%'),
                                r'Ошмянский': ('4249%', '0%'),
                                r'Свислочский': ('4252%', '0%'),
                                r'Слонимский': ('4254%', '0%'),
                                r'Сморгонский': ('4256%', '0%'),
                                r'Щучинский': ('4258%', '0%'),
                                r'Березинский': ('6204%', '0%'),
                                r'Борисовский': ('6208%', '0%'),
                                r'Вилейский': ('6213%', '0%'),
                                r'Воложинский': ('6220%', '0%'),
                                r'Дзержинский': ('6222%', '0%'),
                                r'Клецкий': ('6225%', '0%'),
                                r'Копыльский': ('6228%', '0%'),
                                r'Крупский': ('6230%', '0%'),
                                r'Логойский': ('6232%', '0%'),
                                r'Любанский': ('6234%', '0%'),
                                'Минский': ('6236%', '0%'),
                                r'Молодечненский': ('6238%', '0%'),
                                r'Мядельский': ('6240%', '0%'),
                                r'Несвижский': ('6242%', '0%'),
                                r'Пуховичский': ('6244%', '0%'),
                                r'Слуцкий': ('6246%', '0%'),
                                r'Смолевичский': ('6248%', '6413%'),
                                r'Солигорский': ('6250%', '0%'),
                                r'Стародорожский': ('6252%', '0%'),
                                r'Столбцовский': ('6254%', '0%'),
                                r'Узденский': ('6256%', '0%'),
                                r'Червенский': ('6258%', '0%'),
                                r'Белыничский': ('7204%', '0%'),
                                r'Бобруйский': ('7208%', '7410%'),
                                r'Быховский': ('7213%', '0%'),
                                r'Глусский': ('7217%', '0%'),
                                r'Горецкий': ('7220%', '0%'),
                                r'Дрибинский': ('7223%', '0%'),
                                r'Кировский': ('7225%', '0%'),
                                r'Климовичский': ('7228%', '0%'),
                                r'Кличевский': ('7230%', '0%'),
                                r'Костюковичский': ('7235%', '0%'),
                                r'Краснопольский': ('7238%', '0%'),
                                r'Кричевский': ('7240%', '0%'),
                                r'Круглянский': ('7242%', '0%'),
                                r'Могилевский': ('7244%', '7401%'),
                                r'Мстиславский': ('7246%', '0%'),
                                r'Осиповичский': ('7248%', '0%'),
                                r'Славгородский': ('7250%', '0%'),
                                r'Хотимский': ('7252%', '0%'),
                                r'Чаусский': ('7254%', '0%'),
                                r'Чериковский': ('7256%', '0%'),
                                r'Шкловский': ('7258%', '0%'),
                                }


class Street(object):
    """
    Create DateBase for ArcGIS (*mdb), which contains setdata Streets with shp: 1. Streets(empty polyline layers with sybtypes
    (list of Selsovets and cities) and domains (list of streets in Selsovets or cities)), 2. ATE (polygon layer which contains settlement's boundaries),
    3.Selsovets(poligon layer which contains selsovet's boundaries), 3.Address(points layer which contains address of buildings and parsels),
    4.Topology_streets(topology which contains rules for layer streets: "Must Not Overlap With", "Must Not Overlap",
    "Must Be Inside" (polyline streets in polygon settlement's boundaries))
    """
    def __init__(self, name_district, work_path, login_to_DB, password_to_DB, path_to_layer_ate, name_layer_ate, path_to_maska):
        self.name_district = name_district
        self.work_path = work_path
        self.login_to_DB = login_to_DB
        self.password_to_DB = password_to_DB
        self.nameDataBase = os.path.join(self.work_path, '{0}_streets.mdb'.format(self.name_district))
        self.nameDataSet = os.path.join(self.nameDataBase, 'Streets')
        self.nameStreets = os.path.join(self.nameDataSet, 'Streets')
        self.path_to_layer_ate = path_to_layer_ate
        self.name_layer_ate = name_layer_ate
        self.path_to_maska = path_to_maska
        if self.name_district != 'Минск':
            self.list_sybtype()
        self.create_mdb_DateBase()
        if self.name_district == 'Витебский':
            self.create_table_EVA_Vitebsk()
        self.create_tables_EVA()
        self.create_domen_EVA_in_DateBase()
        if self.name_district != 'Минск':
            self.create_tables_ATE()
            self.create_domen_ATE_in_DateBase()
            self.create_layer_ate()
        if self.name_district == 'Минск':
            self.create_layer_minsk_ate()
        self.create_topology()
        self.create_layer_address()


    def list_sybtype(self):
        """
        Connect to DateBase ORACLE (Address system of the Republic of Belarus) and
        select from DataBase ATEREESTR dictionary of sybtypes (list of Selsovets and cities in chosen district)
        :return: dict of sybtypes (key: name Selsovet or city, value: list of ID Selsovet or city and ID category, which match to Selsovet or city)
        """
        # Connect to DataBase Reestr Address
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID="+self.login_to_DB+";PWD="+self.password_to_DB)
        cursor = conn.cursor()
        # SQL expression
        expression = """with tabl1 as (SELECT  * from ATEOBJECT r3 where r3.CATEGORY = 103 AND r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
 FROM ATEREESTR.ATEOBJECT r4
WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
GROUP BY r3.OBJECTNUMBER))
select r.OBJECTNUMBER,r.NAMEOBJECT,r.CATEGORY, x.SHORTNAME
from X_ATECATEGORY x, X_ATEDISTRICTS d, X_ATEREGION d1, ATEJOURNAL j, ATEOBJECT r

LEFT JOIN ATEJOURNAL j1 ON r.UIDOPEROUT = J1.UIDJRN
LEFT JOIN tabl1 t  ON r.SOATODEPEND = t.SOATO

Where
t.NAMEOBJECT is null and
r.act = 1 and
R.UIDDISTR = {name_district} and
r.CATEGORY = x.CATEGORY and
R.UIDDISTR = D.UIDDISTR and
R.UIDREGION = D1.UIDREGION and
r.UIDOPERIN = J.UIDJRN and
(r.CATEGORY in (103,112,113,121,122,123,212,213,221,222,223,203) OR r.OBJECTNUMBER in (6684, 26521)) AND r.OBJECTNUMBER <> 9387
order by r.NAMEOBJECT
        """.format(name_district=district[self.name_district])
        cursor.execute(expression)

        # dict of sybtypes (key: name Selsovet or city, value: list of ID Selsovet or city and ID category, which match to Selsovet or city)
        self.dict_sybtypes = {}
        for element in cursor.fetchall():
            if element[2] == 103:
                self.dict_sybtypes[element[1].encode('utf-8')] = [int(element[0]), int(element[2])]
            elif element[2] == 203:
                self.dict_sybtypes['ВеликийКамень'] = [int(element[0]), int(element[2])]
            else:
                self.dict_sybtypes['{0}{1}'.format(element[3].encode('utf-8'), element[1].encode('utf-8'))] = [
                    int(element[0]), int(element[2])]
        # Delete points, dash etc. in keys(name Selsovets or cities)
        list_without = """'"-. """
        self.new_dict_syptypes = {}
        for name_sybtypes in self.dict_sybtypes:
            list_name_sybtypes = list(name_sybtypes)
            for without in list_without:
                if without in list_name_sybtypes:
                    while without in list_name_sybtypes:
                        list_name_sybtypes.remove(without)
            self.new_dict_syptypes[''.join(list_name_sybtypes)] = self.dict_sybtypes[name_sybtypes]
        return self.new_dict_syptypes

    def create_mdb_DateBase(self):
            """
            Create *mdb DataBase with DateSet, and polyline layer with fields ("Name_ATE", "Name", "Name_EVA", "ID_ATE", "ID_EVA").
            Set sybtype for field "Name_ATE" and add sybtypes.
            :return: DateBase
            """
            # create mdb
            arcpy.CreatePersonalGDB_management(self.work_path, '{0}_streets.mdb'.format(self.name_district))
            # create dataset Streets
            arcpy.CreateFeatureDataset_management(self.nameDataBase, "Streets", wgs84)
            # create shp Streets
            arcpy.CreateFeatureclass_management(self.nameDataSet, "Streets", "POLYLINE", "", "DISABLED", "DISABLED", wgs84, "", "0", "0", "0")
            # create fields in shp Streets
            arcpy.AddField_management(self.nameStreets, "Name_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(self.nameStreets, "Name", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(self.nameStreets, "Name_EVA", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(self.nameStreets, "ID_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(self.nameStreets, "ID_EVA", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            # set Sybtypefield - Name_ATE
            arcpy.SetSubtypeField_management(self.nameStreets, "Name_ATE")
            # create sybtypes in DateBase
            if self.name_district != "Минск":
                for element in self.new_dict_syptypes.items():
                    arcpy.AddSubtype_management(self.nameStreets,  element[1][0], element[0])
            else:
                arcpy.AddSubtype_management(self.nameStreets, 17030, 'Минск')


    def select_table_EVA(self):
        """
        Connect to DateBase ORACLE and
        select from DataBase IAE (DateBase Streets of the Republic of Belarus) streets in chosen district
        :return: list of streets in chosen district
        """
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login_to_DB + ";PWD=" + self.password_to_DB)
        cursor = conn.cursor()
        # SQL expression
        expression = """with tabl1 as (SELECT  * from ATEOBJECT r3 where r3.CATEGORY = 103 AND r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
FROM ATEREESTR.ATEOBJECT r4
WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
GROUP BY r3.OBJECTNUMBER))

SELECT j.IAEUID AS "ID_EVA", j.OBJECTNUMBER as "ID_ATE",  j.ELEMENTNAME, x.SHORTNAME_RUS,  R.NAMEOBJECT, p.SHORTNAME, t.OBJECTNUMBER as "SELSOV", r.CATEGORY, j.ELEMENTTYPE

FROM IAE.ADRELEMENTS j, ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTS i, ATEREESTR.X_ATEREGION g, NKA_SPR.X_EVA_TYPES_ADDR x, ATEREESTR.ATEOBJECT r

LEFT JOIN tabl1 t  ON r.SOATODEPEND = t.SOATO
LEFT JOIN ATEREESTR.X_ATECATEGORY p2 ON t.CATEGORY = p2.CATEGORY

where r.UIDOPEROUT is null and  j.OBJECTNUMBER = R.OBJECTNUMBER and R.UIDDISTR = I.UIDDISTR and R.UIDREGION = G.UIDREGION and R.CATEGORY = p.CATEGORY and  j.JRNREG_OUT is null and j.ELEMENTTYPE < 50 and R.UIDDISTR = {name_district} and R.OBJECTNUMBER <> 17030 and r.OBJECTNUMBER <> 9387 and x.CODE_1 =  j.ELEMENTTYPE

order by R.NAMEOBJECT, j.ELEMENTNAME""".format(name_district=district[self.name_district])
        cursor.execute(expression)
        return cursor.fetchall()

    def select_table_minsk_EVA(self):
        """
        Connect to DateBase ORACLE and
        select from DataBase IAE (DateBase Streets of the Republic of Belarus) streets in Minsk (capital of the Republic of Belarus)
        :return: list of streets in Minsk
        """
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login_to_DB + ";PWD=" + self.password_to_DB)
        cursor = conn.cursor()
        # SQL expression
        expression = """with tabl1 as (SELECT  * from ATEOBJECT r3 where r3.CATEGORY = 103 AND r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
        FROM ATEREESTR.ATEOBJECT r4
        WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
        GROUP BY r3.OBJECTNUMBER))

        SELECT j.IAEUID AS "ID_EVA", j.OBJECTNUMBER as "ID_ATE",  j.ELEMENTNAME, x.SHORTNAME_RUS,  R.NAMEOBJECT, p.SHORTNAME, t.OBJECTNUMBER as "SELSOV", r.CATEGORY, j.ELEMENTTYPE

        FROM IAE.ADRELEMENTS j, ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTS i, ATEREESTR.X_ATEREGION g, NKA_SPR.X_EVA_TYPES_ADDR x, ATEREESTR.ATEOBJECT r

        LEFT JOIN tabl1 t  ON r.SOATODEPEND = t.SOATO
        LEFT JOIN ATEREESTR.X_ATECATEGORY p2 ON t.CATEGORY = p2.CATEGORY

        where r.UIDOPEROUT is null and  j.OBJECTNUMBER = R.OBJECTNUMBER and R.UIDDISTR = I.UIDDISTR and R.UIDREGION = G.UIDREGION and R.CATEGORY = p.CATEGORY and  j.JRNREG_OUT is null and j.ELEMENTTYPE < 50 and  R.OBJECTNUMBER = 17030 and x.CODE_1 =  j.ELEMENTTYPE

        order by R.NAMEOBJECT, j.ELEMENTNAME"""
        cursor.execute(expression)
        return cursor.fetchall()


    def create_tables_EVA(self):
        """
        Create tables (format - .dbf), which containes information about streets in selsovet or cities
        :return: tables streets .dbf
        """
        self.list_domen_tables_EVA = []
        if self.name_district != 'Минск':
            for element in self.new_dict_syptypes.items():
                arcpy.CreateTable_management(self.nameDataBase, "{0}_EVA".format(element[0]), "", "")
                name_etalon_eva = os.path.join(self.nameDataBase, "{0}_EVA".format(element[0]))
                self.list_domen_tables_EVA.append(name_etalon_eva)
                arcpy.AddField_management(name_etalon_eva, "ID_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
                arcpy.AddField_management(name_etalon_eva, "ID_EVA", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
                arcpy.AddField_management(name_etalon_eva, "Name_EVA", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
                cursor_arc = arcpy.da.InsertCursor(name_etalon_eva, ["ID_ATE", "ID_EVA", "Name_EVA"])

                for el in self.select_table_EVA():
                    # this clause if: elemen[0] is field ID_ATE from table Sybtypes == el[6] is field Selsov from table_EVA
                    if element[1][0] == el[6]:
                        cursor_arc.insertRow([el[1], el[0], '{0}_{1}_{2}_{3}'.format(el[2].encode('utf-8'), el[3].encode('utf-8'), el[4].encode('utf-8'), el[5].encode('utf-8'))])
                    # this clause if: field Selsov from table_EVA is null and field ID_ATE from table table_EVA == field ID_ATE from table Sybtypes (only city, towns etc)
                    elif el[6] is None and el[1] == element[1][0]:
                        cursor_arc.insertRow([el[1], el[0], '{0}_{1}'.format(el[2].encode('utf-8'), el[3].encode('utf-8'))])
                    else:
                        pass

        else:
            arcpy.CreateTable_management(self.nameDataBase, "Минск_EVA", "", "")
            name_etalon_eva = os.path.join(self.nameDataBase, "Минск_EVA")
            self.list_domen_tables_EVA.append(name_etalon_eva)
            arcpy.AddField_management(name_etalon_eva, "ID_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(name_etalon_eva, "ID_EVA", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            arcpy.AddField_management(name_etalon_eva, "Name_EVA", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
            cursor_arc = arcpy.da.InsertCursor(name_etalon_eva, ["ID_ATE", "ID_EVA", "Name_EVA"])
            for el in self.select_table_minsk_EVA():
                cursor_arc.insertRow([el[1], el[0], '{0}_{1}'.format(el[2].encode('utf-8'), el[3].encode('utf-8'))])

    def create_domen_EVA_in_DateBase(self):
        """
        Create domains streets in DateBase from tables streets and delete table streets
        :return: domain streets
        """
        for domen_table_EVA in self.list_domen_tables_EVA:
            #Create domen EVA from domen_table
            arcpy.TableToDomain_management(domen_table_EVA, "ID_EVA", "Name_EVA", self.nameDataBase, domen_table_EVA.split("""\\""")[-1], "EVA", "APPEND")
            #Delete domen_table in DateBase
            arcpy.Delete_management(domen_table_EVA, "Table")
            if self.name_district != "Минск":
                arcpy.AssignDomainToField_management(self.nameStreets, 'Name_EVA', domen_table_EVA.split("""\\""")[-1], self.new_dict_syptypes[domen_table_EVA.split("""\\""")[-1].split('_')[0]][0])
            else:
                arcpy.AssignDomainToField_management(self.nameStreets, 'Name_EVA', domen_table_EVA.split("""\\""")[-1], 17030)

    def select_table_ATE(self):
        """
        Connect to DateBase ORACLE and
        select from DataBase Reestrate list of settlements in chosen district
        :return: list of settlements in district
        """
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login_to_DB + ";PWD=" + self.password_to_DB)
        cursor = conn.cursor()
        # SQL expression
        expression = """with tabl1 as (SELECT  * from ATEOBJECT r3 where r3.CATEGORY = 103 AND r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
FROM ATEREESTR.ATEOBJECT r4
WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
GROUP BY r3.OBJECTNUMBER))

select r.OBJECTNUMBER,r.NAMEOBJECT,x.SHORTNAME,t.OBJECTNUMBER as selsovet
from X_ATECATEGORY x, X_ATEDISTRICTS d, X_ATEREGION d1, ATEJOURNAL j, ATEOBJECT r

LEFT JOIN ATEJOURNAL j1 ON r.UIDOPEROUT = J1.UIDJRN
LEFT JOIN tabl1 t  ON r.SOATODEPEND = t.SOATO

Where
r.act = 1 and
R.UIDDISTR = {name_district} and
t.OBJECTNUMBER is not null and
r.CATEGORY = x.CATEGORY and
R.UIDDISTR = D.UIDDISTR and
R.UIDREGION = D1.UIDREGION and
r.UIDOPERIN = J.UIDJRN and
r.CATEGORY in (101,102,103,111,112,113,121,122,123,202,212,213,221,222,223,231,232,233,234,239,235)
order by t.NAMEOBJECT, r.NAMEOBJECT""".format(name_district=district[self.name_district])
        cursor.execute(expression)
        return cursor.fetchall()

    def create_tables_ATE(self):
        """
        Create table ATE .dbf in DateBase, which containes information about settlements
        :return: table ATE .dbf in DateBase
        """
        self.list_domen_tables_ATE = []
        for element in self.new_dict_syptypes.items():
            if element[1][1] == 103:
                arcpy.CreateTable_management(self.nameDataBase, '{0}_ATE'.format(element[0]), "", "")
                name_etalon_ate = os.path.join(self.nameDataBase, '{0}_ATE'.format(element[0]))
                self.list_domen_tables_ATE.append(name_etalon_ate)
                arcpy.AddField_management(name_etalon_ate, "ID_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
                arcpy.AddField_management(name_etalon_ate, "Name_ATE", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
                cursor_arc = arcpy.da.InsertCursor(name_etalon_ate, ["ID_ATE", "Name_ATE"])
                for el in self.select_table_ATE():
                    if el[3] == element[1][0]:
                        cursor_arc.insertRow([el[0], '{0}_{1}'.format(el[1].encode('utf-8'), el[2].encode('utf-8'))])
                    else:
                        pass

    def create_domen_ATE_in_DateBase(self):
        """
        Create domain ATE, which containes list of settlements in chosen district
        :return: domain ATE in DateBase
        """
        for domen_table_ATE in self.list_domen_tables_ATE:
            #Create domen EVA from domen_table
            arcpy.TableToDomain_management(domen_table_ATE, "ID_ATE", "Name_ATE", self.nameDataBase, domen_table_ATE.split("""\\""")[-1], "ATE", "APPEND")
            #Delete domen_table in DateBase
            arcpy.Delete_management(domen_table_ATE, "Table")
            arcpy.AssignDomainToField_management(self.nameStreets, 'Name', domen_table_ATE.split("""\\""")[-1], self.new_dict_syptypes[domen_table_ATE.split("""\\""")[-1].split('_')[0]][0])

    def create_layer_ate(self):
        """
        create layers ATE (boundaris of settlements) an Selsovets (boundaries of Selsovets) from layer .shp (rb.shp, coordinate system -  geografic CS Pulkovo-1942)
        :param path_to_layer_ate: path where we put layer rb.shp in GCS Pulkovo-1942, which containes boundaries of Selsovets and settlements
        :param name_layer_ate: name layer (.shp), which containes boundaries of Selsovets and settlements
        :return: two layer: ATE and Selsovets in DateBase, WGS-84
        """
        shp = r'{0}\{1}1.shp'.format(self.path_to_layer_ate, self.name_district)
        shp_sk = r'{0}\{1}_sk.shp'.format(self.path_to_layer_ate, self.name_district)
        shp_city = r'{0}\ATE.shp'.format(self.path_to_layer_ate)
        shp_ss = r'{0}\Selsovets.shp'.format(self.path_to_layer_ate)
        tempEnvironment0 = arcpy.env.outputCoordinateSystem
        arcpy.env.outputCoordinateSystem = sk_42

        arcpy.Select_analysis(os.path.join(self.path_to_layer_ate, self.name_layer_ate), shp,
                              "\"SOATO\" LIKE '{0}' OR \"SOATO\" LIKE '{1}'".format(district_soato[self.name_district][0],district_soato[self.name_district][1]))
        arcpy.env.outputCoordinateSystem = tempEnvironment0

        arcpy.Project_management(shp, shp_sk, wgs84, "CK42_to_ITRF2005", sk_42)

        arcpy.Select_analysis(shp_sk, shp_city,
                              "CATEGORY = 111 OR CATEGORY = 112 OR CATEGORY= 121 OR CATEGORY= 113 OR CATEGORY= 123 OR CATEGORY = 213 OR CATEGORY= 221 OR CATEGORY= 223 OR CATEGORY= 222 OR CATEGORY= 231 OR CATEGORY= 232 OR CATEGORY= 234 OR CATEGORY= 235 OR CATEGORY= 239")
        arcpy.Select_analysis(shp_sk, shp_ss, "\"CATEGORY\" =103")

        for root, dirs, files in os.walk(self.path_to_layer_ate):
            for file in files:
                if file.find('1') > - 1 or file.find('_sk') > - 1:
                    os.remove('{0}\{1}'.format(self.path_to_layer_ate, file))
        try:
            arcpy.FeatureClassToGeodatabase_conversion("{0};{1}".format(shp_city, shp_ss), self.nameDataSet)
        except:
            print "This layer's been in DateBase yet"

        # удаление шейпов ATE, Selsovets
        for root, dirs, files in os.walk(self.path_to_layer_ate):
            for file in files:
                if file.find('ATE') > - 1 or file.find('Selsovets') > - 1:
                    os.remove('{0}\{1}'.format(self.path_to_layer_ate, file))


    def create_layer_minsk_ate(self):
        """
        create layes ATE, which contain boundary of Minsk from layer rb.shp GCS Pulkovo-1942
        :return: ATE(boundary Minsk), WGS-84
        """
        shp = r'{0}\{1}1.shp'.format(self.path_to_layer_ate, self.name_district)
        shp_sk = r'{0}\ATE.shp'.format(self.path_to_layer_ate, self.name_district)


        tempEnvironment0 = arcpy.env.outputCoordinateSystem
        arcpy.env.outputCoordinateSystem = sk_42

        arcpy.Select_analysis(os.path.join(self.path_to_layer_ate, self.name_layer_ate), shp,
                              "REGN = 17030")
        arcpy.env.outputCoordinateSystem = tempEnvironment0

        arcpy.Project_management(shp, shp_sk, wgs84, "CK42_to_ITRF2005", sk_42)


        for root, dirs, files in os.walk(self.path_to_layer_ate):
            for file in files:
                if file.find('1') > - 1:
                    os.remove('{0}\{1}'.format(self.path_to_layer_ate, file))
        try:
            arcpy.FeatureClassToGeodatabase_conversion(shp_sk, self.nameDataSet)
        except:
            print "This layer's been in DateBase yet"

        # удаление шейпов ATE, Selsovets
        for root, dirs, files in os.walk(self.path_to_layer_ate):
            for file in files:
                if file.find('ATE') > - 1:
                    os.remove('{0}\{1}'.format(self.path_to_layer_ate, file))


    def create_topology(self):
        """
        Create topology. participate two layers: ATE and Streets
        :return: topology in datebaseset Streets
        """
        Streets_Topology = os.path.join(self.nameDataSet, "Streets_Topology")
        ate = os.path.join(self.nameDataSet, "ate")
        arcpy.CreateTopology_management(self.nameDataSet, "Streets_Topology", "")
        arcpy.AddFeatureClassToTopology_management(Streets_Topology, self.nameStreets, "1", "1")
        arcpy.AddFeatureClassToTopology_management(Streets_Topology, ate, "1", "1")
        arcpy.AddRuleToTopology_management(Streets_Topology, "Must Not Overlap (Line)", self.nameStreets, "", "", "")
        arcpy.AddRuleToTopology_management(Streets_Topology, "Must Not Self-Overlap (Line)", self.nameStreets, "", "","")
        arcpy.AddRuleToTopology_management(Streets_Topology, "Must Be Inside (Line-Area)", self.nameStreets, "", ate, "")

    def create_layer_address(self):
        """
        Connect to DateBase Address system of the Republic of Belarus and select necessary fields and objects
        create layer address by one district from database RADR
        :param Name: name district
        :param path: path to work folder
        :return: shp address in datebase .mdb, WGS84
        """

        # constant variables
        name_address = os.path.join(self.nameDataBase, 'address42')
        maska_Select = os.path.join(self.work_path, 'maska_Select.shp')
        address_cor = os.path.join(self.nameDataBase, 'address_cor')
        address = os.path.join(self.nameDataSet, 'address')

        # Connect to DataBase Reestr Address
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=GRUDINSKAYA;PWD=1109nik")
        cursor = conn.cursor()

        if self.name_district != 'Минск':
        # SQL expression
            expression = """with tab1 as (SELECT max (ID_ADR) mID_ADR, ADR_NUM mADR_NUM from RADR.ADDRESSES GROUP BY ADR_NUM)

            SELECT  t.PROP_TYPE AS "PROP_TYPE", mADR_NUM AS "ADR_NUM ", s.NAME AS "ADR_STATUS",t.OBJ_ID as "ID_ATE",k.ID_EVA,r2. NAMEOBJECT AS "NAMESELSOV",P.SHORTNAME as "ATE_TYPE", r. NAMEOBJECT AS "ATE_NAME", c. ELEMENTTYPENAME AS "EVA_TYPE",c.ELEMENTNAME AS "EVA_NAME",k.NUM_HOUSE, k.NUM_CORP, k.IND_HOUSE, k.KM,t.REMARK, B.DATE_OPER AS "DATE", t.BCOORD, t.LCOORD

            FROM
            ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTs i, ATEREESTR.X_ATEREGION g, RADR.TYPE_SPECIF s, RADR.REF_INADR d, RADR.OPER b,
            ATEREESTR.ATEOBJECT r
            left JOIN ( SELECT * from ATEREESTR.ATEOBJECT r3 where r3.CATEGORY =103
            AND   r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
            FROM ATEREESTR.ATEOBJECT r4
            WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
             GROUP BY r3. OBJECTNUMBER) ) r2  on r.SOATODEPEND=r2.SOATO,
            RADR.ADDRESSES t
            left JOIN RADR.INDEXES e ON t.ID_INDEX=e.ID_INDEX,
            RADR.INTERNAL_ADR k
            Left JOIN (SELECT * FROM IAE.ADRELEMENTS c1
            WHERE  c1.JRNREG_IN = (SELECT MAX (c2. JRNREG_IN)
            FROM IAE.ADRELEMENTS c2
            WHERE c1. IAEUID = c2. IAEUID
             GROUP BY c2. IAEUID)) c ON k.ID_EVA = c. IAEUID, tab1

            WHERE

            r.UIDOPERIN = (SELECT MAX (r1.UIDOPERIN)
            FROM ATEREESTR.ATEOBJECT r1
            WHERE t. OBJ_ID=r1.OBJECTNUMBER
            GROUP BY R1.OBJECTNUMBER)
            AND  t.BCOORD is not null AND t.OPER_IN=b.ID_OPER AND  t.ID_ADR= d.ID_ADR AND mID_ADR=t.ID_ADR AND k.ID_IN_ADR=d.ID_IN_ADR AND t.PROP_TYPE IN (1,2,4) AND t.ACTUAL is null  AND t.OBJ_ID= r. OBJECTNUMBER AND  p.CATEGORY=r.CATEGORY AND i.UIDDISTR=r.UIDDISTR  AND g.UIDREGION=r.UIDREGION AND  s. ID_SPEC=t. KOD_SPEC AND d.OPER_OUT is null AND r.UIDDISTR={distr} and t.OBJ_ID <> 17030

            ORDER BY r.SOATO""".format(distr=district[self.name_district])
        else:
            expression = """with tab1 as (SELECT max (ID_ADR) mID_ADR, ADR_NUM mADR_NUM from RADR.ADDRESSES GROUP BY ADR_NUM)

                       SELECT  t.PROP_TYPE AS "PROP_TYPE", mADR_NUM AS "ADR_NUM ", s.NAME AS "ADR_STATUS",t.OBJ_ID as "ID_ATE",k.ID_EVA,r2. NAMEOBJECT AS "NAMESELSOV",P.SHORTNAME as "ATE_TYPE", r. NAMEOBJECT AS "ATE_NAME", c. ELEMENTTYPENAME AS "EVA_TYPE",c.ELEMENTNAME AS "EVA_NAME",k.NUM_HOUSE, k.NUM_CORP, k.IND_HOUSE, k.KM,t.REMARK, B.DATE_OPER AS "DATE", t.BCOORD, t.LCOORD

                       FROM
                       ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTs i, ATEREESTR.X_ATEREGION g, RADR.TYPE_SPECIF s, RADR.REF_INADR d, RADR.OPER b,
                       ATEREESTR.ATEOBJECT r
                       left JOIN ( SELECT * from ATEREESTR.ATEOBJECT r3 where r3.CATEGORY =103
                       AND   r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
                       FROM ATEREESTR.ATEOBJECT r4
                       WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
                        GROUP BY r3. OBJECTNUMBER) ) r2  on r.SOATODEPEND=r2.SOATO,
                       RADR.ADDRESSES t
                       left JOIN RADR.INDEXES e ON t.ID_INDEX=e.ID_INDEX,
                       RADR.INTERNAL_ADR k
                       Left JOIN (SELECT * FROM IAE.ADRELEMENTS c1
                       WHERE  c1.JRNREG_IN = (SELECT MAX (c2. JRNREG_IN)
                       FROM IAE.ADRELEMENTS c2
                       WHERE c1. IAEUID = c2. IAEUID
                        GROUP BY c2. IAEUID)) c ON k.ID_EVA = c. IAEUID, tab1

                       WHERE

                       r.UIDOPERIN = (SELECT MAX (r1.UIDOPERIN)
                       FROM ATEREESTR.ATEOBJECT r1
                       WHERE t. OBJ_ID=r1.OBJECTNUMBER
                       GROUP BY R1.OBJECTNUMBER)
                       AND  t.BCOORD is not null AND t.OPER_IN=b.ID_OPER AND  t.ID_ADR= d.ID_ADR AND mID_ADR=t.ID_ADR AND k.ID_IN_ADR=d.ID_IN_ADR AND t.PROP_TYPE IN (1,2,4) AND t.ACTUAL is null  AND t.OBJ_ID= r. OBJECTNUMBER AND  p.CATEGORY=r.CATEGORY AND i.UIDDISTR=r.UIDDISTR  AND g.UIDREGION=r.UIDREGION AND  s. ID_SPEC=t. KOD_SPEC AND d.OPER_OUT is null AND t.OBJ_ID = 17030

                       ORDER BY r.SOATO"""

        # Execution SQL exprission
        cursor.execute(expression)

        # Create shp address in DataBase
        arcpy.CreateFeatureclass_management(self.nameDataBase, "address42", 'POINT', "", "DISABLED", "DISABLED", sk_42, "",
                                            "0", "0", "0")

        # Create fields in shp address
        arcpy.AddField_management(name_address, "PROP_TYPE", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ADR_NUM", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ADR_STATUS", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ID_ATE", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ID_EVA", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "NAMESELSOV", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ATE_TYPE", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "ATE_NAME", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "EVA_TYPE", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "EVA_NAME", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "NUM_HOUSE", "DOUBLE", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "NUM_CORP", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "IND_HOUSE", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "KM", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "REMARK", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_address, "DATEREG", "DATE", "", "", "", "", "NULLABLE", "REQUIRED", "")

        cursor_arc = arcpy.da.InsertCursor(name_address,
                                           ["PROP_TYPE", "ADR_NUM", "ADR_STATUS", "ID_ATE", "ID_EVA", "NAMESELSOV",
                                            "ATE_TYPE", "ATE_NAME", "EVA_TYPE", "EVA_NAME", "NUM_HOUSE", "NUM_CORP",
                                            "IND_HOUSE", "KM", "REMARK", "DATEREG", "SHAPE@XY"])

        for element in cursor.fetchall():
            cursor_arc.insertRow(list(element[:-2]) + [(element[-1], element[-2])])

        cursor.close()
        conn.close()

        arcpy.Project_management(name_address, address_cor, wgs84, "CK42_to_ITRF2005", sk_42)


        # in layer maska choose district and clip layer address and export in dateset DateBase
        if self.name_district != 'Минск':
            arcpy.Select_analysis(self.path_to_maska, maska_Select, "\"uid\" = {0}".format(district[self.name_district]))
        else:
            arcpy.Select_analysis(self.path_to_maska, maska_Select, "\"uid\" = 17030")
        arcpy.Clip_analysis(address_cor, maska_Select, address, "")




        # Delete shp from DataBase
        arcpy.Delete_management(name_address, "FeatureClass")
        arcpy.Delete_management(address_cor, "FeatureClass")

        # Delete layer maska_Select
        for root, dirs, files in os.walk(self.work_path):
            for file in files:
                if file.find('maska_Select') > - 1:
                    os.remove('{0}/{1}'.format(self.work_path, file))

    def create_table_EVA_Vitebsk(self):
        """
        This function is created only for city Vitebsk, cause it didn't work correctly.
        :return: domain and sybtypes Vitebsk in DateBase Vitebski district
        """
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login_to_DB + ";PWD=" + self.password_to_DB)
        cursor = conn.cursor()
        # SQL expression
        expression = """with tabl1 as (SELECT  * from ATEOBJECT r3 where r3.CATEGORY = 103 AND r3.UIDOPERIN=( SELECT MAX (r4.UIDOPERIN)
                FROM ATEREESTR.ATEOBJECT r4
                WHERE r3.OBJECTNUMBER=r4.OBJECTNUMBER
                GROUP BY r3.OBJECTNUMBER))

                SELECT j.IAEUID AS "ID_EVA", j.OBJECTNUMBER as "ID_ATE",  j.ELEMENTNAME, x.SHORTNAME_RUS,  R.NAMEOBJECT, p.SHORTNAME, t.OBJECTNUMBER as "SELSOV", r.CATEGORY, j.ELEMENTTYPE

                FROM IAE.ADRELEMENTS j, ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTS i, ATEREESTR.X_ATEREGION g, NKA_SPR.X_EVA_TYPES_ADDR x, ATEREESTR.ATEOBJECT r

                LEFT JOIN tabl1 t  ON r.SOATODEPEND = t.SOATO
                LEFT JOIN ATEREESTR.X_ATECATEGORY p2 ON t.CATEGORY = p2.CATEGORY

                where r.UIDOPEROUT is null and  j.OBJECTNUMBER = R.OBJECTNUMBER and R.UIDDISTR = I.UIDDISTR and R.UIDREGION = G.UIDREGION and R.CATEGORY = p.CATEGORY and  j.JRNREG_OUT is null and j.ELEMENTTYPE < 50 and  R.OBJECTNUMBER = 9387 and x.CODE_1 =  j.ELEMENTTYPE

                order by R.NAMEOBJECT, j.ELEMENTNAME"""
        cursor.execute(expression)
        self.table_EVA_Vitebsk = cursor.fetchall()
        arcpy.AddSubtype_management(self.nameStreets, 9387, "Витебск")
        arcpy.CreateTable_management(self.nameDataBase, "Витебск_EVA", "", "")
        name_etalon_eva = os.path.join(self.nameDataBase, "Витебск_EVA")
        arcpy.AddField_management(name_etalon_eva, "ID_ATE", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_etalon_eva, "ID_EVA", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
        arcpy.AddField_management(name_etalon_eva, "Name_EVA", "TEXT", "", "", "", "", "NULLABLE", "REQUIRED", "")
        cursor_arc = arcpy.da.InsertCursor(name_etalon_eva, ["ID_ATE", "ID_EVA", "Name_EVA"])
        for el in self.table_EVA_Vitebsk:
            cursor_arc.insertRow([el[1], el[0], '{0}_{1}'.format(el[2].encode('utf-8'), el[3].encode('utf-8'))])

        arcpy.TableToDomain_management(name_etalon_eva, "ID_EVA", "Name_EVA", self.nameDataBase, "Витебск_EVA", "EVA", "APPEND")
        # arcpy.AssignDomainToField_management(self.nameStreets, "Name_EVA", "Витебск_EVA", 9387)
        arcpy.Delete_management(name_etalon_eva, "Table")
