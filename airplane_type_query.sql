select m.MODE_S_CODE_HEX, CONCAT('N',m.N_NUMBER) as "N_NUMBER",r.MFR,r.model
from FAA_Reg_Aircraft.dbo.mstr as m
join FAA_REG_AIRCRAFT.dbo.ACFTREF AS r
on m.[MFR_MDL_CODE] = r.code
where m.MODE_S_CODE_HEX in ('a2f357',
'ae621b',
'a4ff25',
'a97f4c',
'a3b4e9',
'ab72b7',
'aa1e41',
'aa2d14',
'a4ce25',
'a4af35',
'a666d0',
'a51b1a',
'a54c11',
'a64517',
'a88e08',
'a0062e',
'a01d70',
'abeca0',
'a9f14c',
'ad1957',
'a12141',
'a89f0f',
'a0e0bc',
'a880b0',
'acad38',
'a37e02',
'a4db2c',
'a9500f',
'a7d9e6',
'a2dac7',
'a72746',
'a66d6a',
'a8dcb2',
'ad4405',
'adc800',
'a1c82c',
'a2718b',
'ac2d33',
'a5de4a',
'a76297',
'a00624',
'a10588',
'ac4fb3',
'a7515d',
'ab077f',
'a0c85f',
'ab7e69',
'a5e16b',
'ac1cf4',
'a93eb8',
'a405e0',
'af18bd',
'a08dd1',
'a86365',
'a709d2',
'a3bcf7')
