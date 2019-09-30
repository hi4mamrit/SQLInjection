import psycopg2
from psycopg2 import sql

connection = psycopg2.connect(
    host='localhost',
    database='test',
    user='postgres',
    password ='Jupiter_1'
)
connection.set_session(autocommit=True)

#hardcoded query safe
def execQry():
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from person')
        result = cursor.fetchone()
    print (result[0])

#bad technique (problem with user input: chances of string interpolation)
def isAdmin(username: str) -> bool:
    with connection.cursor() as cursor:
        qryStr = """
        select isadmin 
        from person
        where name = '%s'
        """ %username

        print(qryStr)
        cursor.execute(qryStr)
        result = cursor.fetchone()
    if result is None:
        return False
    admin, = result
    return admin

#better technique but bad (problem with user input: try handling for special char '  , then what abt other special chars)
def isAdmin1(username: str) -> bool:
    username = username.replace("'","''")
    with connection.cursor() as cursor:
        qryStr = """
        select isadmin 
        from person
        where name = '%s'
        """ %username

        print(qryStr)
        cursor.execute(qryStr)
        result = cursor.fetchone()
    if result is None:
        print("result is None")
        return False
    admin, = result
    return admin

#better technique (problem with user input: ensuring that we pass a literal only)
def isAdmin2(username: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("""
        select isadmin 
        from person
        where name = %(name)s
        """, {'name':username})

        result = cursor.fetchone()
    if result is None:
        print("result is None")
        return False
    admin, = result
    return admin

# Learn sqlComposition when you need to pass tablename as a parameter , which should not be treated as literal
# Bad technique using literal string formation
def getCount1(tablename: str) -> int:
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
            select count(*) 
            from %(tabname)s
            """, {'tabname':tablename})

            result = cursor.fetchone()
        if result is None:
            print("result is None")
            rowC = 0
        rowC, = result
    except Exception as msg :
        print(str(msg))
        rowC = 0
    finally:
        return rowC

# Learn sqlComposition when you need to pass tablename as a parameter , which should not be treated as literal
# Good technique using sql api to compose sql queries
def getCount2(tablename: str) -> int:
    try:
        with connection.cursor() as cursor:
            stmt = sql.SQL("""
            select count(*) 
            from {tabname}
            """).format(
                tabname = sql.Identifier(tablename)
            )

            cursor.execute(stmt)
            result = cursor.fetchone()
        if result is None:
            print("result is None")
            rowC = 0
        rowC, = result
    except Exception as msg :
        print(str(msg))
        rowC = 0
    finally:
        return rowC

# Learn sqlComposition when you need to pass tablename as a parameter and a literal of some sort as another parameter
# Good technique using sql api to compose sql queries
def getCountWithLimit(tablename: str , limit: int) -> int:
    try:
        with connection.cursor() as cursor:
            stmt = sql.SQL("""
            select count(*) 
            from 
            (select 1 from {tabname} limit {lim} ) 
            as limit_query
            """).format(
                tabname = sql.Identifier(tablename),
                lim = sql.Literal(limit)
            )

            cursor.execute(stmt)
            result = cursor.fetchone()
        if result is None:
            print("result is None")
            rowC = 0
        rowC, = result
    except Exception as msg :
        print(str(msg))
        rowC = 0
    finally:
        return rowC



if __name__ == '__main__':
    # execQry()

    # print(isAdmin('amrit'))
    # print(isAdmin('ronn'))
    # print(isAdmin('sonu'))

    # print(isAdmin("';select true;--"))
    # print(isAdmin("';update person set isadmin ='t' where name ='ronn';select true;--"))
    # print(isAdmin('ronn'))

    # print(isAdmin1("';select true;--"))
    # print(isAdmin1("';update person set isadmin ='t' where name ='ronn';select true;--"))
    # print(isAdmin1('ronn'))

    # print(isAdmin2("';select true;--"))
    # print(isAdmin2("';update person set isadmin ='t' where name ='ronn';select true;--"))
    # print(isAdmin2('ronn'))

    # print(getCount1("person"))
    # print(getCount2("person"))
    # print(getCount2("purse"))
    print(getCountWithLimit("person", 1))
