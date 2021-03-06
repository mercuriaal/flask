from celery.result import AsyncResult
from flask import jsonify, request
from flask.views import MethodView

from app import db
from models import Advertisement, User
from celery_tasks import celery, send_email


class AdvertisementView(MethodView):

    def get(self, ad_id=None):
        if ad_id:
            advertisement = Advertisement.query.get_or_404(ad_id)
            return jsonify(advertisement.to_dict())
        else:
            advertisements = Advertisement.query.all()
            return jsonify([advertisement.to_dict() for advertisement in advertisements])

    def post(self):
        advertisement = Advertisement(**request.json)
        db.session.add(advertisement)
        db.session.commit()
        return jsonify(advertisement.to_dict())

    def patch(self, ad_id):
        advertisement = Advertisement.query.get_or_404(ad_id)
        patch_info = request.json
        if patch_info.get('title') is not None:
            advertisement.title = patch_info['title']
        if patch_info.get('description') is not None:
            advertisement.description = patch_info['description']
        db.session.commit()
        return jsonify(advertisement.to_dict())

    def delete(self, ad_id):
        target_advertisement = Advertisement.query.get_or_404(ad_id)
        db.session.delete(target_advertisement)
        db.session.commit()
        return jsonify(target_advertisement.to_dict())


class EmailSender(MethodView):

    def get(self, task_id):
        task = AsyncResult(task_id, app=celery)
        return jsonify({'status': task.status,
                        'result': task.result})

    def post(self):
        task = send_email.delay()
        return jsonify(
            {'task_id': task.id}
        )
