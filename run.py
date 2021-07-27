import os

from app import app
from views import AdvertisementView, EmailSender

app.add_url_rule('/advertisements/', view_func=AdvertisementView.as_view('ads_list'),
                 methods=['GET', 'POST'])
app.add_url_rule('/advertisements/<int:ad_id>', view_func=AdvertisementView.as_view('ads_retrieve'),
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/email', view_func=EmailSender.as_view('post_task'),
                 methods=['POST'])
app.add_url_rule('/email/<string:task_id>', view_func=EmailSender.as_view('get_task'),
                 methods=['GET'])

if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.getenv('PORT', default=5000))
    )
