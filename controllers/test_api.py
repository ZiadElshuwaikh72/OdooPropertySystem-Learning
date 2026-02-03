from odoo import http

class TestApi(http.Controller):

    @http.route("/api/test",methods=["GET"],type="http",auth="none",csrf=False)
    def test_api(self):
        print("test_api")