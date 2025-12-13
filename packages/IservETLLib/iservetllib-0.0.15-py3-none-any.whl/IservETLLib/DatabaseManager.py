import json
from datetime import datetime
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

class DBConfig:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def __str__(self):
        return f"DatabaseConfig(host={self.host}, port={self.port}, user={self.user}, database={self.database})"
    
    def __repr__(self):
        return self.__str__()

class DBManager:
    def __init__(self, application_name, config_string, logger):
        self.db_config = self.parse_db_config(config_string)
        self.connection_string = URL.create(
            drivername="postgresql",
            username=self.db_config.user,
            password=self.db_config.password,
            host=self.db_config.host,
            database=self.db_config.database,
        )
        self.application_name = application_name
        if logger:
            self.logger = logger
        
        self.engine = None
        self.connection = None
        self.transaction = None

    
    def begin_transaction(self):
        """Начать транзакцию"""
        if not self.engine:
            self.engine = create_engine(
                self.connection_string, 
                connect_args={"application_name": self.application_name}
            )
        
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        return self.connection
    
    def commit_transaction(self):
        """Зафиксировать транзакцию"""
        if self.transaction:
            self.transaction.commit()
    
    def rollback_transaction(self):
        """Откатить транзакцию"""
        if self.transaction:
            self.transaction.rollback()
    
    def close_transaction(self):
        """Закрыть соединение"""
        if self.connection:
            self.connection.close()
        if self.engine:
            self.engine.dispose()
        self.connection = None
        self.transaction = None
        self.engine = None
    
    @contextmanager
    def transaction_scope(self):
        """Контекстный менеджер для транзакций"""
        try:
            conn = self.begin_transaction()
            yield conn
            self.commit_transaction()
        except Exception as e:
            self.rollback_transaction()
            raise e
        finally:
            self.close_transaction()
    
    def query_database(self, query, queryParams, use_transaction=True):
        """
        Выполнение запроса в рамках транзакции или отдельно
        
        Parameters
        ----------
        use_transaction : bool
            Если True, используется существующая транзакция
            Если False, создается отдельное соединение
        """
        if use_transaction and self.connection:
            try:
                result = self.connection.execute(query, queryParams)
                items = result.fetchall()
                return items
            except SQLAlchemyError as e:
                error_msg = f"Database error in transaction: {e}"
                self.logger.log(f'{error_msg} {query} {queryParams}')
                raise
        else:
            try:
                engine = create_engine(
                    self.connection_string, 
                    connect_args={"application_name": self.application_name}
                )
                
                with engine.connect() as conn:
                    result = conn.execute(query, queryParams)
                    items = result.fetchall()
                    conn.commit()
                    return items
                    
            except SQLAlchemyError as e:
                error_msg = f"Database error: {e}"
                self.logger.log(f'{error_msg} {query} {queryParams}')
                return None
            finally:
                if 'engine' in locals():
                    engine.dispose()
                    
    def parse_db_config(self, config_string):
        """Парсит строку конфигурации создает DatabaseConfig"""
        config_dict = {}
        
        # Разделяем по точкам с запятой
        pairs = config_string.split(';')
        
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)  # split только по первому двоеточию
                config_dict[key.strip()] = value.strip()
        
        # Создаем объект конфигурации
        return DBConfig(
            host=config_dict.get('host', ''),
            port=int(config_dict.get('port', 0)),
            user=config_dict.get('user', ''),
            password=config_dict.get('password', ''),
            database=config_dict.get('database', '')
        )
    # Functions
    def of_users(self, sender_id, user_id=None, c_profiles=["user", "brigade"]):
        """
        Получение пользователей of_users
        """
        query = """
            SELECT * FROM core.of_users(
                (SELECT to_jsonb(t) FROM core.sf_users(:sender_id) as t), 
                :c_profiles
            )
        """
        if user_id:
            query = query + " " + """WHERE id = :user_id"""

        queryParams = {
            "sender_id": sender_id,
            "c_profiles": json.dumps({
                "c_profiles": c_profiles
            }),
            "user_id": user_id
        }

        return self.query_database(text(query), queryParams)

    def of_levels(self, sender_id):
        """
        Получение подразделений of_levels
        """
        query = """
            SELECT * FROM core.of_levels(
                (SELECT to_jsonb(t) FROM core.sf_users(:sender_id) as t), 
                null
            );
        """
        queryParams = {
            "sender_id": sender_id
        }
        
        return self.query_database(text(query), queryParams)
    
    def of_arm_cd_user_events(self, sender_id, d_date_start, d_date_end):
        """
        Получение календаря of_arm_cd_user_events
        """
        query = """
            SELECT * FROM dbo.of_arm_cd_user_events(
                (SELECT to_jsonb(t) FROM core.sf_users(:sender_id) as t), 
                :json_params
            );
        """
        
        queryParams = {
            "sender_id": sender_id,
            "json_params": json.dumps({
                "d_date_start": d_date_start,
                "d_date_end": d_date_end
            })
        }

        return self.query_database(text(query), queryParams)

    def of_arm_add_calendar_data(self, sender_id, data):
        """
        Обновление календаря of_arm_add_calendar_data
        """
        query = """
            SELECT * FROM dbo.of_arm_add_calendar_data(
                (SELECT to_jsonb(t) FROM core.sf_users(:sender_id) as t), 
                :json_params
            );
        """

        queryParams = {
            "sender_id": sender_id,
            "json_params": json.dumps(data)
        }
        return self.query_database(text(query), queryParams)
    
    def get_user_info_by_id_db(self, USR_ID):
        """
        Получает данные о вызываемом пользователе
        """
        return self.query_database(
            text("""SELECT t.* FROM core.sf_users(:USR_ID) t limit 1"""), 
            {'USR_ID': USR_ID}
        )
    
    def create_route_db(self, params):
        """
        Создание маршрутного листа на основе сгрупированных данных (дата, исполнитель)

        Parameters
        ----------
        engine : dict
            объект для работы с БД
        params : dict
            Сгрупированные данные (исполнитель, дата маршрута, точки учёта)
            "USR_ID": ""
            "route_data": {
                "f_route_type": ""
                "c_name": ""
                "d_start_date": ""
                "d_end_date": ""
                "c_notice": ""
                "c_data_source ": ""
            }
            "registr_pts": {
                "id": ""
                "f_point_type": ""
                "n_order": ""
            }
            "user_info": ""
        -------
        Exception
            Исключение при ошибках в БД
        """
        query = text("""
                select * from dbo.of_arm_generate_route(
                    :user_info,
                    null::jsonb, 
                    :registr_pts,
                    :route_data
                )
            """)
            
        return self.query_database(
            query, 
            {
                'user_id': params['USR_ID'],
                'route_data': params['route_data'],
                'registr_pts': params['registr_pts'],
                'user_info': params['user_info']
            }
        )
    

    def assing_route_db(self, params):
        """
        Назначение бригады на маршрут

        Parameters
        ----------
        params : dict
            Сгрупированные данные (иполнитель, дата маршрута, точки учёта)
            user_info
            USR_ID
            route_data
            users
        """
        query = text("""
            select * from dbo.of_arm_changed_route(
                :user_info, 
                :users, 
                null,
                :route_data
            )
        """)
        
        self.query_database(
            query, 
            {
                'user_info': params['user_info'],
                'user_id': params['USR_ID'],
                'route_data': params['route_data'],
                'users': params['users']
            }
        )
    # End Functions


    # Tables
    def cs_event_types(self):
        """
        Получение cs_event_types
        """
        query = """
            SELECT id, c_name, c_const, b_disabled, b_default
            FROM dbo.cs_event_types;
        """
        
        return self.query_database(text(query), {})    
    
    def get_data_source_db(self):
        """
        Получает ID источника данных EIDB через db_manager
        
        Returns
        -------
        int or None
            ID источника данных
        """

        query = text("""SELECT id FROM dbo.es_data_sources WHERE c_const = 'EIDB' LIMIT 1""")
        return self.query_database(query, {})
    

    def get_brigades_db(self):
        """
        Получение всех доступных бригад
        """
        _query = text("""
            SELECT pu.* FROM core.pd_users pu
            LEFT JOIN core.pd_profiles pp on pp.id = pu.f_profile
            WHERE pp.c_name = 'brigade'
        """)

        return self.query_database(_query, {})

    def get_point_types_db(self):
        """
        Получение всех видов работ
        """
        return self.query_database(text("""SELECT * FROM dbo.cs_point_types"""), {})

    def get_subscr_ids_db(self, subscrs): 
        """
        Получение идентифкатор лицевых счетов на основе данных обрабатываемого файла

        Parameters
        ----------
        subscrs: list[dict]
            Список лицевых счетов
        """

        return self.query_database(
            text("""SELECT * FROM dbo.ss_subscrs ss WHERE c_code IN :subscrs"""), 
            {'subscrs': subscrs}
        )

    def get_registr_pts_db(self, f_data_source, numbers): 
        """
        Получение точек учёта на основе данных обрабатываемого файла

        Parameters
        ----------
        f_data_source : str
            Идентификатор EIBD
        numbers: list[dict]
            Номеры заявок
        """
        
        query = text("""
            SELECT * FROM dbo.ed_registr_pts ers
            WHERE f_data_source = :f_data_source and c_code IN :numbers
        """)
        
        return self.query_database(query, {'numbers': numbers, 'f_data_source': f_data_source})

    def get_addresses_db(self, f_data_source, addresses): 
        """
        Получение адресов из dbo.ss_address на основе данных обрабатываемого файла

        Parameters
        ----------
        addresses: list[dict]
            Список адресов
        f_data_source : str
            Идентификатор EIBD
        """
        
        query = text("""
            SELECT * FROM dbo.ss_address
            WHERE c_manual_name IN :addresses and f_data_source = :f_data_source
        """)
        
        return self.query_database(query, {'addresses': addresses, 'f_data_source': f_data_source})
    
    def get_meter_types_db(self):
        """
        Получение типов приборов учета
        """

        query = text("""
            SELECT * FROM mrkt.ss_products
        """)
        
        return self.query_database(query, {})

    def get_device_locations(self):
        query = text("""
            SELECT * FROM dbo.es_device_locations
        """)
        
        return self.query_database(query, {})
    # End Tables

    # Insert
    def create_subscrs_db(self, account, c_first_name, f_data_source):
        """
        Создание точек учёта в БД

        Parameters
        ----------
        account : dict
            Параметр вставки
        f_data_source : str
            Идентификатор EIBD
        """
        
        query = text("""
            INSERT INTO dbo.ss_subscrs (c_code, c_first_name, f_data_source)
            SELECT 
                :c_code, 
                :c_first_name,
                :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.ss_subscrs 
                WHERE c_code = :c_code
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {
                'c_code': account, 
                'c_first_name': c_first_name,
                'f_data_source': f_data_source
            }
        )
    
    def create_meter_readings_db(self, n_value_prev, d_date_prev, fn_registr_pts, fn_scale, c_notice, fn_meter, f_data_source):
        """
        Создание показаний в базе данных

        Parameters
        ----------
        n_value_prev : int
            Предыдущие показания
        d_date_prev : date
            Дата предыдущих показаний
        fn_registr_pts: str
            Идентификатор точки учета
        fn_scale : int
            шкала
        c_notice : str
            Примечание
        fn_meter : str
            Идентификатор ПУ
        f_data_source : int
            Источник данных
        """
        
        query = text("""
            INSERT INTO dbo.ed_meter_readings (n_value_prev, d_date_prev, fn_registr_pts, fn_scale, c_notice, fn_meter, f_data_source)
            SELECT 
                :n_value_prev, 
                :d_date_prev, 
                :fn_registr_pts, 
                :fn_scale, 
                :c_notice, 
                :fn_meter, 
                :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.ed_meter_readings 
                WHERE n_value_prev = :n_value_prev and d_date_prev = :d_date_prev and fn_registr_pts = :fn_registr_pts and fn_meter = :fn_meter
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {
                'n_value_prev': n_value_prev, 
                'd_date_prev': d_date_prev, 
                'fn_registr_pts': fn_registr_pts, 
                'fn_scale': fn_scale, 
                'c_notice': c_notice, 
                'fn_meter': fn_meter, 
                'f_data_source': f_data_source
            }
        )

    def create_device_locations_db(self, device_location, f_data_source):
        """
        Создание мест установки приборов учета

        Parameters
        ----------
        device_location : dict
            Параметр вставки
        """
        
        query = text("""
            INSERT INTO dbo.es_device_locations (c_name, f_data_source)
            SELECT :c_name, :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.es_device_locations 
                WHERE c_name = :c_name
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {'c_name':  device_location, 'f_data_source': f_data_source}
        )
        
    def create_device_types_db(self, f_category, device_type, f_data_source):
        """
        Создание типа прибора учета установки приборов учета

        Parameters
        ----------
        f_category : str
            Категория (ПУ)
        device_type : str
            Наименование типа
        f_data_source : str
            признак EIBD
        """
        
        query = text("""
            INSERT INTO mrkt.ss_products (f_category, c_name, c_description, f_data_source)
            SELECT :f_category, :c_name, '[EML]_routes_import', :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM mrkt.ss_products 
                WHERE c_name = :c_name
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {'f_category': f_category, 'c_name':  device_type, 'f_data_source': f_data_source}
        )

    def create_address_db(self, f_data_source, row):
        """
        Создание адресов в таблице dbo.ss_address на основе данных обрабатываемого файла

        Parameters
        ----------
        f_data_source : str
            Идентификатор EIBD\n
        row: list[dict]
            Обрабатываемый файл \n
            "Адрес": ""\n
            "Долгота": ""\n
            "Широта": ""\n
            'Населенный пункт,\n
            'Улица'\n
            'Дом'\n
            'Квартира'\n
            'Код ФИАС дома'
        -------
        Exception
            Исключение при ошибках в БД
        """
        query = text("""
            INSERT INTO dbo.ss_address (c_settlement_name, c_street_name, c_district, c_house_name, c_premise, fias_id, c_manual_name, n_longitude, n_latitude, f_data_source)
            SELECT
                :c_settlement_name, 
                :c_street_name,
                :c_district,
                :c_house_name,
                :c_premise,
                :fias_id,
                :c_manual_name,
                :n_longitude,
                :n_latitude,
                :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.ss_address 
                WHERE c_manual_name = :c_manual_name
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {
                'c_district': row['Район'],
                'c_settlement_name': row['Населенный пункт'],
                'c_street_name': row['Улица'],
                'c_house_name': row['Дом'],
                'c_premise': row['Квартира'],
                'fias_id': row['Код ФИАС дома'],
                'c_manual_name': row['Адрес'],
                'n_longitude': float(row['Долгота']),
                'n_latitude': float(row['Широта']),
                'f_data_source': f_data_source
            }
        )

        return True

    def create_registr_pts_db(self, account, f_data_source, user_info):
        """
        Создание точек учёта на основе данных обрабатываемого файла

        Parameters
        ----------
        account : dict
            Данные из таблицы
        f_data_source : str
            Идентификатор EIBD
        user_info : dict
            Данные о пользователе
        """
        query = text("""
            INSERT INTO dbo.ed_registr_pts(f_level, c_code, f_subscr, f_address, d_request_date, f_org, f_point_type, f_data_source)
            SELECT 
                :f_level,
                :c_code,
                :f_subscr,
                :f_address,
                :d_request_date,
                :f_org,
                :f_point_type,
                :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.ed_registr_pts 
                WHERE c_code = :c_code
            )
            RETURNING id
        """)
        
        self.query_database(
            query, 
            {
                'c_code': str(account['Номер заявки']),
                'f_subscr': str(account['Идентификатор лицевого счета']),
                'f_address': str(account['Идентификатор адреса']),
                'f_point_type': int(account['Идентификатор вида работ']),
                'd_request_date': datetime.strptime(account['Дата заявки'], '%d.%m.%Y').strftime('%Y-%m-%d'),
                'f_data_source': f_data_source,
                'f_level': user_info['f_level'],
                'f_org': user_info['f_org']
            }    
        )

    def create_meter_db(self, meter):
        """
        Создание ПУ в БД

        Parameters
        ----------
        meter : dict
            Данные о приборе учета

        Returns
        -------
        int or None
            ID созданной записи или None если запись не была создана
        """
        
        query = text("""
            INSERT INTO dbo.ed_meters(fn_registr_pts, fn_device_type, fn_device_location, d_install_date, d_last_calibration_date, c_serial_number, c_notice, fn_org, f_data_source)
            SELECT 
                :fn_registr_pts, 
                :fn_device_type,
                :fn_device_location,
                :d_install_date,
                :d_last_calibration_date,
                :c_serial_number,
                :c_notice,
                :fn_org,
                :f_data_source
            WHERE NOT EXISTS (
                SELECT 1 FROM dbo.ed_meters 
                WHERE c_serial_number = :c_serial_number
                AND fn_device_type = :fn_device_type
                AND fn_org = :fn_org
            )
            RETURNING id
        """)
        
        result = self.query_database(
            query, 
            {
                'fn_registr_pts': meter['fn_registr_pts'],
                'fn_device_type': meter['fn_device_type'],
                'fn_device_location': meter['fn_device_location'],
                'd_install_date': meter['d_install_date'],
                'd_last_calibration_date': meter['d_last_calibration_date'],
                'c_serial_number': meter['c_serial_number'],
                'c_notice': meter['c_notice'],
                'fn_org': meter['fn_org'],
                'f_data_source': meter['f_data_source']       
            }
        )
        
        # Если запись была создана, возвращаем ID, иначе None
        if result and len(result) > 0:
            return result[0].id
        return None
    # End Insert