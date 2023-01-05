#!/usr/bin/python
import re, os, sys, argparse, json

pre = []
replace_rules = []
post = []
#
# table_header specs: map
# TableName: (
#   [list of column names],
#   [list of positions to skip based on the intersaction with __out_schema__ (descending order)]
# )
#
table_header = {}
in_table_header = {}
last_header = None
NAME_TEMPLATE = None
__src__ = None
__dst__ = None
__dialect__ = None
__out_schema__ = None


def getStructureInfoCreate(match, replace):
    global last_header

    match_iter = re.finditer(r"(?:\( *|, *)`(?P<name>[^`]+)`(?:[^,\)]+)", match.group(0))
    in_table_header[match.group(1)] = [x.group("name") for x in match_iter]

    if __dialect__ == "mssql":
        # For the last processed table, reset the standard behaviour of autoincrement
        replace = (
            (
                "IF OBJECTPROPERTY(OBJECT_ID('" + NAME_TEMPLATE + "'), 'TableHasIdentity') = 1 " +
                    "SET IDENTITY_INSERT " + NAME_TEMPLATE + " OFF;" + os.linesep
            ) % (last_header, last_header) if last_header else ""
        ) + replace
    
    last_header = match.group(1)
    
    return replace


def extractListOfValues(inputStr):
    values = []
    if not inputStr:
        return values
    
    value_buffer = ""
    in_string = False
    escape_quote = False
    parentheses_counter = 0
    for c in inputStr:
        if escape_quote and c != "'":
            in_string = False
            escape_quote = False

        if in_string:
            if c == "'":
                escape_quote = not escape_quote
            
            value_buffer += c
        else:
            if c == "'":
                if __dialect__ == "mssql":
                    value_buffer += "N'"
                else:
                    value_buffer += "'"
                
                in_string = True
            elif c == "(":
                parentheses_counter += 1
                value_buffer += c
            elif c == ")":
                parentheses_counter -= 1
                value_buffer += c
            elif parentheses_counter > 0 and c == ",":
                value_buffer += c
            elif c == ",":
                values.append(value_buffer.strip())
                value_buffer = ""
                
                assert not in_string, "Error while parsing values list: Unexpected quote. `%s`" % (inputStr)
                assert not escape_quote, "Error while parsing values list: Unexpected escape quote. `%s`" % (inputStr)
                continue
            else:
                value_buffer += c
    
    assert value_buffer != "", "Error while parsing values list: Missing value. `%s`" % (inputStr)
    values.append(value_buffer.strip())
    
    return values


def injectStructureInfoInsertInto(match, replace):
    global last_header

    statement = match.group(0)
    match = re.match(r"^\s*INSERT\s+INTO\s*(?:(?P<quote>[\"` ])(?P<name>.*?)(?P=quote)).*VALUES\s*\((?P<values>.*)\).*$", statement)
    assert match, "Error while parsing an Insert Statement: `%s`" % (statement)
    
    last_header = match.group("name")
    headers = table_header.get(last_header, None)
    if not headers:
        in_headers = in_table_header.get(last_header, None)
        entries_to_skip = []

        if __out_schema__:
            out_headers = __out_schema__.get(last_header, None)
            assert out_headers, "Error while creating an Insert Statement, mismatch between input data and schema: `%s`" % (statement)
            out_headers = set(out_headers)
            for i in range(len(in_headers) - 1, -1, -1):
                if not in_headers[i] in out_headers:
                    del in_headers[i]
                    entries_to_skip.append(i)

        headers = ([NAME_TEMPLATE % (x) for x in in_headers], entries_to_skip if len(entries_to_skip) > 0 else None)
        table_header[last_header] = headers

    assert headers, "Error while creating an Insert Statement, no table definition found for `%s`" % (last_header)

    values = extractListOfValues(match.group("values"))
    
    if headers[1]:
        for pos in headers[1]:
            del values[pos]

    assert len(headers[0]) == len(values), "Error while creating an Insert Statement, mismatch between number of headers and number of values for table `%s`: %s" % (last_header, statement)
    statement = ("INSERT INTO " + NAME_TEMPLATE + "(%s) VALUES(%s);\n") % (last_header, ",".join(headers[0]), ",".join(values))
    
    return statement


def writeline(stream, line):
    for l in line if type(line) is list else [line]:
        stream.write(l.rstrip() + os.linesep)


def initialize(out):
    global pre, replace_rules, post, NAME_TEMPLATE

    # Delete any action on the internal sqlite_sequence table
    replace_rules.append((True, r"^.*sqlite_sequence.*;[\r\n]*$", "", 0, None, True))
    # Fix the datetime values
    replace_rules.append((False, " +00:00'", "'", 0, None, False))
    # Rewrite compatible insert rules
    replace_rules.append((True, r"^INSERT INTO.*$", None, 0, injectStructureInfoInsertInto, True))

    if __dialect__ in ["mysql", "mariadb"]:
        NAME_TEMPLATE = "`%s`"
        pre.append("START TRANSACTION;")
        # Disable/enable the constraint checks
        pre.append("SET FOREIGN_KEY_CHECKS=0;")
        post.append("SET FOREIGN_KEY_CHECKS=1;")
        
        # Extract the table structure and replace the CREATE statement with a TRUNCATE
        replace_rules.append((True, r"^CREATE TABLE `(?P<name>[^`]*)`.*$", ("TRUNCATE TABLE " + NAME_TEMPLATE + ";") % ("{1}"), 1, getStructureInfoCreate, True))
    elif __dialect__ == "mssql":
        NAME_TEMPLATE = "[%s]"
        pre.append("BEGIN TRANSACTION;")
        pre.append("declare @query varchar(max);");
        # Disable/enable the constraint checks for every table
        pre.append("select @query = coalesce(@query + ' ' + 'ALTER TABLE [' + name + '] NOCHECK CONSTRAINT all;', 'ALTER TABLE [' + name + '] NOCHECK CONSTRAINT all;') from sys.tables; exec(@query);")
        post.append("select @query = coalesce(@query + ' ' + 'ALTER TABLE [' + name + '] WITH CHECK CHECK CONSTRAINT all;', 'ALTER TABLE [' + name + '] WITH CHECK CHECK CONSTRAINT all;') from sys.tables; exec(@query);")

        # Extract the table structure and replace the CREATE statement with a DELETE
        # it also allows to manually set values for columns with autoincrement
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


# To write custom output after writing the `pre` variable
def post_initialize(out):
    pass


# To write custom output before writing the `post` variable
def pre_finalize(out):
    if __dialect__ == "mssql" and last_header:
        # For the last processed table, reset the standard behaviour of autoincrement
        writeline(out, ("IF OBJECTPROPERTY(OBJECT_ID('" + NAME_TEMPLATE + "'), 'TableHasIdentity') = 1 SET IDENTITY_INSERT " + NAME_TEMPLATE + " OFF;") % (last_header, last_header))


# To write custom output after writing the `post` variable
def finalize(out):
    # Always COMMIT the transaction at the end of the file.
    # In case of errors of the script, either the transaction is auto-rollbacked
    # or it is safe to execute again the script to delete all data and reimport them
    writeline(out, "COMMIT;")

    # Line nedded at the end of the script to ensure all MSSQL tools
    # will properly interpret the file as a full script to be executed
    if __dialect__ == "mssql":
        writeline(out, "go")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='dump-converter.py', usage='python3 %(prog)s [options] INPUT > select-queries.sql', description='Linkurious Enterprise User-Data Store dump converter')
    parser.add_argument('input', action='store', metavar='INPUT', help='the SQLite dump to convert (a *.sql file)')
    parser.add_argument('-o', '--out', dest='output', action='store', default='export-parsed.sql', required=False, help='the output file for the new import instructions (default: export-parsed.sql)')
    parser.add_argument('-d', '--dump-schema', dest='dump_schema', action='store', default=None, required=False, help='the output file in json format of the schema used to create the output, compatible with the schema option (default: not exported)')
    parser.add_argument('--dialect', dest='dialect', action='store', choices=['mysql', 'mariadb', 'mssql'], default='mysql', help='the dialect of the destination database (default: mysql)')
    parser.add_argument('--schema', dest='schema', action='store', default=None, required=False, help='the file containing the destination schema structure, it is a *.json file containing the mapping as { "table name": ["list of columns"] } (default: everything is created according to the input file)')

    args = parser.parse_args()
    __src__ = args.input
    __dst__ = args.output
    __dialect__ = args.dialect
    
    if args.schema:
        filename, ext = os.path.splitext(args.schema)
        assert ext in [".json"], "Unsupported schema format"
        
        if ext == ".json":
            with open(args.schema, "r") as schema:
                __out_schema__ = json.loads(schema.read())

    with open(__src__, 'r') as src:
        with open(__dst__, 'w') as dst:
            initialize(dst)
            writeline(dst, pre)
            post_initialize(dst)

            # multiline_create_buffer = ""
            for line in src:
                #
                # Backup code:
                # No more need to collapse CREATE statements in a single line
                #
                # # Convert any multiline CREATE statement into a single line statement
                # stripped_line = line.strip() # main objective to remove new line chars
                # if stripped_line.startswith("CREATE TABLE") and not stripped_line.endswith(");"):
                #     assert multiline_create_buffer == "", "Error while parsing a Create Statement, unexpected create statement"
                #     multiline_create_buffer = stripped_line
                #     continue
                # elif multiline_create_buffer:
                #     multiline_create_buffer += " " + stripped_line
                #     if stripped_line.endswith(");"):
                #         line = multiline_create_buffer
                #         multiline_create_buffer = ""
                #     else:
                #         continue

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
            
            pre_finalize(dst)
            writeline(dst, post)
            finalize(dst)
    
    if args.dump_schema:
        filename, ext = os.path.splitext(args.dump_schema)
        if ext != ".json":
            args.dump_schema += ".json"
        
        try:
            with open(args.dump_schema, "w") as outfile:
                json.dump(__out_schema__ if __out_schema__ else in_table_header, outfile, indent = 4, sort_keys = True)
        except:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            sys.stderr.write("Error while exporting the input schema: %s" % str(ex_value))
            sys.stderr.write(os.linesep)

    for table, (cols, ids) in table_header.items():
        print(("SELECT %s from " + NAME_TEMPLATE + ";") % (", ".join(cols), table))
