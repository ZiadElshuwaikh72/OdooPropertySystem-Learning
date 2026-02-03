from odoo import models, fields,api
from odoo.exceptions import ValidationError
from datetime import timedelta
import requests

class Property(models.Model):
    _name='property'
    # _description='Property_record'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True,default='New',size=50,translate=True)
    ref=fields.Char(default='New',readonly=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=True)
    date_availability = fields.Date(tracking=True)
    expected_selling_date = fields.Date(tracking=True)
    is_late= fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage=fields.Boolean(groups="app_one.property_manager_group")
    garden=fields.Boolean(groups="app_one.property_manager_group")
    garden_area = fields.Integer()
    garden_orientation= fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),

    ])
    owner_id=fields.Many2one('owner')
    tag_ids=fields.Many2many('tag')
    owner_address=fields.Char(related='owner_id.address')
    owner_phone=fields.Char(related='owner_id.phone')

    state=fields.Selection([
        ('draft','Draft'),
        ('pinding','Pinding'),
        ('sold','Sold'),
        ('end','End'),
        ('closed','Closed'),
    ],default='draft')

    _sql_constraints = [
        ('unique_name', 'unique(name)','This name is already in use.')
    ]

    line_ids=fields.One2many('property.line','property_id')
    active=fields.Boolean(default=True)

    create_time=fields.Datetime(default=fields.Datetime.now)
    next_time=fields.Datetime(compute='_compute_next_time')

    @api.depends('expected_price','selling_price','owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("inside _compute_diff")
            rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("inside _onchange_expected_price")
            return{
                'warning':{'tittle':'warning','message':'not allow enter number negative','type':'notification'}
            }



    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
      for rec in self:
        if rec.bedrooms == 0:
            raise ValidationError('Bedrooms must be greater than 0')




    def action_draft(self):
        for rec in self:
            # call method create_history_record
            rec.create_history_record(rec.state,'draft')
            print("choose in draft")
            rec.state='draft'


    def action_pinding(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pinding')
            print("choose in pinding")
            rec.state='pinding'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            print("choose in sold")
            rec.state='sold'



    def action_end(self):
        for rec in self:
            rec.create_history_record(rec.state, 'end')
            print("choose in end")
            rec.state='end'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state='closed'

          # Cross-Model Creation
    def create_history_record(self,old_state,new_state,reason=None):
      for rec in self:
          rec.env['property.history'].create({
              'user_id':rec.env.uid,
              'property_id':rec.id,
              'old_state':old_state,
              'new_state':new_state,
              'reason':reason
          })



    # Automated Action ( cron jobs)
    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if (rec.expected_selling_date
                    and rec.expected_selling_date < fields.Date.today()
                    and rec.state in ['draft','pinding']
                ):
                rec.is_late=True
            else:
                rec.is_late=False


              #  Env
    def action_env(self):
      print(self.env['owner'].search([]))

            #  Sequence
    @api.model
    def create(self, vals):
        res=super(Property,self).create(vals)
        if res.ref=='New':
         res.ref=self.env['ir.sequence'].next_by_code('property_seq')
         return res

        #Method Server action with change state wizard
    def action_open_change_state_wizard(self):
      if self.state == 'closed':
        action=self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context']={'default_property_id':self.id}
        return action
      else :
          raise ValidationError('This property is not closed must be property closed')

        # method _compute_next_time add time on current time
    @api.depends('create_time')
    def _compute_next_time(self):
         for rec in self:
             if rec.create_time:
                 rec.next_time=rec.create_time+ timedelta(hours=6)
             else:
                 rec.next_time=False

                # method Samrt Buttons action_open_related_owner
    def action_open_related_owner(self):
            action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
            view_id=self.env.ref('app_one.owner_view_form').id
            action['res_id']=self.owner_id.id
            action['views']=[[view_id,'form']]
            return action
    #
    # #create
    # @api.model_create_multi
    # def create(self, vals):
    #     res=super(Property,self).create(vals)
    #     #logic
    #     print("inside create method")
    #     return res
    #
    # #Read
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res=super(Property, self)._search(domain, offset, limit, order, access_rights_uid)
    #
    #     #logic
    #     print("inside _search")
    #     return res
    #
    # #Update
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("inside write")
    #     return res
    #
    #
    # #Delete
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print("inside unlink")
    #     return res

    #integration with EndPoint GetAll properties
    def get_properties(self):
        payload=dict()
        try:
            response=requests.get('http://localhost:8069/v1/properties',data=payload)
            if response.status_code==200:
                # print(response.content)
                print(response.json())
            else:
                print("failed")
        except Exception as e:
            raise ValidationError(str(e))

    #method button property Excel Report
    def property_excel_report(self):
        return{
            'type':'ir.actions.act_url',
            'url':f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }


class PropertyLine(models.Model):
        _name='property.line'

        area=fields.Float()
        description=fields.Char()
        property_id=fields.Many2one('property')