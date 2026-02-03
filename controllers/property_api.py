import json
import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request


    # Structure method valid response
def valid_response(data,pagination_info,status):
    response_body = {
    'message': 'Success',
    'data': data
    }
    if pagination_info:
        response_body['pagination'] = pagination_info

    return request.make_json_response(response_body,status= status)


    # Structure method invalid response case http
def invalid_response(error, status):
        response_body = {
            'error': error
        }
        return request.make_json_response(response_body,status= status)

    # Structure method invalid response case json
def valid_json_response(data, message="Success"):
        return {
            "message": message,
            "data": data
        }

def invalid_json_response(message):
        return {
            "message": message
        }


class PropertyApi(http.Controller):

    # Helper method
    # Validate required fields dynamically
    # vals   -> data coming from request body (dict)
    # fields -> list of required fields
    # -----------------------------------------
    def _validate_required_fields(self, vals, fields):
        for field in fields:
            # check if field not sent or empty
            if not vals.get(field):
                return f"{field} is required"
        return None



    # endpoint V1 API Create
    @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    def property_api(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        #validate on field from data from body in postmaon from request
        if not vals.get('name'):
            return request.make_json_response({
                "message":"name is required"
            }, status=400)

        try:
            res=request.env['property'].sudo().create(vals)
            if res:
                return request.make_json_response({
                    "id": res.id,
                    "name": res.name,
                    "message":"Property API successfully created",
                },status=200)
        except Exception as error:
            return request.make_json_response({
                "message":error
            },status=400)

    # # endpoint V1 API Create using execution sql query
    # @http.route("/v1/property",methods=["POST"],type="http",auth="none",csrf=False)
    # def property_api(self):
    #     args=request.httprequest.data.decode()
    #     vals=json.loads(args)
    #     #validate on field from data from body in postmaon from request
    #     if not vals.get('name'):
    #         return request.make_json_response({
    #             "message":"name is required"
    #         }, status=400)
    #
    #     try:
    #         # res=request.env['property'].sudo().create(vals)
    #
    #         # حول string → JSON valid
    #         vals['name'] = json.dumps(vals['name'])
    #
    #         cr=request.env.cr
    #         columns=','.join(vals.keys())
    #         values=','.join(['%s'] * len(vals))
    #         query=f"""INSERT INTO property ({columns})
    #                 VALUES ({values}) returning id,name,postcode """
    #         cr.execute(query,tuple(vals.values()))
    #         res=cr.fetchone()
    #         if res:
    #             return request.make_json_response({
    #                 "message": "Property API successfully created",
    #                 "id":     res[0],
    #                 "name": res[1],
    #                 "postcode": res[2],
    #             },status=200)
    #     except Exception as error:
    #         return request.make_json_response({
    #             "message":error
    #         },status=400)

    # endpoint V2 API Create
    @http.route("/v2/property", methods=["POST"], type="json", auth="none", csrf=False)
    def property_api_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # Reusable validation
        error = self._validate_required_fields(vals, ['name','postcode'])
        if error:
            return{
                "message":error,
            }
            # Create record
        res = request.env['property'].sudo().create(vals)
        if res:
            return {
                "id":res.id,
                "name":res.name,
                "message": "Property API successfully created"
            }
    #EndPoint Update
    @http.route("/v1/property/<int:property_id>",methods=["PUT"],type="json", auth="none", csrf=False)
    def update_property(self,property_id):
       try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return{
                    "message":"property not found"
                }
            args=request.httprequest.data.decode()
            vals=json.loads(args)
            property_id.write(vals)
            #return Response
            return{
                "id":property_id.id,
                "name":property_id.name,
                "message":"Property API successfully updated"
            }
       except Exception as error:
            return {
                "message":error
            }
    #EndPoint Get Record
    @http.route("/v1/property/<int:property_id>",methods=["GET"],type="http", auth="none", csrf=False)
    def get_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error":"property not found"
                },status=404)
            return request.make_json_response({
                "id":property_id.id,
                "name":property_id.name,
                "postcode":property_id.postcode,
                "ref":property_id.ref,
                "description":property_id.description,
                "bedrooms":property_id.bedrooms,
                "expected_price":property_id.expected_price,
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "error":error
            },status=400)
        #Endpoint Delete
    @http.route("/v1/property/<int:property_id>",methods=["DELETE"],type="http", auth="none", csrf=False)
    def delete_property(self,property_id):
        try:
            property_id=request.env['property'].sudo().search([('id','=',property_id)])
            if not property_id:
                return request.make_json_response({
                    "error":"property not found"
                },status=404)
            #method Delete
            property_id.unlink()
            return request.make_json_response({
                "message":"Property API successfully deleted"
            },status=200)
        except Exception as error:
            return request.make_json_response({
                "error":error
            },status=400)

        # GET ALL and filteration on record
        # implentaion structure method valid and invalid response
    @http.route("/v1/properties",methods=["GET"],type="http", auth="none", csrf=False)
    def get_all_properties_list(self):
        try:
            #get data from request
            params=parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain=[]
            #pagination
            page=offset=None
            limit=5
            if params:
                if params.get('limit'):
                    limit=int(params.get('limit')[0])
                if params.get('page'):
                    page=int(params.get('page')[0])
                if page:
                    offset=(page*limit)-limit
            # filteration on return records
            if params.get('state'):
                property_domain +=[('state','=',params.get('state')[0])]

            property_records=request.env['property'].sudo().search(property_domain,offset=offset,limit=limit,order='id desc')
            # count records using search_count
            property_count=request.env['property'].sudo().search_count(property_domain)

            if not property_records:
                return invalid_response("property not found",status=404)

                # 1
            # return valid_response([{
            #     "id":property_id.id,
            #     "name":property_id.name,
            #     "postcode":property_id.postcode,
            #     "ref":property_id.ref,
            #     "description":property_id.description,
            #     "bedrooms":property_id.bedrooms,
            #     "expected_price":property_id.expected_price,
            #     "state":property_id.state,
            # } for property_id in property_records],status=200)

            # 1 the same 2

               # 2
            # Prepare data
            data = []
            for prop in property_records:
                data.append({
                    "id": prop.id,
                    "name": prop.name,
                    "postcode": prop.postcode,
                    "ref": prop.ref,
                    "description": prop.description,
                    "bedrooms": prop.bedrooms,
                    "expected_price": prop.expected_price,
                    "state": prop.state,
                })
            #pagination as metadata
            pagination_info = {
                'page': page if page else 1,
                'limit': limit,
                'total_records': property_count,
                'pages': math.ceil(property_count / limit) if limit else 1,
            }

            return valid_response(data,pagination_info,status=200)

        except Exception as e:
            return request.make_json_response({
                "error": str(e)
            }, status=400)


