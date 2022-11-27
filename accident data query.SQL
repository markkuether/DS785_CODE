SELECT ev.ev_id, ev.ev_date, ev.ev_state, ev.ev_city, ev.latitude, ev.longitude, ev.apt_name, ev_nr_apt_id, ac.rwy_num, es.occurrence_code, es.occurrence_description,
ac.acft_category, ac.acft_make, ac.acft_model, ac.acft_series, ac.regis_no
FROM FAA_ACCIDENTS_2022.DBO.EVENTS AS ev
JOIN FAA_ACCIDENTS_2022.DBO.Events_Sequence AS es
ON ev.ev_id = es.ev_id
JOIN FAA_ACCIDENTS_2022.DBO.aircraft AS ac
ON ev.ev_id = ac.ev_id
join FAA_ACCIDENTS_2022.DBO.engines AS eg
ON ev.ev_id = eg.ev_id
WHERE ev.ev_date BETWEEN '2021-09-01' AND '2022-09-01'
AND es.phase_no IN (505, 506,507,508,509,550, 551, 552, 650)
AND es.eventsoe_no IN 
(000, 080, 090, 091, 092, 093, 094, 096, 097, 120, 200, 220,
230,231, 232, 240, 241, 270, 271, 280, 290, 300)
AND es.defining_ev = 1
AND ac.acft_category = 'AIR'
AND ac.total_seats < 8
AND ac.num_eng = 1
AND eg.eng_type = 'rec'
ORDER BY ev.ev_state, ev.ev_city