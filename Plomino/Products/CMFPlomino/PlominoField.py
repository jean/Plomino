# -*- coding: utf-8 -*-
#
# File: PlominoField.py
#
# Copyright (c) 2008 by ['Eric BREHAULT']
# Generator: ArchGenXML Version 2.0
#            http://plone.org/products/archgenxml
#
# Zope Public License (ZPL)
#

__author__ = """Eric BREHAULT and Caroline ANSALDI <eric.brehault@makina-corpus.org>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFPlomino import fields

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.CMFPlomino.config import *

##code-section module-header #fill in your manual code here
from Products.CMFPlomino.PlominoUtils import StringToDate
from fields.selection import ISelectionField
from fields.text import ITextField
from fields.datetime import IDatetimeField
from fields.name import INameField
from fields.doclink import IDoclinkField
from ZPublisher.HTTPRequest import FileUpload

##/code-section module-header

schema = Schema((

    StringField(
        name='id',
        widget=StringField._properties['widget'](
            label="Id",
            description="The field id",
            label_msgid='CMFPlomino_label_field_id',
            description_msgid='CMFPlomino_help_field_id',
            i18n_domain='CMFPlomino',
        ),
    ),
    StringField(
        name='FieldType',
        default="TEXT",
        widget=SelectionWidget(
            label="Field type",
            description="The kind of this field",
            label_msgid='CMFPlomino_label_FieldType',
            description_msgid='CMFPlomino_help_FieldType',
            i18n_domain='CMFPlomino',
        ),
        vocabulary=[[f, FIELD_TYPES[f][0]] for f in FIELD_TYPES.keys()],
    ),
    StringField(
        name='FieldMode',
        default="EDITABLE",
        widget=SelectionWidget(
            label="Field mode",
            description="How content will be generated",
            label_msgid='CMFPlomino_label_FieldMode',
            description_msgid='CMFPlomino_help_FieldMode',
            i18n_domain='CMFPlomino',
        ),
        vocabulary= FIELD_MODES,
    ),
    TextField(
        name='Formula',
        widget=TextAreaWidget(
            label="Formula",
            description="How to calculate field content",
            label_msgid='CMFPlomino_label_FieldFormula',
            description_msgid='CMFPlomino_help_FieldFormula',
            i18n_domain='CMFPlomino',
        ),
    ),
    StringField(
        name='FieldReadTemplate',
        widget=StringField._properties['widget'](
            label="Field read template",
            description="Custom rendering template in read mode",
            label_msgid='CMFPlomino_label_FieldReadTemplate',
            description_msgid='CMFPlomino_help_FieldReadTemplate',
            i18n_domain='CMFPlomino',
        ),
    ),
    StringField(
        name='FieldEditTemplate',
        widget=StringField._properties['widget'](
            label="Field edit template",
            description="Custom rendering template in edit mode",
            label_msgid='CMFPlomino_label_FieldEditTemplate',
            description_msgid='CMFPlomino_help_FieldEditTemplate',
            i18n_domain='CMFPlomino',
        ),
    ),

    BooleanField(
        name='Mandatory',
        default="0",
        widget=BooleanField._properties['widget'](
            label="Mandatory",
            description="Is this field mandatory? (empty value will not be allowed)",
            label_msgid='CMFPlomino_label_FieldMandatory',
            description_msgid='CMFPlomino_help_FieldMandatory',
            i18n_domain='CMFPlomino',
        ),
    ),
    TextField(
        name='ValidationFormula',
        widget=TextAreaWidget(
            label="Validation formula",
            description="Evaluate the input validation",
            label_msgid='CMFPlomino_label_FieldValidation',
            description_msgid='CMFPlomino_help_FieldValidation',
            i18n_domain='CMFPlomino',
        ),
    ),
    BooleanField(
        name='ToBeIndexed',
        default="0",
        widget=BooleanField._properties['widget'](
            label="Add to index",
            description="The field will be searchable",
            label_msgid='CMFPlomino_label_FieldIndex',
            description_msgid='CMFPlomino_help_FieldIndex',
            i18n_domain='CMFPlomino',
        ),
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PlominoField_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PlominoField(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IPlominoField)

    meta_type = 'PlominoField'
    _at_rename_after_creation = True

    schema = PlominoField_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('validateFormat')
    def validateFormat(self, submittedValue):
        """check if submitted value match the field expected format
        """
        adapt = self.getSettings()
        return adapt.validate(submittedValue)

    security.declarePublic('processInput')
    def processInput(self, submittedValue, doc, process_attachments):
        """process submitted value according the field type
        """
        fieldtype = self.getFieldType()
        fieldName = self.id
        adapt = self.getSettings()
        if fieldtype=="ATTACHMENT" and process_attachments:
            if isinstance(submittedValue, FileUpload):
                current_files=doc.getItem(fieldName)
                if current_files=='':
                    current_files={}
                (new_file, contenttype) = doc.setfile(submittedValue)
                if new_file is not None:
                    current_files[new_file]=contenttype
                v=current_files
        else:
            v = adapt.processInput(submittedValue)
        return v

    security.declareProtected(READ_PERMISSION, 'getFieldRender')
    def getFieldRender(self, form, doc, editmode, creation=False, request=None):
        """Rendering the field
        """
        mode = self.getFieldMode()
        fieldName = self.id
        if doc is None:
            target = form
        else:
            target = doc

        # compute the value
        if mode=="EDITABLE":
            if doc is None:
                if creation and not self.Formula()=="":
                    try:
                        fieldValue = self.runFormulaScript("field_"+form.id+"_"+fieldName+"_formula", target, self.Formula)
                    except Exception:
                        fieldValue = ""
                elif request is None:
                    fieldValue = ""
                else:
                    fieldValue = request.get(fieldName, '')
                    if self.getFieldType()=="DATETIME" and not (fieldValue=='' or fieldValue is None):
                        fieldValue = StringToDate(fieldValue, form.getParentDatabase().getDateTimeFormat())
            else:
                fieldValue = doc.getItem(fieldName)

        if mode=="DISPLAY" or mode=="COMPUTED":
            try:
                fieldValue = self.runFormulaScript("field_"+form.id+"_"+fieldName+"_formula", target, self.Formula)
            except Exception:
                fieldValue = ""

        if mode=="CREATION":
            if creation:
                # Note: on creation, there is no doc, we use self as param
                # in formula
                try:
                    fieldValue = self.runFormulaScript("field_"+form.id+"_"+fieldName+"_formula", form, self.Formula)
                except Exception:
                    fieldValue = ""
            else:
                fieldValue = doc.getItem(fieldName)

        # get the rendering template
        pt=None
        if mode=="EDITABLE" and editmode:
            templatemode="Edit"
            # if custom template, use it
            if not self.getFieldEditTemplate()=="":
                pt=getattr(self.resources, self.getFieldEditTemplate()).__of__(self)
        else:
            templatemode="Read"
            # if custom template, use it
            if not self.getFieldReadTemplate()=="":
                pt=getattr(self.resources, self.getFieldReadTemplate()).__of__(self)
        
        # if no custom template provided, get the template associated to the field type 
        if pt is None:
            fieldType = self.FieldType
            pt=self.getRenderingTemplate(fieldType+"Field"+templatemode)
            if pt is None:
                pt=self.getRenderingTemplate("DefaultField"+templatemode)
        
        if self.getFieldType()=="SELECTION":
            selectionlist = ISelectionField(self).getSelectionList(target)
        elif self.getFieldType()=="NAME" and mode=="EDITABLE" and editmode:
            selectionlist = INameField(self).getNamesList()
        elif self.getFieldType()=="DOCLINK":
            selectionlist = IDoclinkField(self).getDocumentsList(target)
        else:
            selectionlist = None
            
        try:
            return pt(fieldname=fieldName,
                fieldvalue=fieldValue,
                selection=selectionlist,
                field=self
                )
        except Exception, e:
            self.traceRenderingErr(e, self)
            return ""
        
    security.declarePublic('getParentDatabase')
    def getParentDatabase(self):
        """Get the database containing this field
        """
        return self.getParentNode().getParentDatabase()
    
    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """post edit
        """
        self.cleanFormulaScripts("field_"+self.getParentNode().id+"_"+self.id)
        db = self.getParentDatabase()
        if self.getToBeIndexed() :
            db.getIndex().createFieldIndex(self.id, self.getFieldType())

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """post create
        """
        db = self.getParentDatabase()
        if self.getToBeIndexed():
            db.getIndex().createFieldIndex(self.id, self.getFieldType())

    security.declarePublic('getSettings')
    def getSettings(self, key=None):
        """
        """
        if hasattr(fields, self.FieldType.lower()):
            fieldinterface = getattr(getattr(fields, self.FieldType.lower()), "I"+self.FieldType.capitalize()+"Field")
        else:
            fieldinterface = getattr(getattr(fields, "base"), "IBaseField")
        if key is None:
            return fieldinterface(self)
        else:
            return getattr(fieldinterface(self), key, None)
                                           
registerType(PlominoField, PROJECTNAME)
# end of class PlominoField

##code-section module-footer #fill in your manual code here
##/code-section module-footer


