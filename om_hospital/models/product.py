# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class Product(models.Model):
    _inherit = "product.template"

    # bom_counts = fields.Integer(compute="_compute_boms_count",)

    used_in_bom_parent_count = fields.Integer(compute="_compute_parent_bom_count")

    # def _compute_parent_bom_count(self):
    #     print("called\n\n")
    #     for product in self:
    #         new_bom_ids = []
    #         list_of_bom = []
    #         product_id = self.env["product.product"].search(
    #             [('product_tmpl_id', '=', product.id)])
    #         print('------------',product_id)
    #         # import pdb
    #         # pdb.set_trace()
    #         bom_ids = self.env['mrp.bom'].search(
    #             [('bom_line_ids.product_id', '=', product_id.id)])
    #         print('-------------------',bom_ids)
    #         for bom in bom_ids:
    #             list_of_bom.append(bom.id)
    #         for bom in bom_ids:
    #             new_bom_ids.append(self.prepare_bom(bom, list_of_bom))
    #         for bom_id_list in new_bom_ids:
    #             for bom_id in bom_id_list:
    #                 list_of_bom.append(bom_id)
    #         product.used_in_bom_parent_count = len(list(set(list_of_bom)))



    # def prepare_bom(self, bom, list_of_bom):
    #     if bom.product_tmpl_id.used_in_bom_parent_count == 0:
    #         return self.env['mrp.bom'].search([('product_tmpl_id', '=', bom.product_tmpl_id.id)]).ids
    #     else:
    #         product_id = self.env["product.product"].search(
    #             [('product_tmpl_id', '=', bom.product_tmpl_id.id)])
    #         new_bom_ids = self.env['mrp.bom'].search(
    #             [('bom_line_ids.product_id', '=', product_id.id)])
    #         for bom in new_bom_ids:
    #             list_of_bom.append(bom.id)
    #         for bom in new_bom_ids:
    #             return self.prepare_bom(bom, list_of_bom)



    # def action_used_in_parent_bom(self):
    #     new_bom_ids = []
    #     list_of_bom = []
    #     product_id = self.env["product.product"].search(
    #         [('product_tmpl_id', '=', self.id)])
    #     bom_ids = self.env['mrp.bom'].search(
    #         [('bom_line_ids.product_id', '=', product_id.id)])
    #     for bom in bom_ids:
    #         list_of_bom.append(bom.id)
    #     for bom in bom_ids:
    #         new_bom_ids.append(self.prepare_bom(bom, list_of_bom))
    #     for bom_id_list in new_bom_ids:
    #         for bom_id in bom_id_list:
    #             list_of_bom.append(bom_id)
    #     return {
    #         'name': _('Parent BOM'),
    #         'view_type': 'form',
    #         'view_mode': 'tree,form',
    #         'res_model': 'mrp.bom',
    #         'view_id': False,
    #         'type': 'ir.actions.act_window',
    #         'domain': [('id', 'in', list(set(list_of_bom)))],
    #     }




    # def _compute_boms_count(self):
    #     for product in self:
    #         # product.bom_counts = self.env['mrp.bom'].search_count([('product_tmpl_id', '=', product.id)])
    #         # import pdb
    #         # pdb.set_trace()
    #         # if self.bom_line_ids == 0:
    #         #     return product.bom_count
    #         # else:
    #         #     bom = product.bom_line_ids + product.bom_count
    #         #     return bom * _compute_boms_count(bom-1)
    #         new_bom_ids = []
    #         list_of_bom = []
    #         product_id = self.env["product.product"].search(
    #             [('product_tmpl_id', '=', product.id)])
    #         bom_ids = self.env['mrp.bom'].search(
    #             [('bom_line_ids.product_id', '=', product_id.id)])
    #         print('-----------',bom_ids)
