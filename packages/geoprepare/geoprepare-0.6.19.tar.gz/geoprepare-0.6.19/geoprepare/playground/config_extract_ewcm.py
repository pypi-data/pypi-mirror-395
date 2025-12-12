import re

# Configuration text
config_text = """[[austria]
[belgium]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[latvia]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[bulgaria]
[lithuania]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[croatia]
[luxembourg]
[cyprus]
[malta]
[czech_republic]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[netherlands]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[denmark]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[poland]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[estonia]
[portugal]
[finland]

[paraguay]
crops = ['sb']

[romania]
crops = ['ww', 'mz']

[slovakia]
[slovenia]
[greece]
[sweden]

[thailand]
crops = ['rc']

[ireland]

[philippines]
crops = ['rc']

[japan]
crops = ['rc']

[vietnam]
crops = ['rc']

[turkey]
crops = ['ww']

[argentina]
; 'argentina' chirps data for 2017 is missing
crops = ['sb', 'ww', 'mz']

[australia]
crops = ['ww', 'mz']

[brazil]
; 'brazil' chirps data for 2017 is missing
crops = ['mz', 'sb', 'ww', 'rc']

[china]
; CHIRPS covers China almost completely but extreme N part is left behind

[egypt]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[india]
crops = ['rc', 'mz', 'ww', 'sb']

[france]
crops = ['ww', 'mz']

[mexico]
crops = ['ww', 'mz', 'sb']

[hungary]
crops = ['ww', 'mz']

[indonesia]
crops = ['mz', 'rc']

[italy]
crops = ['ww', 'mz']

[south_africa]
crops = ['mz', 'ww']

[spain]
crops = ['ww', 'mz']

[united_states_of_america]

[republic_of_korea]
crops = ['rc']

[canada]
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[germany]
crops = ['ww', 'mz']
eo_all = ['crop_stats', 'ndvi', 'gcvi',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[kazakhstan]
crops = ['sw']
eo_all = ['crop_stats', 'ndvi', 'gcvi',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[russian_federation]
; 'sw' TODO
LIST_ABB_CROPS = ['ww', 'sw', 'mz']
IGNORE_3rd = False
eo_all = ['crop_stats', 'ndvi', 'gcvi',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = []  ; ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

[ukraine]
LIST_ABB_CROPS = ['ww', 'mz', 'sb']
; luhans'ka_185013000 is mising esi_4wk data
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface', 'esi_4wk']  ; Yield-gap

[u.k._of_great_britain_and_northern_ireland]
crops = ['ww', 'mz']
eo_all = ['crop_stats', 'ndvi', 'gcvi', 'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
SEASONAL_STD = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_MAX = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
SEASONAL_AGG = ['ndvi', 'GDD', 'cpc_tmin', 'cpc_tmax', 'esi_4wk', 'cpc_precip']
eo_model = ['ndvi', 'GDD', 'cpc_tmax', 'cpc_tmin', 'cpc_precip', 'esi_4wk', 'nsidc_surface', 'nsidc_rootzone']
cond_yg = ['ndvi',  'GDD',  'cpc_tmin', 'cpc_tmax', 'cpc_precip', 'nsidc_surface']  ; Yield-gap

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; EWCM
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
[afghanistan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw', 'rc']
USE_CROPLAND_MASK = True

[algeria]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sw', 'ww']
USE_CROPLAND_MASK = True

[angola]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[bangladesh]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['rc']
USE_CROPLAND_MASK = True

[benin]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[botswana]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[bolivia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz']
USE_CROPLAND_MASK = True

[burkina_faso]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[burundi]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[cambodia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['rc']
USE_CROPLAND_MASK = True

[colombia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz']
USE_CROPLAND_MASK = True

[cuba]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[cameroon]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[cape_verde]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[central_african_republic]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sb', 'mz', 'sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[chad]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[congo]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[cote_d'ivoire]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[democratic_republic_of_the_congo]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[djibouti]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[equatorial_guinea]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[eritrea]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[eswatini]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[ethiopia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[equador]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz']
USE_CROPLAND_MASK = True

[gambia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[ghana]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[guinea-bissau]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[guinea]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[haiti]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[iraq]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[kenya]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[kyrgyzstan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw', 'rc']
USE_CROPLAND_MASK = True

[lao_people's_democratic_republic]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sb', 'mz', 'sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[liberia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[libya]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[lebanon]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[lesotho]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[madagascar]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[malawi]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[mali]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[mauritania]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[mozambique]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[mongolia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[morocco]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[myanmar]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sb', 'mz', 'sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[namibia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['sr', 'rc', 'ww', 'mz']
USE_CROPLAND_MASK = True

[nepal]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sb', 'mz', 'sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[niger]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[nigeria]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[pakistan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw', 'rc']
USE_CROPLAND_MASK = True

[peru]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz']
USE_CROPLAND_MASK = True

[rwanda]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[senegal]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[sierra_leone]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[somalia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[south_sudan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[sri_lanka]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz']
USE_CROPLAND_MASK = True

[sudan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[swaziland]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[syrian_arab_republic]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw']
USE_CROPLAND_MASK = True

[tajikistan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[togo]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops = ['mz', 'sr', 'rc']
USE_CROPLAND_MASK = True

[tunisia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sw', 'ww']
USE_CROPLAND_MASK = True

[turkmenistan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['ww', 'sw', 'rc']
USE_CROPLAND_MASK = True

[uganda]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[united_republic_of_tanzania]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[uzbekistan]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = EWCM_Level_1.shp
crops= ['sw', 'ww', 'rc']
USE_CROPLAND_MASK = True

[yemen]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww', 'tf']
USE_CROPLAND_MASK = True

[zambia]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'rc', 'ww']
USE_CROPLAND_MASK = True

[zimbabwe]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops= ['mz', 'sr', 'rc', 'ww']
USE_CROPLAND_MASK = True

[el_salvador]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[guatemala]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[honduras]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[nicaragua]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['mz', 'rc', 'sb']
USE_CROPLAND_MASK = True

[iran__(islamic_republic_of)]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['ww', 'sw']
USE_CROPLAND_MASK = True

[chile]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['ww']
USE_CROPLAND_MASK = True

[dem_people's_rep_of_korea]
category = EWCM
calendar_file = EWCM_2024-10-16.xlsx
shp_boundary = Level_1_without_special_characters.shp
crops = ['mz', 'rc']
USE_CROPLAND_MASK = True]"""  # Replace with your actual configuration text

# Extract EWCM countries
ewcm_countries = re.findall(r'\[(.*?)\]\ncategory\s*=\s*EWCM', config_text)

# Sort countries alphabetically
ewcm_countries_sorted = sorted(ewcm_countries)

# Display result
for country in ewcm_countries_sorted:
    print(country)
