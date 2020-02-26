#!/usr/bin/python
import re, os, sys, argparse

pre = []
replace_rules = []
post = []
table_header = {}
last_header = None
NAME_TEMPLATE = None
__src__ = None
__dst__ = None
__dialect__ = None


def getStructureInfoCreate(match, replace):
    global last_header

    match_iter = re.finditer(r"(?:\(|, )`(?P<name>[^`]+)`(?:[^,\)]+)", match.group(0))
    table_header[match.group(1)] = [NAME_TEMPLATE % x.group("name") for x in match_iter]

    if __dialect__ == "mssql":
        replace = (
            (
                "IF OBJECTPROPERTY(OBJECT_ID('" + NAME_TEMPLATE + "'), 'TableHasIdentity') = 1 " +
                    "SET IDENTITY_INSERT " + NAME_TEMPLATE + " OFF;" + os.linesep
            ) % (last_header, last_header) if last_header else ""
        ) + replace
    
    last_header = match.group(1)
    
    return replace


def injectStructureInfoInsertInto(match, replace):
    global last_header

    statement = match.group(0)
    match = re.match(r"^INSERT INTO\s*(?:(?P<quote>[\"` ])(?P<name>.*?)(?P=quote)).*", statement)
    if match:
        last_header = match.group("name")
        headers = table_header.get(last_header, None)
        if headers:
            statement = ("INSERT INTO " + NAME_TEMPLATE + " (%s) %s") % (last_header, ", ".join(headers), line[line.find("VALUES"):])
    
    return statement


def writeline(stream, line):
    for l in line if type(line) is list else [line]:
        stream.write(l.rstrip() + os.linesep)


def initialize(out):
    global pre, replace_rules, post, NAME_TEMPLATE

    replace_rules.append((True, r"^.*sqlite_sequence.*;[\r\n]*$", "", 0, None, True))
    replace_rules.append((True, r"^PRAGMA foreign_keys=OFF;[\r\n]*$", "", 0, None, True))
    replace_rules.append((False, " +00:00'", "'", 0, None, False))
    replace_rules.append((True, r"^INSERT INTO.*$", None, 0, injectStructureInfoInsertInto, False))

    if __dialect__ in ["mysql", "mariadb"]:
        NAME_TEMPLATE = "`%s`"
        pre.append("SET FOREIGN_KEY_CHECKS=0;")
        post.append("SET FOREIGN_KEY_CHECKS=1;")
        
        replace_rules.append((True, r"^BEGIN TRANSACTION;[\r\n]*$", "START TRANSACTION;", 0, None, True))
        replace_rules.append((True, r"^CREATE TABLE `(?P<name>[^`]*)`.*$", ("TRUNCATE TABLE " + NAME_TEMPLATE + ";") % ("{1}"), 1, getStructureInfoCreate, True))
    elif __dialect__ == "mssql":
        NAME_TEMPLATE = "[%s]"
        pre.append("EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT all';")
        post.append("EXEC sp_MSforeachtable 'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT all';")

        replace_rules.append(
            (
                True,
                r"^CREATE TABLE `(?P<name>[^`]*)`.*$",
                (
                    "IF OBJECTPROPERTY(OBJECT_ID('" + NAME_TEMPLATE + "'), 'TableHasIdentity') = 1 BEGIN " +
                        "SET IDENTITY_INSERT " + NAME_TEMPLATE + " ON; " +
                        "DBCC CHECKIDENT ('" + NAME_TEMPLATE + "', RESEED, 0); " +
                    "END" + os.linesep +
                    "DELETE " + NAME_TEMPLATE + ";"
                ) % ("{1}", "{1}", "{1}", "{1}"),
                1,
                getStructureInfoCreate,
                True
            )
        )


def post_initialize(out):
    pass


def pre_finalize(out):
    if __dialect__ == "mssql" and last_header:
        writeline(out, ("IF OBJECTPROPERTY(OBJECT_ID('" + NAME_TEMPLATE + "'), 'TableHasIdentity') = 1 SET IDENTITY_INSERT " + NAME_TEMPLATE + " OFF;") % (last_header, last_header))


def finalize(out):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='dump-converter.py', usage='python3 %(prog)s [options] INPUT > select-queries.sql', description='Linkurious Enterprise User-Data Store dump converter')
    parser.add_argument('input', action='store', metavar='INPUT', help='the Sqlite dump to convert (a *.sql file)')
    parser.add_argument('-o', '--out', dest='output', action='store', default='export-parsed.sql', required=False, help='the output file for the new import instructions (default: export-parsed.sql)')
    parser.add_argument('--dialect', dest='dialect', action='store', choices=['mysql', 'mariadb', 'mssql'], default='mysql', help='the dialect of the destination database (default: mysql)')

    args = parser.parse_args()
    __src__ = args.input
    __dst__ = args.output
    __dialect__ = args.dialect
    
    with open(__src__, 'r') as src:
        with open(__dst__, 'w') as dst:
            initialize(dst)
            writeline(dst, pre)
            post_initialize(dst)

            for line in src:
                for rule in replace_rules:
                    if rule[0]:
                        match = re.match(rule[1], line)
                        if match:
                            if rule[4]:
                                newLine = rule[4](match, rule[2])
                            else:
                                newLine = rule[2]

                            for i in range(1, rule[3] + 1):
                                newLine = newLine.replace("{%d}" % i, match.group(i))

                            if rule[5]:
                                if newLine != "":
                                    writeline(dst, newLine)
                                break
                            else:
                                line = newLine
                    else:
                        if rule[1] in line:
                            newLine = line.replace(rule[1], rule[2])
                            
                            if rule[5]:
                                if newLine != "":
                                    writeline(dst, newLine)
                                break
                            else:
                                line = newLine
                else:
                    writeline(dst, line)
            
            pre_finalize(dst)
            writeline(dst, post)
            finalize(dst)
    
    for table, cols in table_header.items():
        print(("SELECT %s from " + NAME_TEMPLATE + ";") % (", ".join(cols), table))
