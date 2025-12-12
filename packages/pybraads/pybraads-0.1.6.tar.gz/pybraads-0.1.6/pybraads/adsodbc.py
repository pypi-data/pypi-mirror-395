"""

    PyBrainUtils -- Copyright (C) 2024 Brainstorming S.A.
    class to manage ADS dat bases with odbc driver
    
"""
import re
import pyodbc

class AdsConnection:
    """ To connect on the database ADS
    """
    def __init__(self, DataDirectory : str, Uid : str, Pwd : str, MoreParam: str = None):
        """__init__
            Init and open the ADS connection

        Parameters
        ----------
        DataDirectory : str
            the URL with dictionary name of th database
        Uid : str
            database user
        Pwd : str
            database password
        """
        self._datadirectory = DataDirectory
        self._uid = Uid
        self._pwd = Pwd
        self._error = ''
        self._MoreParam = ''
        if MoreParam != None:
            self._MoreParam = MoreParam + ';'

        self._connected = False
        try:
            if self._uid == '' :
                self._connection = pyodbc.connect('DRIVER={Advantage StreamlineSQL ODBC};DataDirectory='+self._datadirectory+';TrimTrailingSpaces=TRUE;ServerType=REMOTE;'+self._MoreParam)
            else :
                self._connection = pyodbc.connect('DRIVER={Advantage StreamlineSQL ODBC};DataDirectory='+self._datadirectory+';UID='+self._uid+';PWD='+self._pwd+';TrimTrailingSpaces=TRUE;ServerType=REMOTE;'+self._MoreParam)
            self._connection.autocommit = False
        except pyodbc.Error as ex:
            self._error = str(ex) 
        else:
            self._connected = True
    
    def Close(self):
        """Close the connection
        """
        if self._connected == True:
            self._connection.close()

    def commit(self):
        """commit the modications
        """
        if self._connected == True:
            self._connection.commit()

    def rollback(self):
        """rollback the modification
        """
        if self._connected == True:
            self._connection.rollback()

    #property functions
    def _get_conn(self)->pyodbc.Connection:
        """__get_adsconn property 

        Returns
        -------
        pyodbc.Connection
            Send the ads connection of the database
        """
        return self._connection
    
    def _get_isconnected(self)->bool:
        """__get_isconnected 
            Is use to test if the datase is connected
        Returns
        -------
        bool
            true is database is connected otherwise false
        """
        return self._connected
    
    def _get_error(self)->str:
        """getError 
            to catch the error returned during the connection
        Returns
        -------
        str
            The connection error
        """
        return self._error

    # Set property() to use get_name, set_name and del_name methods
    conn = property(_get_conn)
    isconnected = property(_get_isconnected)
    error = property(_get_error)
    
class AdsQuery:
    """ To create à new query
    """
    def __init__(self, adsconn: AdsConnection):
        """__init__ 
            Init the query object

        Parameters
        ----------
        DataConnection : pyodbc.Cursor
            The ADS database connection cursor
        """
        self._error = ''
        self._adsConn = adsconn.conn
        self._data = adsconn.conn.cursor()
        self._datas = []
        self._recordindex = -1
        self._fieldsname = []
        self._sql = ''
        self._paramNames = []
        self._paramValues = []
    
    def addparam(self, aParamName : str, aParamValue : any):
        """addparam Add parameters for query SQL

        Parameters
        ----------
        aParamName : str
            The param name
        aParamValue : any
            The param value
        """
        self._paramNames.append(aParamName)
        self._paramValues.append(aParamValue)


    def open(self)->bool:
        """open
            Open the query

        Parameters
        ----------

        Returns
        -------
        bool
            true is query opened otherwise false
        """
        try:
            isopen = False
            # Close existing cursor if any and create a new one
            if self._data is not None:
                try:
                    self._data.close()
                except:
                    pass
            self._data = self._adsConn.cursor()

            sql, params = self.__binparams()
            self._data.execute(sql, params)
            self._datas = self._data.fetchall()
            self._recordindex = -1

            if len(self._fieldsname)>0:
                del self._fieldsname[:]               

            self._fieldsname = [field[0] for field in self._data.description]
            isopen = True    

        except pyodbc.Warning as wa:
            self._error = str(wa)
        except pyodbc.Error as er:
            self._error = str(er)
        except pyodbc.InterfaceError as ie:
            self._error = str(ie)
        except pyodbc.DatabaseError as dbr:
            self._error = str(dbr)
        except pyodbc.DataError as dr:
            self._error = str(er)
        except pyodbc.OperationalError as opr:
            self._error = str(opr)
        except pyodbc.IntegrityError as itge:
            self._error = str(itge)
        except pyodbc.InternalError as itne:
            self._error = str(itne)
        except pyodbc.NotSupportedError as nse:
            self._error = str(nse)
        except SyntaxError as serr:
            self._error = str(serr)
        except ValueError as verr:
            self._error = str(verr)
        finally:
            return isopen    
        
    def execute(self)->bool:
        """Execute the query

        Parameters
        ----------

        Returns
        -------
        bool
            true is query executed otherwise false
        """
        cursor = None
        try:
            isexecuted = False
            # Create a new cursor for execution
            cursor = self._adsConn.cursor()
            sql, params = self.__binparams()

            cursor.execute(sql, params)

            isexecuted = True


        except pyodbc.Warning as wa:
            self._error = str(wa)
        except pyodbc.Error as er:
            self._error = str(er)
        except pyodbc.InterfaceError as ie:
            self._error = str(ie)
        except pyodbc.DatabaseError as dbr:
            self._error = str(dbr)
        except pyodbc.DataError as dr:
            self._error = str(er)
        except pyodbc.OperationalError as opr:
            self._error = str(opr)
        except pyodbc.IntegrityError as itge:
            self._error = str(itge)
        except pyodbc.InternalError as itne:
            self._error = str(itne)
        except pyodbc.NotSupportedError as nse:
            self._error = str(nse)
        except SyntaxError as serr:
            self._error = str(serr)
        except ValueError as verr:
            self._error = str(verr)
        finally:
            # Close the cursor after execution
            if cursor is not None:
                try:
                    cursor.close()
                except:
                    pass
            return isexecuted

    def close(self):
        """Close the cursor and free resources
        """
        if self._data is not None:
            try:
                self._data.close()
            except:
                pass
            finally:
                self._data = None

    def FieldIndex(self, afieldname : str)->int:
        """FieldIndex Get the column number of th field

        Parameters
        ----------
        afieldname : str
            Field name, attention case sensitive

        Returns
        -------
        int
            Field column number
        """
        return self._fieldsname.index(afieldname)
    
    #private functions
    def __binparams(self)->str|str:
        """__binparams2 format sql query and param 
           for the execute funciton

        Parameters
        ----------
        
        Returns
        -------
        str|str
            reatrn too value the sql and the arrays of params

        Raises
        ------
        ValueError
            the error convetion
        """
        bindingParams = []
        sql = self._sql
        matches = re.findall(r'[:]\w+', sql)
        if len(matches) == 0:
            return sql, bindingParams
        
        for match in matches:
            key = match[1:]
            try:
                ind = self._paramNames.index(key)
            except :
                ind = -1

            if ind != -1:
                bindingParams.append(self._paramValues[ind])
            else:
                raise ValueError('no value found for key: ' + key)

        
        sql = re.sub(r'[:]\w+', r'?', sql)

        return sql, bindingParams    
        
    #property function
    def __get_fieldnames(self)->list:
        """__get_fieldnames return field list of the query

        Returns
        -------
        list
            all fields            
        """
        return self._fieldsname
    
    def __get_allrecords(self)->pyodbc.Cursor:
        """__get_dataset all rows of thr query

        Returns
        -------
        pyodbc.Cursor
            get all rows of the databases
        """
        return self._data.fetchall()
    
    def __get_dataset(self)->[]: #pyodbc.Row:
        """__get_dataset get the active raw

        Returns
        -------
        pyodbc.Cursor
            An active row
        """
        #return self._row
        
        return self._datas[self._recordindex]
    
    def __get__error(self)->str:
        """getError 
            to catch the error returned during the open/execute

        Returns
        -------
        str
            The error
        """
        return self._error
    
    def __set_error(self, aError : str):
        """__set_error Set the error

        Parameters
        ----------
        aError : str
            the Error
        """
        self._error = aError
    
    def __get_eof(self)->bool:
        """__get_eof To get if at end of the query

        Returns
        -------
        bool
            True end of file, False not to the end
        """
        eof = True
        try:
            nbr_row = len(self._datas)
            recordindex = self._recordindex

            if (nbr_row > 0) and (recordindex < nbr_row-1):
                self._recordindex += 1
                eof = False

            #try :
            #    self._row = self._data.fetchone()
            #    eof = (self._row == None)
            #except:
            #    eof = True
        finally:
            return eof
    
    def __get_sql(self)->str:
        return self._sql
    
    def __set_sql(self, asql : str):
        self._sql = asql
        if len(self._paramNames)>0:
            del self._paramNames[:]
        if len(self._paramValues)>0:
            del self._paramValues[:]

    # Set property() to use get_name, set_name and del_name methods
    fieldnames = property(__get_fieldnames)
    allrecords = property(__get_allrecords)
    dataset = property(__get_dataset)
    error = property(__get__error, __set_error)
    eof = property(__get_eof)
    sql = property(__get_sql,__set_sql)