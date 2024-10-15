# app/routes.py
from flask import jsonify, request
from .models import Geoname, AlternateName
from . import db

def register_routes(app):
    @app.route('/places', methods=['GET'])
    def get_places():
        name = request.args.get('name')
        country = request.args.get('country')
        query = db.session.query(Geoname).filter(Geoname.name.ilike(f'%{name}%'))
        if country:
            query = query.filter(Geoname.country == country)
        results = query.all()
        return jsonify([place.to_dict() for place in results]), (200 if results else 404)

    @app.route('/places/bulk', methods=['POST'])
    def bulk_lookup():
        data = request.json
        results = []
        for item in data:
            name = item['name']
            country = item.get('country')
            query = db.session.query(Geoname).filter(Geoname.name.ilike(f'%{name}%'))
            if country:
                query = query.filter(Geoname.country == country)
            results.extend(query.all())
        return jsonify([place.to_dict() for place in results]), (200 if results else 404)

    @app.route('/place/<int:geonameId>', methods=['GET'])
    def get_place(geonameId):
        place = db.session.query(Geoname).get(geonameId)
        if place:
            return jsonify(place.to_dict()), 200
        return jsonify({'error': 'Place not found'}), 404

    @app.route('/place/<int:geonameId>/name', methods=['GET'])
    def get_place_name(geonameId):
        place = db.session.query(Geoname).get(geonameId)
        if place:
            return place.name, 200
        return jsonify({'error': 'Place not found'}), 404

    @app.route('/place/<int:geonameId>/alternatenames', methods=['GET'])
    def get_alternate_names(geonameId):
        names = db.session.query(AlternateName).filter_by(geonameid=geonameId).all()
        if names:
            return jsonify([name.to_dict() for name in names]), 200
        return jsonify({'error': 'No alternate names found'}), 404
