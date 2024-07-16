"""Organisation Indicators Quries."""

from constants import FACILITIES


class OrgindicatorsNCD:
    def __init__(self, cursor_obj):
        self.cursor_obj = cursor_obj

    def ncd_rentention_one_year(self) -> None:
        end_date = '"2023-03-31"'
        end_reporting_date = '"2023-03-31"'
        query = """
        /* 2.Retention In Care For Ncds At 12 And 24 Months */
        /* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @endReportindDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location = {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program","Chronic care program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1
            and state IN ("On treatment","In advanced care")
            and opi.patient_id in (
            SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP","ASTHMA_FOLLOWUP","EPILEPSY_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
        "DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
            and opi.patient_id in 
            (
        SELECT
            opi.patient_id as pat
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program","Chronic care program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, end_reporting_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            # print(response)
            print(
                "Retention In Care For Ncds At 12 months [ " + facility + " ]:",
                len(response),
            )

    def ncd_rentention_two_years(self) -> None:
        end_date = '"2022-03-31"'
        end_reporting_date = '"2022-03-31"'
        query = """
        /* 2.Retention In Care For Ncds At 24 Months */
        /* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @endReportindDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location = {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program","Chronic care program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1
            and state IN ("On treatment","In advanced care")
            and opi.patient_id in (
            SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP","ASTHMA_FOLLOWUP","EPILEPSY_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
        "DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
            and opi.patient_id in 
            (
        SELECT
            opi.patient_id as pat
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program","Chronic care program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, end_reporting_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Retention In Care For Ncds At 24 months [ " + facility + " ]:",
                len(response),
            )

    def ncd_active_in_care(self) -> None:
        end_date = '"2024-03-31"'

        query = """
        /* Denominaotr - # of NCD patients currently in care */

        USE openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location = {};
        ---
        select count(*)
        from
        (
        select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
        ops.location
        from  mw_patient mwp  
        join omrs_patient_identifier opi
        on mwp.patient_id = opi.patient_id
        JOIN
        (SELECT
        index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Chronic Care Program","Mental Health Care Program")
					and start_date <= @endDate
					and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP","ASTHMA_FOLLOWUP","EPILEPSY_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
        "DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of NCD patients currently in care [ " + facility + " ]:",
                response[0][0],
            )

    def ncd_patients_with_visit_in_last_three_months(self) -> None:
        start_date = '"2024-01-01"'
        end_date = '"2024-03-31"'

        query = """
        /* Numerator - Number of NCD patients with a visit in the last three months */
        SET @startDate = {};
        ---
        SET @endDate = {};
        ---
        select location, count(*)
        from (
        SELECT distinct(patient_id), location FROM mw_ncd_visits
        where visit_date >= @startDate and visit_date <= @endDate
        ) x
        group by location
        """.format(
            start_date, end_date
        )
        qry_lst = query.split("---")
        for qry in qry_lst:
            self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
        for data_point in response:
            print(
                "Number of NCD patients with a visit in the last three months [ "
                + data_point[0]
                + " ]:",
                data_point[1],
            )

    def ncd_mortality(self) -> None:
        start_date = '"2024-01-01"'
        end_date = '"2024-03-31"'
        query = """
        /* NCD Mortality */
        /* Numerator - Patient died */
        use openmrs_warehouse;
        ---
        SET @startDate = {};
        ---
        SET @endDate = {};
        ---

        select location, count(*)
        from
        (
        select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
        ops.location
        from  mw_patient mwp  
        join omrs_patient_identifier opi
        on mwp.patient_id = opi.patient_id
        JOIN
        (SELECT
        index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Chronic Care Program","Mental Health Care Program")
					and start_date <= @endDate
                 
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("patient died")
            ) x
            where start_date between @startDate and @endDate
            group by location;
        """.format(
            start_date, end_date
        )
        qry_lst = query.split("---")
        for qry in qry_lst:
            self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
        for data_point in response:
            print(
                "Number of NCD patients who died in last quarter [ "
                + data_point[0]
                + " ]:",
                data_point[1],
            )

    def ncd_active_in_care_12_months_before(self) -> None:
        end_date = '"2023-03-31"'

        query = """
        /* Denominaotr - # of NCD patients currently in care */

        USE openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location = {};
        ---
        select count(*)
        from
        (
        select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
        ops.location
        from  mw_patient mwp  
        join omrs_patient_identifier opi
        on mwp.patient_id = opi.patient_id
        JOIN
        (SELECT
        index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Chronic Care Program","Mental Health Care Program")
					and start_date <= @endDate
					and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP","ASTHMA_FOLLOWUP","EPILEPSY_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
        "DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of NCD patients active in care 12 months before [ "
                + facility
                + " ]:",
                response[0][0],
            )

    def ncd_active_in_care_24_months_before(self) -> None:
        end_date = '"2022-03-31"'

        query = """
        /* Denominaotr - # of NCD patients currently in care */

        USE openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location = {};
        ---
        select count(*)
        from
        (
        select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
        ops.location
        from  mw_patient mwp  
        join omrs_patient_identifier opi
        on mwp.patient_id = opi.patient_id
        JOIN
        (SELECT
        index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Chronic Care Program","Mental Health Care Program")
					and start_date <= @endDate
					and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP","ASTHMA_FOLLOWUP","EPILEPSY_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
        "DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of NCD patients active in care 24 months before [ "
                + facility
                + " ]:",
                response[0][0],
            )


class OrgindicatorsHIV:
    def __init__(self, cursor_obj):
        self.cursor_obj = cursor_obj

    def mmd_summary(self) -> None:
        end_date = '"2024-03-31"'
        query = """
        /* Denominaotr - # of NCD patients currently in care */

        USE openmrs_warehouse;
        ---
        SET @birthDateDivider = 30;
        ---
        SET @endDate = {};
        ---
        SET @location = {};
        ---
        /* Pepfar Cut-off = 30, MoH cut-off = 60 */
        SET @defaultCutOff = 60;
        ---
        call create_age_groups();
        ---
        call create_last_art_outcome_at_facility(@endDate,@location);
        ---
        select sum(less_than_three_months), sum(three_to_five_months), sum(six_months_plus)
        from
        (
        select sort_value,x.age_group, x.gender, 
        CASE WHEN less_than_three_months is null then 0 else less_than_three_months end as less_than_three_months,
        CASE WHEN three_to_five_months is null then 0 else three_to_five_months end as three_to_five_months,
        CASE WHEN six_months_plus is null then 0 else six_months_plus end as six_months_plus

        from
        age_groups as x
        LEFT OUTER JOIN
        (
        SELECT CASE
	    WHEN age <= 11 and gender = "M" THEN "< 1 year"
	    WHEN age <= 11 and gender = "F" THEN "< 1 year"
	    WHEN age >=12 and age <= 59 and gender = "M" THEN "1-4 years"
	    WHEN age >=12 and age <= 59 and gender = "F" THEN "1-4 years"
	    WHEN age >=60 and age <= 119 and gender = "M" THEN "5-9 years"
	    WHEN age >=60 and age <= 119 and gender = "F" THEN "5-9 years"
	    WHEN age >=120 and age <= 179 and gender = "M" THEN "10-14 years"
	    WHEN age >=120 and age <= 179 and gender = "F" THEN "10-14 years"
	    WHEN age >=180 and age <= 239 and gender = "M" THEN "15-19 years"
	    WHEN age >=180 and age <= 239 and gender = "F" THEN "15-19 years"
	    WHEN age >=240 and age <= 299 and gender = "M" THEN "20-24 years"
	    WHEN age >=240 and age <= 299 and gender = "F" THEN "20-24 years"
	    WHEN age >=300 and age <= 359 and gender = "M" THEN "25-29 years"
	    WHEN age >=300 and age <= 359 and gender = "F" THEN "25-29 years"
	    WHEN age >=360 and age <= 419 and gender = "M" THEN "30-34 years"
	    WHEN age >=360 and age <= 419 and gender = "F" THEN "30-34 years"
	    WHEN age >=420 and age <= 479 and gender = "M" THEN "35-39 years"
	    WHEN age >=420 and age <= 479 and gender = "F" THEN "35-39 years"
	    WHEN age >=480 and age <= 539 and gender = "M" THEN "40-44 years"
	    WHEN age >=480 and age <= 539 and gender = "F" THEN "40-44 years"
	    WHEN age >=540 and age <= 599 and gender = "M" THEN "45-49 years"
	    WHEN age >=540 and age <= 599 and gender = "F" THEN "45-49 years"
	    WHEN age >=600 and age <= 659 and gender = "M" THEN "50-54 years"
	    WHEN age >=600 and age <= 659 and gender = "F" THEN "50-54 years"
	    WHEN age >=660 and age <= 719 and gender = "M" THEN "55-59 years"
	    WHEN age >=660 and age <= 719 and gender = "F" THEN "55-59 years"
	    WHEN age >=720 and age <= 779 and gender = "M" THEN "60-64 years"
	    WHEN age >=720 and age <= 779 and gender = "F" THEN "60-64 years"
	    WHEN age >=780 and age <= 839 and gender = "M" THEN "65-69 years"
	    WHEN age >=780 and age <= 839 and gender = "F" THEN "65-69 years"
	    WHEN age >=840 and age <= 899 and gender = "M" THEN "70-74 years"
	    WHEN age >=840 and age <= 899 and gender = "F" THEN "70-74 years"
	    WHEN age >=900 and age <= 959 and gender = "M" THEN "75-79 years"
	    WHEN age >=900 and age <= 959 and gender = "F" THEN "75-79 years"
	    WHEN age >=960 and age <= 1019 and gender = "M" THEN "80-84 years"
	    WHEN age >=960 and age <= 1019 and gender = "F" THEN "80-84 years"
	    WHEN age >=1020 and age <= 1079 and gender = "M" THEN "85-89 years"
	    WHEN age >=1020 and age <= 1079 and gender = "F" THEN "85-89 years"
	    WHEN age >=1080 and gender = "M" THEN "90 plus years"
	    WHEN age >=1080 and gender = "F" THEN "90 plus years"
        END as age_group,gender as "gender", 
        COUNT(IF((days_diff < 80), 1, NULL)) as less_than_three_months,
        COUNT(IF((days_diff BETWEEN 80 and 168), 1, NULL)) as three_to_five_months,
        COUNT(IF((days_diff > 168), 1, NULL)) as six_months_plus
        from 
        (
        select map.patient_id,mwp.first_name, mwp.last_name,mwp.gender,floor(datediff(@endDate,mwp.birthdate)/@birthDateDivider) as age, map.visit_date,
        map.next_appointment_date as next_appt_date, map.art_regimen, map.arvs_given, datediff(map.next_appointment_date,map.visit_date) as days_diff
        from mw_art_followup map
        join    
        (
	    select patient_id,MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date from mw_art_followup where visit_date <= @endDate
	    group by patient_id
	    ) map1
        ON map.patient_id = map1.patient_id and map.visit_date = map1.visit_date
        join mw_patient mwp  
        on mwp.patient_id = map.patient_id
        where map.patient_id in (select pat from last_facility_outcome where state = "On antiretrovirals")
        and floor(datediff(@endDate,map.next_appointment_date)) <=  @defaultCutOff
        ) sub
        group by age_group,gender
        ) cohort on x.age_group = cohort.age_group
        and x.gender = cohort.gender
        order by sort_value
        ) x;
        """
        categories = [
            "sum(less_than_three_months)",
            "sum(three_to_five_months)",
            "sum(six_months_plus)",
        ]
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            for x in range(len(response[0])):
                print(categories[x], "[", facility, "]: ", response[0][x])
            print("----------")

    def hiv_mortality(self) -> None:
        start_date = '"2024-01-01"'
        end_date = '"2024-03-31"'
        query = """
        /* HIV Mortality */
        /* Numerator */
        use openmrs_warehouse;
        ---
        SET @startDate = {};
        ---
        SET @endDate = {};
        ---
        SET @location= {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("patient died")
            and start_date between @startDate and @endDate;
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(start_date, end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            # print(response)
            print(
                "Number of HIV patients died in quarter [ " + facility + " ]:",
                len(response),
            )

    def hiv_active_in_care(self) -> None:
        end_date = '"2024-03-31"'
        query = """
        /* Denominator */
        /* Active in care based on end date */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location= {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of HIV patients active in care [ " + facility + " ]:",
                len(response),
            )

    def hiv_active_in_care_12_months_before(self) -> None:
        end_date = '"2023-03-31"'
        query = """
        /* Denominator */
        /* Active in care based on end date */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location= {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of HIV patients active in care 12 months before [ "
                + facility
                + " ]:",
                len(response),
            )

    def hiv_active_in_care_24_months_before(self) -> None:
        end_date = '"2022-03-31"'
        query = """
        /* Denominator */
        /* Active in care based on end date */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location= {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Number of HIV patients active in care 24 months before [ "
                + facility
                + " ]:",
                len(response),
            )

    def hiv_viral_load_suppression_numerator(self) -> None:
        start_date = '"2022-12-01"'
        end_date = '"2024-03-31"'
        query = """
        /* 4. Viral Load suppression */
        /* Numerator */
        USE openmrs_warehouse;
        ---
        /* Space to cover 1 year 3 months between start date and end date */
        SET @startDate = {};
        ---
        SET @endDate = {};
        ---
        SET @location = {};
        ---
        select count(*)
        from mw_art_viral_load mavl
        join (
        SELECT patient_id as p_id, max(visit_date) as last_visit_date 
        FROM mw_art_viral_load
        where visit_date <= @endDate
        group by patient_id
        ) x
        ON x.p_id = mavl.patient_id
        and mavl.visit_date = x.last_visit_date
        where visit_date between @startDate and @endDate and location = @location
        and (ldl = "True" or less_than_limit <= 200 or viral_load_result <= 200) and other_results is null;
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(start_date, end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Viral load suppression(numerator) [ " + facility + " ]:",
                response[0][0],
            )

    def hiv_viral_load_suppression_denominator(self) -> None:
        start_date = '"2022-12-01"'
        end_date = '"2024-03-31"'
        query = """
        /* Denominator */
        USE openmrs_warehouse;
        ---
        /* Space to cover 1 year 3 months between start date and end date */
        SET @startDate = {};
        ---
        SET @endDate = {};
        ---
        SET @location = {};
        ---
        select count(*)
        from mw_art_viral_load mavl
        join (
        SELECT patient_id as p_id, max(visit_date) as last_visit_date 
        FROM mw_art_viral_load
        where visit_date <= @endDate
        group by patient_id
        ) x
        ON x.p_id = mavl.patient_id
        and mavl.visit_date = x.last_visit_date
        where visit_date between @startDate and @endDate and location = @location
        and (ldl is not null or less_than_limit is not null or viral_load_result is not null) and other_results is null;
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(start_date, end_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(
                "Viral load suppression(denominator) [ " + facility + " ]:",
                response[0][0],
            )

    def art_rententiona_at_12_months(self) -> None:
        end_date = '"2024-03-31"'
        end_reporting_date = '"2024-03-31"'
        query = """
        /* 3. % of ART retention at 12 month */

        /* Numerator - Result should subtract to denominator to get number of patients in care */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @endReportindDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location={};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff
        )
            and opi.patient_id in 
            (
        SELECT
            opi.patient_id as pat
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, end_reporting_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print("ART rentention at 12 months [ " + facility + " ]:", len(response))

    def art_rententiona_at_24_months(self) -> None:
        end_date = '"2021-06-30"'
        end_reporting_date = '"2022-06-30"'
        query = """
        /* 3. % of ART retention at 12 month */

        /* Numerator - Result should subtract to denominator to get number of patients in care */
        use openmrs_warehouse;
        ---
        SET @endDate = {};
        ---
        SET @endReportindDate = {};
        ---
        SET @defaultCutOff = 60;
        ---
        SET @location={};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
        start_date,
            program_state_id,
            end_date
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff
        )
            and opi.patient_id in 
            (
        SELECT
            opi.patient_id as pat
        FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
        FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("HIV program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
        """
        for facility in FACILITIES:
            facility = '"' + facility + '"'
            formatted_qry = query.format(end_date, end_reporting_date, facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print("ART rentention at 24 months [ " + facility + " ]:", len(response))
