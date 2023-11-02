from odoo import models, fields, api


class Matters(models.Model):
    _name = 'matter.model'
    _description = 'Meer and Hasan Matters'

    title = fields.Char(string="Matter Title")
    fir_number = fields.Char(string="FIR Number")
    order = fields.Char(string="Order Title")
    file_number = fields.Char(string="File Number")
    case_no = fields.Char(string="Case Number")
    institution_number = fields.Char(string='Institution Number')
    date = fields.Date(string='Date')
    description = fields.Text(string="Brief Description")
    further_article = fields.Text(string="Further Article")
    fir_year = fields.Selection(selection='_get_years', string='Year')
    assign_to_user_ids = fields.Many2many('res.users', 'matter_assign_to_user_rel', 'matter_id', 'user_id',
                                          string='Assign To User')
    reviewed_by_ids = fields.Many2many('res.users', 'matter_reviewed_by_rel', 'matter_id', 'user_id',
                                       string='Reviewed by')

    preceding_id = fields.One2many("precedings.model", 'matter_id')
    document_id = fields.One2many('document.model', 'matter_id', string='Documents')
    district_id = fields.Many2one('district.model', string="District")
    court_type_id = fields.Many2one('courttypes.model', string="Court Type")
    court_name_id = fields.Many2one('courtname.model', string="Court Name")
    case_category_id = fields.Many2one('casecategory.model', string="Case Category")
    police_station_id = fields.Many2one('policestation.model', string="Police Stations")
    case_status_id = fields.Many2one('casestatus.model', string="Matter Status")
    party_1_id = fields.Many2one('res.partner', string='Party No 01')
    party_2_id = fields.Many2one('res.partner', string='Party No 02')
    appeal_id = fields.Many2one('matter.model', string="Appeal Matter", help="Reference to the Appeal Matter")
    related_matter_id = fields.Many2one('matter.model', string="Related Matter", help="Reference to the Original Matter")
    order_id = fields.Many2one('sale.order', string='Sale Order', help='Reference to Sale Order')

    def _get_years(self):
        # Define the range of years you want
        start_year = 1900
        end_year = 2030

        # Generate a list of years
        years = [(str(year), str(year)) for year in range(start_year, end_year + 1)]

        return years

    def action_create_related_matter(self):
        current_matter = self

        new_matter = self.env['matter.model'].create({
            'party_1_id': current_matter.party_2_id.id if current_matter.party_2_id else False,
            'party_2_id': current_matter.party_1_id.id if current_matter.party_1_id else False,
            'appeal_id': current_matter.appeal_id.id if current_matter.appeal_id else False,
            'related_matter_id': current_matter.id,   # Set the matter_id field to link the original matter
            # Add other fields you want to copy and set for the new Matter
        })
        current_matter.write({'related_matter_id': new_matter.id})
        return {
            'name': "New Matter",
            'view_mode': 'form',
            'res_model': 'matter.model',
            'res_id': new_matter.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class Precedings(models.Model):
    _name = 'precedings.model'
    _description = 'Matter Precedings'

    title = fields.Char(string="Precedings")
    matter_id = fields.Many2one('matter.model', string='Matter')
    case_category_id = fields.Many2one('casecategory.model', string='Matter Category')
    case_stage_id = fields.Many2one('casestage.model', string="Matter Stage", create=False)
    proceedings_document_id = fields.One2many('proceeding_documents.model', 'precedings_id', string='Documents File')


class Documents(models.Model):
    _name = 'document.model'
    _description = 'Matters Document'

    title = fields.Char(string="Document Name")
    file = fields.Binary(string="File Attachment", attachment=True)
    matter_id = fields.Many2one('matter.model', string="Matter")


class Districts(models.Model):
    _name = 'district.model'
    _description = 'Pakistan Districts'

    name = fields.Char(string="District Name")
    courtTypeId = fields.One2many("courttypes.model", 'district_id', string="Court Type")
    courtNameId = fields.One2many("courtname.model", 'court_type_id', string="Court Name")
    caseCategoryId = fields.One2many("casecategory.model", 'court_type_id', string="Case Category")
    policeStationId = fields.One2many("policestation.model", 'district_id', string="Police Stations")
    order_id = fields.Many2one('sale.order', string='Sale Order', help='Reference to Sale Order')

class Courttypes(models.Model):
    _name = 'courttypes.model'
    _description = 'Basic Court Types'

    title = fields.Char(string="Court Type")
    district_id = fields.Many2one('district.model', string="District")
    courtNameId = fields.One2many("courtname.model", 'court_type_id', string="Court Name")
    caseCategoryId = fields.One2many("casecategory.model", 'court_type_id', string="Case Category")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result


class Courtname(models.Model):
    _name = "courtname.model"
    _description = "Name of Courts/Judges"

    title = fields.Char(string="Court/Judges Name")
    court_type_id = fields.Many2one('courttypes.model', string="Court Name")
    district_id = fields.Many2one('district.model', string="District")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result


class PoliceStation(models.Model):
    _name = "policestation.model"
    _description = "Police Station in Districts"

    name = fields.Char(string="Police Station Name")
    district_id = fields.Many2one('district.model', string="District")


class CaseStage(models.Model):
    _name = "casestage.model"
    _description = "Matter Stage"

    title = fields.Char(string="Matter Stage")
    preceeding_id = fields.One2many('precedings.model', 'case_stage_id', create=False)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result


class CaseStatus(models.Model):
    _name = "casestatus.model"
    _description = "Case Status"

    title = fields.Char(string="Case Status")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result


class CaseCategory(models.Model):
    _name = "casecategory.model"
    _description = "Category of Case"

    title = fields.Char(string="Case Category")
    court_type_id = fields.Many2one('courttypes.model', string="Case Category")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result


class ProceedingsDocuments(models.Model):
    _name = "proceeding_documents.model"
    _description = "Proceedings Documents"

    title = fields.Char(string="Document Title")
    date = fields.Date(string='Document Date')
    file = fields.Binary(string="Document File", attachment=True)
    precedings_id = fields.Many2one('precedings.model', string="Matter")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_related_district(self):
        matter_model = self.env['matter.model']
        new_matter = matter_model.create({
            'order_id': self.id,  # Link the new district to the order
            # Add other fields you want to set for the new District
            'title': "Testing Matter"
        })

        return new_matter

    @api.model
    def create(self, values):
        new_order = super(SaleOrder, self).create(values)

        # Create a new district linked to the sale order
        new_order._create_related_district()

        return new_order