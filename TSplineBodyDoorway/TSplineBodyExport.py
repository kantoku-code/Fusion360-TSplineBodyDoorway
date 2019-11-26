#FusionAPI_python TSplineBodyExport Ver0.0.2
#Author-kantoku
#Description-export Tsm files

import adsk.core, adsk.fusion, traceback
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
import os

class TSplineBodyExport(Fusion360CommandBase):

    _tBodies = None
    _check_id_header: str = 'check'
    _lMsg = None

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = None
        try:
            iptChecks = [c for c in inputs if c.id[0:5] == self._check_id_header]
            onChecks = [int(c.id[5:]) for c in iptChecks if c.value]
            if len(onChecks) < 1: return

            ao = AppObjects()
            path :str  = self.select_Folder(ao.ui)
            if len(path) < 1: return
            path = path.replace('/','\\')

            tbs = self._tBodies.getBodies(onChecks)
            errLst :list() = []
            for tb in tbs:
                expPath = self.getExpPath(os.path.join(path,tb.filename))
                try:
                    if not tb.saveAsTSMFile(expPath):
                        errLst.append(tb.filename)
                except:
                    errLst.append(tb.filename)

            msg = 'Done '
            if len(errLst) > 0:
                msg += '\n-- export errer --\n' + '\n'.join(errLst)
                
            ao.ui.messageBox(msg)
        except:
            if ao.ui:
                ao.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
                
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        self._lMsg = LangMsg()

        self._tBodies = self.getTSplineBodyList()
        if self._tBodies is None: return

        ao = AppObjects()

        #Table
        tbl = inputs.addTableCommandInput('table', 'Table', 0, '1:10:3:3')
        tbl.hasGrid = False
        tbl.maximumVisibleRows = 20
        
        for idx, tb in enumerate(self._tBodies.getBodies()):
            tbl.addCommandInput(
                inputs.addBoolValueInput(
                    self._check_id_header + '{}'.format(idx), 
                    'Checkbox', 
                    True, 
                    '', 
                    False),
                idx, 0)

            tbl.addCommandInput(
                inputs.addTextBoxCommandInput(
                    'info1{}'.format(idx), 
                    'tbodyinfo1',
                    tb.info1, 
                    1, 
                    True),
                idx, 1)

            tbl.addCommandInput(
                inputs.addTextBoxCommandInput(
                    'info2{}'.format(idx), 
                    'tbodyinfo2',
                    tb.info2, 
                    1, 
                    True),
                idx, 2)

            tbl.addCommandInput(
                inputs.addTextBoxCommandInput(
                    'info3{}'.format(idx), 
                    'tbodyinfo3',
                    tb.info3, 
                    1, 
                    True),
                idx, 3)
        
        #Dialog
        inputs.command.setDialogInitialSize(500,800)

# -- Support functions --
    def getTSplineBodyList(self):

        ao = AppObjects()
        forms = [comp.features.formFeatures for comp in ao.design.allComponents]
        fmLst = []
        for fs in forms:
            for f in fs:
                fmLst.append(f)

        tbLst = []
        for tbs in [f.tSplineBodies for f in fmLst]:
            for tb in tbs:
                tbLst.append(tb)

        if len(tbLst) < 1:
            msg = self._lMsg.msg('err_nonform')
            ao.ui.messageBox(msg)
            return None

        return TBodyContainer(tbLst)

    def select_Folder(self, ui: adsk.core.UserInterface) -> str:
        dlg = ui.createFolderDialog()
        dlg.title = self._lMsg.msg('dlg_title')
        if dlg.showDialog() != adsk.core.DialogResults.DialogOK :
            return ''
        return dlg.folder

    def getExpPath(self, path :str) -> str:
        if not os.path.exists(path):
            return path

        root, ext = os.path.splitext(path)
        num = 0
        for idx in range(1000):
            num += 1
            tmpPath = root + '_' + str(num) + ext
            if not os.path.exists(tmpPath):
                return tmpPath
        return path

# -- Support class --
class TBodyContainer(object):
    def __init__(self, lst :list()):
        if len(lst) < 1: return

        super().__init__()
        self.tBodies = lst
        for tb in self.tBodies:
            fFeat: adsk.fusion.FormFeature = tb.parentFormFeature
            comp : adsk.fusion.Component = fFeat.parentComponent
            # tb.info1 = '{0:<30}'.format(tb.name)
            # tb.info2 = ':{0:<15}: {1:<15}'.format(fFeat.name,comp.name)
            tb.info1 = '{0:<30}'.format(tb.name)
            tb.info2 = ':{0:<30}'.format(fFeat.name)
            tb.info3 = ':{0:<30}'.format(comp.name)

            tb.filename = r'{}_{}_{}.tsm'.format(tb.name,fFeat.name,comp.name)

    def getBodies(self, idxs = []) -> list():
        if len(idxs) < 1:
            return self.tBodies
        else:
            lst = []
            for i in idxs:
                lst.append(self.tBodies[i])
            return lst

class LangMsg(Fusion360CommandBase):
    _lang = -1
    _msgDict = None

    def __init__(self):
        ao = AppObjects()
        lang = ao.app.preferences.generalPreferences.userLanguage
    
        langs = adsk.core.UserLanguages
        if lang == langs.JapaneseLanguage:
            self._lang = 0
        else:
            self._lang = 1
        
        self.__setDict__()
    
    def __setDict__(self):
        self._msgDict = {
            'dlg_title': ('エクスポートフォルダ選択', 'select export folder'),
            'err_nonform': ('エクスポートするTスプラインボディがありません!', 'There are no TSplineBody to export!')
        }

    def msg(self, key :str) -> str:
        if key not in self._msgDict:
            return 'msg err'
        
        return self._msgDict[key][self._lang]