from requests import Session
from parsers.lib.exceptions import ParserException
from parsers.lib import web
from parsers.lib import countrycode
from parsers.lib import IN


def fetch_consumption(country_code='IN-KA', session=None):
    """Fetch Karnataka consumption"""
    countrycode.assert_country_code(country_code, 'IN-KA')
    html = web.get_response_soup(country_code, 'http://kptclsldc.com/Default.aspx', session)

    india_date_time = IN.read_datetime_from_span_id(html, 'Label6', 'DD/MM/YYYY HH:mm')

    demand_value = IN.read_value_from_span_id(html, 'Label5')

    data = {
        'countryCode': country_code,
        'datetime': india_date_time.datetime,
        'consumption': demand_value,
        'source': 'kptclsldc.com'
    }

    return data


def fetch_production(country_code='IN-KA', session=None):
    """Fetch Karnataka  production"""
    countrycode.assert_country_code(country_code, 'IN-KA')

    html = web.get_response_soup(country_code, 'http://kptclsldc.com/StateGen.aspx', session)

    india_date_time = IN.read_datetime_from_span_id(html, 'lbldate', 'M/D/YYYY h:mm:ss A')

    # RTPS Production: https://en.wikipedia.org/wiki/Raichur_Thermal_Power_Station
    rtps_value = IN.read_value_from_span_id(html, 'lblrtptot')

    # BTPS Production: https://en.wikipedia.org/wiki/Bellary_Thermal_Power_station
    btps_value = IN.read_value_from_span_id(html, 'lblbtptot')

    # YTPS Production: https://en.wikipedia.org/wiki/Yermarus_Thermal_Power_Station
    ytps_value = IN.read_value_from_span_id(html, 'ytptot')

    # UPCL Production: https://en.wikipedia.org/wiki/Udupi_Power_Plant
    upcl_value = IN.read_value_from_span_id(html, 'lblupctot')

    # JINDAl Production: https://en.wikipedia.org/wiki/JSW_Vijayanagar_Power_Station
    jindal_value = IN.read_value_from_span_id(html, 'lbljintot')

    # Coal Production
    coal_value = rtps_value + btps_value + ytps_value + upcl_value + jindal_value

    # Sharavati Production: Sharavati  Hydroelectric
    sharavati_value = IN.read_value_from_span_id(html, 'lblshvytot')

    # Nagjhari Production: Kalinadi-Nagjhari Hydroelectric
    nagjhari_value = IN.read_value_from_span_id(html, 'lblngjtot')

    # Varahi Production: https://en.wikipedia.org/wiki/Varahi_River#Varahi_Hydro-electric_Project
    varahi_value = IN.read_value_from_span_id(html, 'lblvrhtot')

    # Kodsalli Production: Kalinadi Kodasalli Hydroelectric
    kodsalli_value = IN.read_value_from_span_id(html, 'lblkdsltot')

    # Kadra Production: https://en.wikipedia.org/wiki/Kadra_Dam
    kadra_value = IN.read_value_from_span_id(html, 'lblkdrtot')

    # GERUSOPPA production: Gerusoppa Dam
    gerusoppa_value = IN.read_value_from_span_id(html, 'lblgrsptot')

    # JOG production: https://en.wikipedia.org/wiki/Jog_Falls
    jog_value = IN.read_value_from_span_id(html, 'lbljogtot')

    # LPH Production: Linganamakki Dam
    lph_value = IN.read_value_from_span_id(html, 'lbllphtot')

    # Supa production: https://en.wikipedia.org/wiki/Supa_Dam
    supa_value = IN.read_value_from_span_id(html, 'lblsupatot')

    # SHIMSHA: https://en.wikipedia.org/wiki/Shimsha#Power_generation
    shimsha_value = IN.read_value_from_span_id(html, 'lblshimtot')

    # SHIVASAMUDRA: https://en.wikipedia.org/wiki/Shivanasamudra_Falls#Power_generation
    shivasamudra_value = IN.read_value_from_span_id(html, 'lblshivtot')

    # MANIDAM: Mani Dam Hydroelectric
    manidam_value = IN.read_value_from_span_id(html, 'lblmanitot')

    # MUNRABAD: Munirabad Hydroelectric
    munrabad_value = IN.read_value_from_span_id(html, 'lblmbdtot')

    # BHADRA: https://en.wikipedia.org/wiki/Bhadra_Dam
    bhadra_value = IN.read_value_from_span_id(html, 'lblbdratot')

    # GHATAPRABHA: Ghataprabha Hydroelectric
    ghataprabha_value = IN.read_value_from_span_id(html, 'lblgtprtot')

    # ALMATTI: https://en.wikipedia.org/wiki/Almatti_Dam
    almatti_value = IN.read_value_from_span_id(html, 'lblalmttot')

    # CGS (Central Generating Stations) Production
    # TODO: Search CGS production type
    cgs_value = IN.read_value_from_span_id(html, 'lblcgs')

    # NCEP (Non-Conventional Energy Production)
    ncep_html = web.get_response_soup(country_code, 'http://kptclsldc.com/StateNCEP.aspx', session)
    ncep_date_time = IN.read_datetime_from_span_id(ncep_html, 'Label1', 'DD/MM/YYYY HH:mm:ss')

    # Check ncep date is similar than state gen date
    if abs(india_date_time.timestamp - ncep_date_time.timestamp) > 600:
        raise ParserException('IN-KA', 'NCEP or State datetime is not valid')

    biomass_value = IN.read_value_from_span_id(ncep_html, 'lbl_tb')

    # TODO: Cogeneration value production type?
    cogen_value = IN.read_value_from_span_id(ncep_html, 'lbl_tc')

    mini_hydro_value = IN.read_value_from_span_id(ncep_html, 'lbl_tm')

    wind_value = IN.read_value_from_span_id(ncep_html, 'lbl_tw')

    solar_value = IN.read_value_from_span_id(ncep_html, 'lbl_ts')

    # Hydro production
    hydro_value = sharavati_value + nagjhari_value + varahi_value + kodsalli_value \
                  + kadra_value + gerusoppa_value + jog_value + lph_value + supa_value \
                  + shimsha_value + shivasamudra_value + manidam_value + munrabad_value \
                  + bhadra_value + ghataprabha_value + almatti_value + mini_hydro_value

    # Unknown production
    unknown_value = cgs_value + cogen_value

    data = {
        'countryCode': country_code,
        'datetime': india_date_time.datetime,
        'production': {
            'biomass': biomass_value,
            'coal': coal_value,
            'gas': 0.0,
            'hydro': hydro_value,
            'nuclear': 0.0,
            'oil': 0.0,
            'solar': solar_value,
            'wind': wind_value,
            'geothermal': 0.0,
            'unknown': unknown_value
        },
        'storage': {
            'hydro': 0.0
        },
        'source': 'kptclsldc.com',
    }

    return data


if __name__ == '__main__':
    session = Session()
    print fetch_production('IN-KA', session)
    print fetch_consumption('IN-KA', session)
