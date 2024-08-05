"""The main entry point."""
import sshtunnel
import pymysql
import os
from dotenv import load_dotenv, dotenv_values
from reports.orgindiators import OrgindicatorsNCD, OrgindicatorsHIV
from reports.advancedncd import (
    CHF,
    Epilepsy,
    DiabetesType2,
    DiabetesType1,
    CKD,
    Mentalhealth,
    COPD,
    Asthma,
    Hypertension,
)

ssh_host = "10.100.11.43"
try:
    with sshtunnel.SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=username,
        ssh_password=password,
        remote_bind_address=(sql_ip, sql_port),
    ) as tunnel:
        try:
            conn = pymysql.connect(
                host=sql_ip,
                user=sql_username,
                passwd=sql_password,
                db=sql_database,
                port=tunnel.local_bind_port,
            )
            cursor_obj = conn.cursor()
            advancedchf = CHF(cursor_obj)
            advancedepilepsy = Epilepsy(cursor_obj)
            advanceddiabetes2 = DiabetesType2(cursor_obj)
            advanceddiabetes1 = DiabetesType1(cursor_obj)
            advancedckd = CKD(cursor_obj)
            advancedmentalhealth = Mentalhealth(cursor_obj)
            advancedcopd = COPD(cursor_obj)
            advancedasthma = Asthma(cursor_obj)
            advancedhypertension = Hypertension(cursor_obj)
            orgindicatorshiv = OrgindicatorsHIV(cursor_obj)
            orgindicatorsncd = OrgindicatorsNCD(cursor_obj)
            if ssh_host == "10.100.11.43":
                server = "Upper Neno"
            elif ssh_host == "10.160.22.15":
                server = "Lower Neno"
            header = "\t\t Querying Data From {} Database".format(server)
            print(header)
            print()
            print("***************", "Pulling CHF Data", "***************")
            print()
            advancedchf.enrolled_and_active_in_care()
            print("===============================")
            advancedchf.newly_registered()
            print("===============================")
            advancedchf.defaulted()
            print("===============================")
            advancedchf.died()
            print("===============================")
            advancedchf.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedchf.patients_with_diagnosis_rheumatic_heart_disease()
            print("===============================")
            advancedchf.patients_with_diagnosis_congenital_heart_disease()
            print("===============================")
            advancedchf.patients_with_nyha_classification_recorded_in_last_visit()
            print("===============================")
            advancedchf.patients_recordd_in_nyha_class_one()
            print("===============================")
            advancedchf.patients_recorded_in_nyha_class_two()
            print("===============================")
            advancedchf.patients_recorded_in_nyha_class_three()
            print("===============================")
            advancedchf.patients_recorded_in_nyha_class_four()
            print("===============================")
            advancedchf.patients_with_a_visit_in_last_month_with_hospitilization_in_last_month()

            print()
            print("***************", "Pulling Epilepsy Data", "***************")
            print()
            print("===============================")
            advancedepilepsy.enrolled_and_active_in_care()
            print("===============================")
            advancedepilepsy.newly_registered()
            print("===============================")
            advancedepilepsy.defaulted()
            print("===============================")
            advancedepilepsy.died()
            print("===============================")
            advancedepilepsy.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedepilepsy.patients_with_visit_last_month_with_no_seizures()

            print()
            print("***************", "Pulling Diabetes Type 2 Data", "***************")
            print()
            print("===============================")
            advanceddiabetes2.enrolled_and_active_in_care()
            print("===============================")
            advanceddiabetes2.newly_registered()
            print("===============================")
            advanceddiabetes2.defaulted()
            print("===============================")
            advanceddiabetes2.died()
            print("===============================")
            advanceddiabetes2.patients_with_visit_in_the_last_month()
            print("===============================")
            advanceddiabetes2.patients_with_visit_in_last_month_with_FBS_less_than_150()
            print("===============================")
            advanceddiabetes2.currently_enrolled_patients_that_have_ever_experienced_complication()
            print("===============================")
            advanceddiabetes2.patients_on_insulin()

            print()
            print("***************", "Pulling Diabetes Type 1 Data", "***************")
            print()
            print("===============================")
            advanceddiabetes1.enrolled_and_active_in_care()
            print("===============================")
            advanceddiabetes1.newly_registered()
            print("===============================")
            advanceddiabetes1.defaulted()
            print("===============================")
            advanceddiabetes1.died()
            print("===============================")
            advanceddiabetes1.patients_with_visit_in_the_last_month()
            print("===============================")
            advanceddiabetes1.patients_with_visit_in_last_month_with_FBS_less_than_150()

            print()
            print(
                "***************",
                "Pulling Chronic Kidney Disease Data",
                "***************",
            )
            print()
            print("===============================")
            advancedckd.enrolled_and_active_in_care()
            print("===============================")
            advancedckd.newly_registered()
            print("===============================")
            advancedckd.defaulted()
            print("===============================")
            advancedckd.died()
            print("===============================")
            advancedckd.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedckd.patients_with_visit_in_last_month_creatinine_level_recorded()
            print("===============================")
            advancedckd.patients_with_visit_in_last_month_with_urinalysis_recorded()

            print()
            print("***************", "Pulling Mental Health Data", "***************")
            print()
            print("===============================")
            advancedmentalhealth.enrolled_and_active_in_care()
            print("===============================")
            advancedmentalhealth.newly_registered()
            print("===============================")
            advancedmentalhealth.defaulted()
            print("===============================")
            advancedmentalhealth.died()
            print("===============================")
            advancedmentalhealth.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedmentalhealth.patients_with_visit_in_last_month_who_have_been_hospitalized()
            print("===============================")
            advancedmentalhealth.patients_on_medicine_who_reported_side_effects_from_medication()
            print("===============================")
            advancedmentalhealth.patients_in_care_that_were_reported_stable_in_last_visit()
            print("===============================")
            advancedmentalhealth.patients_in_care_that_were_reported_stable_in_last_visit()

            print()
            print("***************", "Pulling COPD Data", "***************")
            print()
            print("===============================")
            advancedcopd.enrolled_and_active_in_care()
            print("===============================")
            advancedcopd.newly_registered()
            print("===============================")
            advancedcopd.defaulted()
            print("===============================")
            advancedcopd.died()

            print()
            print("***************", "Pulling Asthma Data", "***************")
            print()
            print("===============================")
            advancedasthma.enrolled_and_active_in_care()
            print("===============================")
            advancedasthma.newly_registered()
            print("===============================")
            advancedasthma.defaulted()
            print("===============================")
            advancedasthma.died()
            print("===============================")
            advancedasthma.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedasthma.patients_with_disease_severity_recorded_at_most_recent_visit()
            print("===============================")
            advancedasthma.patients_with_intermittent_asthma_recorded_at_recent_visit()
            print("===============================")
            advancedasthma.patients_with_mild_persitent_asthma_recorded_at_recent_visit()
            print("===============================")
            advancedasthma.patients_with_moderate_asthma_recorded_at_recent_visit()
            print("===============================")
            advancedasthma.patients_with_severe_persitent_asthma_recorded_at_recent_visit()
            print("===============================")
            advancedasthma.patients_with_uncontrolled_asthma_recorded_at_recent_visit()

            print()
            print("***************", "Pulling Hypertension Data", "***************")
            print()
            print("===============================")
            advancedhypertension.enrolled_and_active_in_care()
            print("===============================")
            advancedhypertension.newly_registered()
            print("===============================")
            advancedhypertension.defaulted()
            print("===============================")
            advancedhypertension.died()
            print("===============================")
            advancedhypertension.patients_with_visit_in_the_last_month()
            print("===============================")
            advancedhypertension.currently_enrolled_patients_that_have_ever_experienced_complication()
            print("===============================")
            advancedhypertension.patients_with_visit_in_last_3_months_BPbelow_140over90()





            # print("===============================")
            # orgindicatorsncd.ncd_rentention_two_years()
            # print("===============================")
            # orgindicatorsncd.ncd_active_in_care()
            # print("===============================")
            # orgindicatorsncd.ncd_patients_with_visit_in_last_three_months()
            # print("===============================")
            # orgindicatorsncd.ncd_mortality()
            # print("===============================")
            # orgindicatorsncd.ncd_active_in_care_12_months_before()
            # print("===============================")
            # orgindicatorsncd.ncd_active_in_care_24_months_before()

            # print("===============================")
            # orgindicatorshiv.mmd_summary()
            # print("===============================")
            # orgindicatorshiv.hiv_mortality()
            # print("===============================")
            # orgindicatorshiv.hiv_active_in_care()
            # print("===============================")
            # orgindicatorshiv.hiv_active_in_care_12_months_before()
            # print("===============================")
            # orgindicatorshiv.hiv_active_in_care_24_months_before()
            # print("===============================")
            # orgindicatorshiv.hiv_viral_load_suppression_numerator()
            # print("===============================")
            # orgindicatorshiv.hiv_viral_load_suppression_denominator()
            # print("===============================")
            # orgindicatorshiv.art_rententiona_at_12_months()
            # print("===============================")
            # orgindicatorshiv.art_rententiona_at_24_months()
            cursor_obj.close()
            conn.close()
        except Exception as e:
            print(e)
except sshtunnel.BaseSSHTunnelForwarderError:
    print("Make Sure you have internet connection")
