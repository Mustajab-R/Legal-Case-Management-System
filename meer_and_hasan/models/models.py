from odoo import api, fields, models


class Matters(models.Model):
    _name = 'matter.model'
    _description = 'Meer and Hasan Matters'

    title = fields.Char(string="Matter Title")
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('complete', 'Çomplete')
    ])
    fir_number = fields.Char(string="FIR Number")
    fir_year = fields.Char(string="FIR Year")

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


class Precedings(models.Model):
    _name = 'precedings.model'
    _description = 'Matter Precedings'

    title = fields.Char(string="Precedings")
    matter_id = fields.Many2one('matter.model', string='Matter')
    case_category_id = fields.Many2one('casecategory.model', string='Matter Category')
    case_stage_id = fields.Many2one('casestage.model', string="Matter Stage")
    matter_stage = fields.Selection(related='matter_id.stage', string="Matter Stage", readonly=False)


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
    preceeding_id = fields.One2many('precedings.model', 'case_stage_id', string="Preceedings")

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, record.title))
        return result
class CaseStatus(models.Model):
    _name = "casestatus.model"
    _description = "Case Status"

    title = fields.Char(string="Case Status")


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
