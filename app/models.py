from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, foreign, object_session
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Admin1CodesAscii(db.Model):
    __tablename__ = 'admin1CodesAscii'

    code = db.Column(db.String(15), index=True, primary_key=True)
    name = db.Column(db.Text)
    nameAscii = db.Column(db.Text)
    geonameid = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f"<Admin1CodesAscii(code={self.code}, name={self.name})>"

class Admin2Codes(db.Model):
    __tablename__ = 'admin2Codes'

    code = db.Column(db.String(15), index=True, primary_key=True)
    name = db.Column(db.Text)
    nameAscii = db.Column(db.Text)
    geonameid = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f"<Admin2Codes(code={self.code}, name={self.name})>"

class AlternateName(db.Model):
    __tablename__ = 'alternatename'

    alternatenameId = db.Column(db.Integer, primary_key=True)
    geonameid = db.Column(db.Integer, db.ForeignKey('geoname.geonameid'))
    isoLanguage = db.Column(db.String(7), index=True)
    alternateName = db.Column(db.String(200), index=True)
    isPreferredName = db.Column(db.Boolean)
    isShortName = db.Column(db.Boolean)
    isColloquial = db.Column(db.Boolean)
    isHistoric = db.Column(db.Boolean)

    geoname = relationship('Geoname', back_populates='alternate_names_table')

    def __repr__(self):
        return f"<AlternateName(alternateName={self.alternateName}, isoLanguage={self.isoLanguage})>"

class ContinentCodes(db.Model):
    __tablename__ = 'continentCodes'

    code = db.Column(db.String(2), index=True, primary_key=True)
    name = db.Column(db.String(20))
    geonameid = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f"<ContinentCodes(code={self.code}, name={self.name})>"

class CountryInfo(db.Model):
    __tablename__ = 'countryinfo'

    iso_alpha2 = db.Column(db.String(2), index=True)
    iso_alpha3 = db.Column(db.String(3), index=True)
    iso_numeric = db.Column(db.Integer, index=True)
    fips_code = db.Column(db.String(3), index=True)
    name = db.Column(db.String(200))
    capital = db.Column(db.String(200))
    areainsqkm = db.Column(db.Float)
    population = db.Column(db.Integer)
    continent = db.Column(db.String(2), index=True)
    tld = db.Column(db.String(3))
    currency = db.Column(db.String(3))
    currencyName = db.Column(db.String(20))
    Phone = db.Column(db.String(10))
    postalCodeFormat = db.Column(db.String(100))
    postalCodeRegex = db.Column(db.String(255))
    geonameId = db.Column(db.Integer, index=True, primary_key=True)
    languages = db.Column(db.String(200))
    neighbours = db.Column(db.String(100))
    equivalentFipsCode = db.Column(db.String(10))

    def __repr__(self):
        return f"<CountryInfo(name={self.name}, iso_alpha2={self.iso_alpha2})>"

class FeatureCodes(db.Model):
    __tablename__ = 'featureCodes'

    code = db.Column(db.String(7), index=True, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<FeatureCodes(code={self.code}, name={self.name})>"

class Geoname(db.Model):
    __tablename__ = 'geoname'

    geonameid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    asciiname = db.Column(db.String(200))
    alternatenames = db.Column(db.String(4000))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    fclass = db.Column(db.String(1))
    fcode = db.Column(db.String(10))
    country = db.Column(db.String(2), index=True)
    cc2 = db.Column(db.String(200))
    admin1 = db.Column(db.String(20), index=True)
    admin2 = db.Column(db.String(80), index=True)
    admin3 = db.Column(db.String(20))
    admin4 = db.Column(db.String(20))
    population = db.Column(db.Integer, index=True)
    elevation = db.Column(db.Integer)
    gtopo30 = db.Column(db.Integer)
    timezone = db.Column(db.String(40))
    moddate = db.Column(db.Date)

    alternate_names_table = relationship('AlternateName', back_populates='geoname')
    country_info = relationship('CountryInfo', 
                                primaryjoin="Geoname.country == foreign(CountryInfo.iso_alpha2)", 
                                viewonly=True, 
                                uselist=False)

    def __repr__(self):
        return f"<Geoname(name={self.name}, geonameid={self.geonameid})>"

    # -------------------------------------------------------------------------
    def _get_preferred_name(self, lang=None):
        if not lang:
            return self.name

        for alt in self.alternate_names_table:
            if alt.isoLanguage == lang and alt.isPreferredName:
                return alt.alternateName

        # fallback to default name
        return self.name


    # -------------------------------------------------------------------------
    def _get_alternate_names(self, lang=None):
        result = {}

        for alt in self.alternate_names_table:
            if lang and alt.isoLanguage != lang:
                continue

            if alt.isoLanguage not in result:
                result[alt.isoLanguage] = []

            result[alt.isoLanguage].append(alt.alternateName)

        return result

    # -------------------------------------------------------------------------
    def _get_country_name(self, lang=None):
        if not self.country_info:
            return None

        # Default English name
        default_name = self.country_info.name

        if not lang:
            return default_name

        session = object_session(self)

        alt = (
            session.query(AlternateName)
            .filter(
                AlternateName.geonameid == self.country_info.geonameId,
                AlternateName.isoLanguage == lang,
                AlternateName.isPreferredName == True
            )
            .first()
        )

        if alt:
            return alt.alternateName

        return default_name
        
 
    # app/models.py
    def to_dict(self, fields=None, lang=None):
        """
        fields: list of requested fields (or None for full representation)
        lang: language code affecting language-dependent fields
        """

        # --- Core field map ---
        field_map = {
            "geonameId": lambda: self.geonameid,
            "name": lambda: self._get_preferred_name(lang),
            "country.code": lambda: self.country,
            "country.name": lambda: self._get_country_name(lang),
            "latitude": lambda: float(self.latitude) if self.latitude else None,
            "longitude": lambda: float(self.longitude) if self.longitude else None,
            "population": lambda: self.population,
            "alternate_names": lambda: self._get_alternate_names(lang),
        }

        # --- Default: full representation ---
        if not fields:
            return {
                key: resolver()
                for key, resolver in field_map.items()
            }

        # --- Filtered representation ---
        result = {}
        for field in fields:
            if field in field_map:
                result[field] = field_map[field]()

        return result

class Hierarchy(db.Model):
    __tablename__ = 'hierarchy'

    id = db.Column(db.Integer, index=True, primary_key=True)
    parentId = db.Column(db.Integer, index=True)
    childId = db.Column(db.Integer, index=True)
    type = db.Column(db.String(50))

    def __repr__(self):
        return f"<Hierarchy(parentId={self.parentId}, childId={self.childId})>"

class IsoLanguageCodes(db.Model):
    __tablename__ = 'iso_languagecodes'

    id = db.Column(db.Integer, index=True, primary_key=True)
    iso_639_3 = db.Column(db.String(4))
    iso_639_2 = db.Column(db.String(50))
    iso_639_1 = db.Column(db.String(50))
    language_name = db.Column(db.String(200))

    def __repr__(self):
        return f"<IsoLanguageCodes(language_name={self.language_name})>"

class TimeZones(db.Model):
    __tablename__ = 'timeZones'

    country = db.Column(db.String(2), index=True)
    timeZoneId = db.Column(db.String(200), primary_key=True)
    GMT_offset = db.Column(db.Numeric(3, 1))
    DST_offset = db.Column(db.Numeric(3, 1))
    raw_offset = db.Column(db.Numeric(3, 1))

    def __repr__(self):
        return f"<TimeZones(country={self.country}, timeZoneId={self.timeZoneId})>"

class PostalCodes(db.Model):
    __tablename__ = 'postalCodes'

    country = db.Column(db.String(2), index=True)
    postal_code = db.Column(db.String(20), index=True, primary_key=True)
    name = db.Column(db.String(180))
    admin1_name = db.Column(db.String(100))
    admin1_code = db.Column(db.String(20), index=True)
    admin2_name = db.Column(db.String(100))
    admin2_code = db.Column(db.String(20))
    admin3_name = db.Column(db.String(100))
    admin3_code = db.Column(db.String(20))
    latitude = db.Column(db.Numeric(10, 7))
    longitude = db.Column(db.Numeric(10, 7))
    accuracy = db.Column(db.SmallInteger)

    def __repr__(self):
        return f"<PostalCodes(postal_code={self.postal_code}, country={self.country})>"

