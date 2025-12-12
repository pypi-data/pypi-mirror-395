"""Niko Home Control 2 configuration file reader.

This module provides utilities for reading and parsing Niko Home Control 2
configuration files (.nhc2 format) which contain SQLite databases.
"""

from zipfile import ZipFile
import sqlite3

class NHC2FileReader:
    """Reader for Niko Home Control 2 configuration files.
    
    Extracts and reads device and location information from .nhc2 configuration
    files exported from the Niko Home Control app.
    
    Attributes:
        nhc2_file_path (str): Path to the .nhc2 configuration file.
        db_name (str): Path to the extracted SQLite database file.
    """
    
    def __init__(self, nhc2_file_path=None):
        """Initialize NHC2FileReader.
        
        Args:
            nhc2_file_path (str, optional): Path to .nhc2 configuration file.
            
        Raises:
            ValueError: If nhc2_file_path is not provided.
            FileNotFoundError: If the configuration file does not exist.
        """
        if not nhc2_file_path:
            raise ValueError("No config file path provided!")
        
        import os
        if not os.path.exists(nhc2_file_path):
            raise FileNotFoundError(f"Configuration file not found: {nhc2_file_path}")
        
        self.nhc2_file_path = nhc2_file_path

        self._unzip_file()


    def _unzip_file(self):
        """Extract SQLite database from .nhc2 file.
        
        Unzips the .nhc2 archive and extracts the SQLite database file.
        Sets the db_name attribute to the path of the extracted database.
        
        Raises:
            ValueError: If the .nhc2 file does not contain a SQLite database.
            IOError: If extraction fails due to permissions or disk space.
        """
        db_name = self.nhc2_file_path.rstrip(".nhc2")
        db_name = f"{db_name}.sqlite"

        try:
            # loading the temp.zip and creating a zip object
            with ZipFile(self.nhc2_file_path, 'r') as zipdata:
                zipinfos = zipdata.infolist()
                
                sqlite_found = False
                for zipinfo in zipinfos:
                    if '.sqlite' in zipinfo.filename:
                        zipinfo.filename = db_name
                        zipdata.extract(zipinfo)
                        sqlite_found = True
                        break
                
                if not sqlite_found:
                    raise ValueError(f"No SQLite database found in {self.nhc2_file_path}")
        except IOError as e:
            raise IOError(f"Failed to extract database from {self.nhc2_file_path}: {e}")

        self.db_name = db_name


    def get_locations(self):
        """Get all locations from the configuration file.
        
        Queries the SQLite database for all configured locations/rooms.
        
        Returns:
            list: List of location dictionaries, each containing:
                - location_uuid (str): Unique identifier for the location.
                - location_name (str): Human-readable name of the location.
                
        Raises:
            sqlite3.DatabaseError: If the database is corrupted or invalid.
            sqlite3.OperationalError: If the Location table does not exist.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Query devices
            cursor.execute("""
                SELECT CreationId as location_uuid, Name as location_name
                FROM Location
                """)
            rows = cursor.fetchall()

            # Build a dict of devices
            locations = [
                {"location_uuid": row[0], "location_name": row[1]}
                for row in rows
            ]

            return locations
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError(f"Database query failed - table may not exist: {e}")
        except sqlite3.DatabaseError as e:
            raise sqlite3.DatabaseError(f"Database error: {e}")
        finally:
            if conn:
                conn.close()


    def get_devices(self, device_type=None, location_uuid=None, location_name=None):
        """Get devices from the configuration file.
        
        Queries the SQLite database for devices, optionally filtered by
        device type or location.
        
        Args:
            device_type (str, optional): Filter by device type code. Defaults to None.
            location_uuid (str, optional): Filter by location UUID. Defaults to None.
            location_name (str, optional): Filter by location name. Defaults to None.
            
        Returns:
            list: List of device dictionaries, each containing:
                - device_uuid (str): Unique identifier for the device.
                - device_name (str): Human-readable name of the device.
                - device_type (str): Device type code.
                - location_uuid (str): UUID of the location containing the device.
                - location_name (str): Name of the location containing the device.
                
        Raises:
            sqlite3.DatabaseError: If the database is corrupted or invalid.
            sqlite3.OperationalError: If required tables do not exist.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        query = """
            SELECT 
                action.FifthplayId as device_uuid, 
                action.Name as device_name, 
                actor.ActorTypeCode as device_type,
                location.CreationId as location_uuid,
                location.Name as location_name
            FROM Action action
            LEFT JOIN Actor actor
            ON action.Name = actor.Name
            LEFT JOIN Location location
            ON action.LocationId = location.Id
            WHERE actor.ActorTypeCode IS NOT NULL
        """

        # add device type filter if provided
        if device_type:
            query += f"AND actor.ActorTypeCode = '{device_type}'"

        # add location filter if provided
        if location_name:
            query += f"AND location.Name = '{location_name}'"

        elif location_uuid:
            query += f"AND location.CreationId = '{location_uuid}'"

        # Query devices
        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Build a dict of devices
            devices = [
                {"device_uuid": row[0], "device_name": row[1], "device_type": row[2], "location_uuid": row[3], "location_name": row[4]}
                for row in rows
            ]

            return devices
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError(f"Database query failed - tables may not exist: {e}")
        except sqlite3.DatabaseError as e:
            raise sqlite3.DatabaseError(f"Database error: {e}")
        finally:
            if conn:
                conn.close()


    def get_device_types(self):
        """Get all unique device types from the configuration file.
        
        Queries the SQLite database for all distinct device type codes.
        
        Returns:
            list: List of device type code strings (e.g., ['Lamp', 'DimmableLamp']).
            
        Raises:
            sqlite3.DatabaseError: If the database is corrupted or invalid.
            sqlite3.OperationalError: If required tables do not exist.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            # Query devices
            cursor.execute("""
                SELECT DISTINCT actor.ActorTypeCode as device_type
                FROM Action action
                LEFT JOIN Actor actor
                ON action.Name = actor.Name
                WHERE actor.ActorTypeCode IS NOT NULL
            """)
            rows = cursor.fetchall()

            device_types = [row[0] for row in rows]

            return device_types
        except sqlite3.OperationalError as e:
            raise sqlite3.OperationalError(f"Database query failed - tables may not exist: {e}")
        except sqlite3.DatabaseError as e:
            raise sqlite3.DatabaseError(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
