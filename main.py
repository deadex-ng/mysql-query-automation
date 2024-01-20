"""The main entry point."""
import sshtunnel
import pymysql
from orgindiators import OrgindicatorsNCD, OrgindicatorsHIV

sql_hostname = ' '
sql_username = ' '
sql_password = ' '
sql_main_database = ' '
sql_port = 3306
ssh_host = ' '
ssh_user = ' '
ssh_password = ' '
ssh_port = 22
sql_ip = ' '

try:
    with sshtunnel.SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_password,
        remote_bind_address=(sql_ip, sql_port),
    ) as tunnel:
        try:
            conn = pymysql.connect(
                host=sql_ip,
                user=sql_username,
                passwd=sql_password,
                db=sql_main_database,
                port=tunnel.local_bind_port,
            )
            cursor_obj = conn.cursor()
            orgindicatorshiv = OrgindicatorsHIV(cursor_obj)
            orgindicatorsncd = OrgindicatorsNCD(cursor_obj)
            print("\t\t Querying Data From Database")
            print()
            orgindicatorsncd.ncd_rentention_one_year()
            print("===============================")
            orgindicatorsncd.ncd_rentention_two_years()
            print("===============================")
            orgindicatorsncd.ncd_active_in_care()
            print("===============================")
            orgindicatorsncd.ncd_patients_with_visit_in_last_three_months()
            print("===============================")
            orgindicatorsncd.ncd_mortality()
            print("===============================")
            orgindicatorsncd.ncd_active_in_care_12_months_before()
            print("===============================")
            orgindicatorsncd.ncd_active_in_care_24_months_before()

            print("===============================")
            orgindicatorshiv.mmd_summary()
            print("===============================")
            orgindicatorshiv.hiv_mortality()
            print("===============================")
            orgindicatorshiv.hiv_active_in_care()
            print("===============================")
            orgindicatorshiv.hiv_active_in_care_12_months_before()
            print("===============================")
            orgindicatorshiv.hiv_active_in_care_24_months_before()
            print("===============================")
            orgindicatorshiv.hiv_viral_load_suppression_numerator()
            print("===============================")
            orgindicatorshiv.hiv_viral_load_suppression_denominator()
            print("===============================")
            orgindicatorshiv.art_rententiona_at_12_months()
            print("===============================")
            orgindicatorshiv.art_rententiona_at_24_months()
            cursor_obj.close()
            conn.close()
        except Exception as e:
            print(e)
except sshtunnel.BaseSSHTunnelForwarderError:
    print("Make Sure you have internet connection")
