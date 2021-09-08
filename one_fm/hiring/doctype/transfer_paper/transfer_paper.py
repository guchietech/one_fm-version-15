
# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from one_fm.api.notification import create_notification_log
from frappe.model.document import Document
from frappe.utils import today, add_days, get_url
from one_fm.grd.doctype.work_permit import work_permit
from one_fm.api.notification import create_notification_log

class TransferPaper(Document):
    def validate(self):
        self.set_today_date()
        self.set_new_salary_from_job_offer()
        self.set_pam_designation()
        self.set_pam_file_number()
        self.set_electronic_signature()
        self.arrange_arabic_name()

        # self.set_pas_values()
        self.set_grd_values()
        # self.check_signed_workContract_employee_completed()
        # self.get_wp_status()
        
    def set_today_date(self):
        if not self.date_of_application:
            self.db_set('date_of_application',today())

    def set_new_salary_from_job_offer(self):
        """ This method is getting the basic amount of the salary structure in Job offer
            and setting it into the basic salary in Transfer Paper"""
        if not self.salary:
            salary = frappe.db.get_value('Job Offer', {'job_applicant':self.applicant},['one_fm_salary_structure'])
            components = frappe.get_doc('Salary Structure',salary)
            print(components.earnings)
            for component in components.earnings:
                if component.salary_component == "Basic":
                    self.db_set('salary', component.amount) 

    def set_pam_designation(self):
        if not self.pam_designation:
            doc = frappe.get_doc('Job Applicant',self.applicant)
            if doc.pam_designation_button == 1 and doc.one_fm_pam_designation != None:
                self.db_set('pam_designation',doc.one_fm_pam_designation)
            elif doc.pam_designation_button == 0 and doc.one_fm_erf_pam_designation != None:
                self.db_set('pam_designation',doc.one_fm_erf_pam_designation)
    
    def set_pam_file_number(self):
        """This method is to get the pam file number and
         check if its contract or private and set it in the right field"""
        if not self.pam_file_number:
            doc = frappe.get_doc('Job Applicant',self.applicant)
            if doc.pam_number_button == 1 and doc.one_fm_file_number != None: #pam number get changed in job applicant
                govermental,main_file = frappe.db.get_value('PAM File',{'pam_file_number':doc.one_fm_file_number},['government_project','file_number'])
                if govermental == 0:#the file not govermental 
                    self.db_set('pam_file_number',doc.one_fm_file_number)
                if govermental == 1:
                    self.db_set('contract_file_number',doc.one_fm_file_number)
                    self.db_set('pam_file_number',main_file)
            
            elif doc.pam_number_button == 0 and doc.one_fm_erf_pam_file_number != None: #pam number is the one set in erf
                govermental,main_file = frappe.db.get_value('PAM File',{'pam_file_number':doc.one_fm_erf_pam_file_number},['government_project','file_number'])
                print(govermental,main_file)
                if govermental == 0:#the file not govermental 
                    self.db_set('pam_file_number',doc.one_fm_erf_pam_file_number)
                if govermental == 1:
                    self.db_set('contract_file_number',doc.one_fm_erf_pam_file_number)
                    self.db_set('pam_file_number',main_file)
        
    def set_grd_values(self):
        if not self.grd_operator:
            self.grd_operator = frappe.db.get_single_value("GRD Settings", "default_grd_operator_transfer")

    def set_electronic_signature(self):
        if not self.authorized_signature:
            doc = frappe.get_doc('Job Applicant',self.applicant) 
            if doc.one_fm_signatory_name and doc.one_fm_pam_authorized_signatory:
                authorized_list = frappe.get_doc('PAM Authorized Signatory List',doc.one_fm_pam_authorized_signatory)
                for authorized in authorized_list.authorized_signatory:
                    if doc.one_fm_signatory_name == authorized.authorized_signatory_name_arabic:
                        self.db_set('authorized_signature', authorized.signature)
                # print("-->",self.authorized_signature)

    def arrange_arabic_name(self):
        """This method arranges the names in the print format based on what is filled in job applicant doctype"""
        applicant_full_arabic_name=[]
        if self.applicant:
            # applicant_full_arabic_name = [{'First Name in Arabic':'first_name'},{'Second Name in Arabic':'second_name'},
            #     {'Third Name in Arabic':'third_name'},{'Last Name in Arabic':'last_name'}]
            applicant = frappe.get_doc('Job Applicant',self.applicant)
            if applicant.one_fm_first_name_in_arabic and not applicant.one_fm_second_name_in_arabic and not applicant.one_fm_third_name_in_arabic and not applicant.one_fm_forth_name_in_arabic and applicant.one_fm_last_name_in_arabic:
                self.first_name_in_arabic = applicant.one_fm_first_name_in_arabic
                self.second_name_in_arabic = applicant.one_fm_last_name_in_arabic
                self.third_name_in_arabic = ''
                self.forth_name_in_arabic = ''
                self.last_name_in_arabic = ''
            elif applicant.one_fm_first_name_in_arabic and applicant.one_fm_second_name_in_arabic and not applicant.one_fm_third_name_in_arabic and not applicant.one_fm_forth_name_in_arabic and applicant.one_fm_last_name_in_arabic:
                self.first_name_in_arabic = applicant.one_fm_first_name_in_arabic
                self.second_name_in_arabic = applicant.one_fm_second_name_in_arabic
                self.third_name_in_arabic = applicant.one_fm_last_name_in_arabic
                self.forth_name_in_arabic = ''
                self.last_name_in_arabic = ''
            elif applicant.one_fm_first_name_in_arabic and applicant.one_fm_second_name_in_arabic and applicant.one_fm_third_name_in_arabic and not applicant.one_fm_forth_name_in_arabic and applicant.one_fm_last_name_in_arabic:
                self.first_name_in_arabic = applicant.one_fm_first_name_in_arabic
                self.second_name_in_arabic = applicant.one_fm_second_name_in_arabic
                self.third_name_in_arabic = applicant.one_fm_third_name_in_arabic
                self.forth_name_in_arabic = applicant.one_fm_last_name_in_arabic
                self.last_name_in_arabic = ''
            elif applicant.one_fm_first_name_in_arabic and applicant.one_fm_second_name_in_arabic and not applicant.one_fm_third_name_in_arabic and applicant.one_fm_forth_name_in_arabic and applicant.one_fm_last_name_in_arabic:
                self.first_name_in_arabic = applicant.one_fm_first_name_in_arabic
                self.second_name_in_arabic = applicant.one_fm_second_name_in_arabic
                self.third_name_in_arabic = applicant.one_fm_forth_name_in_arabic
                self.forth_name_in_arabic = applicant.one_fm_last_name_in_arabic
                self.last_name_in_arabic = ''
            
    def set_pas_values(self):
        doc = frappe.get_doc('Job Applicant',self.applicant)
        if doc.one_fm_pam_file_number:
            company_data = frappe.get_doc('PAM File',doc.one_fm_pam_file_number)
            self.db_set('company_trade_name_arabic', company_data.license_trade_name_arabic)
            self.db_set('license_number', company_data.license_number)#licence to issuer_number
            self.db_set('pam_file_number', company_data.pam_file_number)

    def get_wp_status(self):
        """
        This method is getting the last wp record create by this TP and checking its status.
        TP status will be completed if the wp record is completed. 
        """
        if self.tp_status != "Completed" and self.work_permit_ref:
            wp = frappe.get_doc('Work Permit',self.work_permit_ref)
            self.db_set('work_permit_status', wp.work_permit_status)
            if wp.work_permit_status == "Completed":
                self.db_set('tp_status', "Completed")

    def check_signed_workContract_employee_completed(self):
        """"
        This method create wp record after tp is submitted and notify operator 
        """
        if self.signed == "Yes" and self.tp_status == "Pending By GRD":
            if frappe.db.exists("Employee", {"one_fm_civil_id":self.civil_id}):#employee is created 
                employee = frappe.db.get_value("Employee", {"one_fm_civil_id":self.civil_id})
                if employee:
                    self.recall_create_transfer_work_permit(employee)#create wp for local transfer
                    self.notify_grd_transfer_wp_record()
            else:
                frappe.throw("No Employee record created yet...")

    def recall_create_transfer_work_permit(self,employee):
        name = work_permit.create_work_permit_transfer(self.name,employee)
        self.work_permit_ref = name

    def notify_grd_transfer_wp_record(self):
        # Getting the wp record the one not rejected and linked to the TP
        wp = frappe.db.get_value("Work Permit",{'transfer_paper':self.name,'work_permit_status':'Draft'})
        if wp:
            wp_record = frappe.get_doc('Work Permit', wp)
            page_link = get_url("/desk#Form/Work Permit/" + wp_record.name)
            subject = ("Apply for Transfer Work Permit Online")
            message = "<p>Please Apply for Transfer WP Online for <a href='{0}'></a>.</p>".format(page_link, wp_record.employee)
            create_notification_log(subject, message, [self.grd_operator], wp_record)
            
    

@frappe.whitelist()
def resend_new_wp_record(doc_name):
    doc = frappe.get_doc('Transfer Paper',doc_name)
    if doc.work_permit_ref:
        wp = frappe.get_doc("Work Permit",doc.work_permit_ref)
        print("==>new",wp.name)
    if wp:
        wp.db_set('work_permit_status', "Closed")
        doc.check_signed_workContract_employee_completed()
        doc.db_set('tp_status', "Pending By GRD")
        
    

    

    

