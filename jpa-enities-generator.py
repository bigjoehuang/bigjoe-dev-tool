import os
import time 
import mysql.connector
from string import Template

baseOutputDir = "./output/"  
packageName = "org.bigjoe.demo.entity"

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="test"
)

#---------------------------------------------------------------------------
date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def underscore_to_camelcase(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

def getFieldType(columnType):
    type = 'String'         
    if (columnType.startswith('int')):
        type = 'Integer'
    elif (columnType.startswith('bigint')):
        type = 'Long'
    elif (columnType.startswith('decimal')):
        type = 'java.math.BigDecimal'
    elif (columnType.startswith('datetime') or columnType.startswith('timestamp')):
        type = 'java.util.Date'    

    return type    

if __name__ == '__main__':
    path = baseOutputDir + str.replace(packageName, '.', '/')
    if not os.path.exists(path):
        os.makedirs(path)

    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(table_name)
        entityName = table_name
        className = underscore_to_camelcase(table_name)

        cursor.execute("DESCRIBE {}".format(table_name))
        schema = cursor.fetchall()

        with open("tpl.java", encoding='utf-8') as fp:
            read_yml_str = fp.read()
            tempTemplate1 = Template(read_yml_str)

            fields = '' 
            for column in schema:
                # print(column)
                columnName = str(column[0])  
                columnType = str(column[1])  
                if (columnName == 'id' ):
                    continue

                # print(columnName, columnType)
                feildType = getFieldType(columnName)

                fields += "    private " + feildType  + ' '  + columnName + ";\n"

            content = tempTemplate1.safe_substitute({
                "fields": fields, 
                "entityName": entityName, 
                "className": className, 
                "packageName":packageName,
                "date":date
            })
            
            # print(content)
            
            file = path + "/" +className + ".java"
            fo = open(file, "w")
            fo.write(content)
            fo.close()

    print('--end--')                

