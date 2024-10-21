# app/routes.py
from flask import jsonify, request
from .models import Geoname, AlternateName, CountryInfo
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from . import db

def register_routes(app):

    #--------------------------------------------------------------------------
    @app.route('/places', methods=['GET'])
    def get_places():
        name = request.args.get('name')
        country = request.args.get('countryName')
        countryCode = request.args.get('countryCode')

        query = db.session.query(Geoname) \
        .join(AlternateName, Geoname.geonameid == AlternateName.geonameid) \
        .filter(AlternateName.alternateName == name) \
        .filter(Geoname.fclass == 'P') \
        .filter(Geoname.fcode.like('PPL%'))

        if countryCode:
          query = query.filter(Geoname.country == countryCode)
        elif country:
            AlternateNameCountry = aliased(AlternateName)

            query = query.join(CountryInfo, Geoname.country == CountryInfo.iso_alpha2) \
            .join(AlternateNameCountry, CountryInfo.geonameId == AlternateNameCountry.geonameid) \
            .filter(AlternateNameCountry.alternateName == country)

        results = query.all()

       
        return jsonify([place.to_dict() for place in results]), (200 if results else 404)

    #--------------------------------------------------------------------------
    @app.route('/placename', methods=['GET'])
    def get_placename():
        name = request.args.get('name')
        country = request.args.get('countryName')
        countryCode = request.args.get('countryCode')
        language = request.args.get('language')

        query = db.session.query(Geoname) \
        .join(AlternateName, Geoname.geonameid == AlternateName.geonameid) \
        .filter(AlternateName.alternateName == name) \
        .filter(Geoname.fclass == 'P') \
        .filter(Geoname.fcode.like('PPL%'))

        if countryCode:
          query = query.filter(Geoname.country == countryCode)
        elif country:
            AlternateNameCountry = aliased(AlternateName)

            query = query.join(CountryInfo, Geoname.country == CountryInfo.iso_alpha2) \
            .join(AlternateNameCountry, CountryInfo.geonameId == AlternateNameCountry.geonameid) \
            .filter(AlternateNameCountry.alternateName == country)

        result = query.first()

        if language:
          if result:
            for alt in result.alternate_names_table:
              if alt.isoLanguage == language:
                return alt.alternateName, 200
          return '', 404
        else:
          if result:
            return result.name, 200
          else:
            return '', 404


    #--------------------------------------------------------------------------
#    @app.route('/places/bulk', methods=['POST'])
#    def bulk_lookup():
#        data = request.json
#        results = []
#        for item in data:
#            name = item['names']
#            country = item.get('country')
#            query = db.session.query(Geoname).filter(Geoname.name.ilike(f'%{name}%'))
#            if country:
#                query = query.filter(Geoname.country == country)
#            results.extend(query.all())
#        return jsonify([place.to_dict() for place in results]), (200 if results else 404)

    #--------------------------------------------------------------------------
    @app.route('/place/<int:geonameId>', methods=['GET'])
    def get_place(geonameId):
        place = db.session.query(Geoname).get(geonameId)
        if place:
            return jsonify(place.to_dict()), 200
        return jsonify({'error': 'Place not found'}), 404

    #--------------------------------------------------------------------------
#    @app.route('/place/<int:geonameId>/name', methods=['GET'])
#    def get_place_name(geonameId):
#
#        language = request.args.get('language')
#
#        if language:
#          places = db.session.query(Geoname) \
#          .join(AlternateName, Geoname.geonameid == AlternateName.geonameid) \
#          .filter(AlternateName.isoLanguage == language) \
#          .get(geonameId) 
#
#          if places:
#            # todo
#            pass
#          else:
#            return 'error: Place not found', 404
#
#        else: 
#          place = db.session.query(Geoname).get(geonameId)
#          if place:
#            return place.name, 200
#          return 'error: Place not found', 404

    #--------------------------------------------------------------------------
#    @app.route('/place/<int:geonameId>/alternatenames', methods=['GET'])
#    def get_alternate_names(geonameId):
#        names = db.session.query(AlternateName).filter_by(geonameid=geonameId).all()
#        if names:
#            return jsonify([name.to_dict() for name in names]), 200
#        return jsonify({'error': 'No alternate names found'}), 404

