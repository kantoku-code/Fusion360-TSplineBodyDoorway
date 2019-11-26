#FusionAPI_python TSplineBodyImport Ver0.0.2
#Author-kantoku
#Description-import Tsm files

import adsk.core, adsk.fusion, traceback
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
import os

class TSplineBodyImport(Fusion360CommandBase):

    _lMsg = None

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = None
        try:
            ao = AppObjects()

            files: list()  = self.select_File(ao.ui)
            if len(files) < 1: return
            
            forms = ao.root_comp.features.formFeatures
            fFeat :adsk.fusion.FormFeature = forms.add()
            tBodies :adsk.fusion.TSplineBodies = fFeat.tSplineBodies

            fFeat.startEdit()

            errLst :list() = []
            for path in files:
                tmpPath :str = self.getTempPath(path)
                os.rename(path,tmpPath)
                try:
                    tb :adsk.fusion.TSplineBody = tBodies.addByTSMFile(tmpPath)
                    basename = os.path.basename(path)
                    base, ext = os.path.splitext(basename)
                    tb.name = os.path.basename(base)
                    # tb.name = os.path.basename(path)
                except:
                    errLst.append(path)
                finally:
                    os.rename(tmpPath, path)

            fFeat.finishEdit()
            
            msg = 'Done ({})'.format(fFeat.name)
            if len(errLst) > 0:
                msg += '\n-- import errer --\n' + '\n'.join(errLst)
                
            ao.ui.messageBox(msg)
        except:
            if ao.ui:
                ao.ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        self._lMsg = LangMsg()

    # -- Support functions --
    def select_File(self, ui: adsk.core.UserInterface) -> list():
        dlg = ui.createFileDialog()
        dlg.title = self._lMsg.msg('dlg_title')
        dlg.filter = self._lMsg.msg('dlg_filter')

        dlg.isMultiSelectEnabled = True
        if dlg.showOpen() != adsk.core.DialogResults.DialogOK :
            return []

        return dlg.filenames

    def getTempPath(self, path :str) -> str:
        folder = os.path.dirname(path)
        num = 0
        for idx in range(1000):
            num += 1
            tmpPath = os.path.join(folder, str(num) + '.tsm')
            if not os.path.exists(os.path.join(folder, tmpPath)):
                return tmpPath

        return path

# -- Support class --
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
            'dlg_title': ('インポートファイル選択', 'select import files'),
            'dlg_filter': ('Tsmファイル(*.tsm)', 'Tsm File(*.tsm)s')
        }

    def msg(self, key :str) -> str:
        if key not in self._msgDict:
            return 'msg err'
        
        return self._msgDict[key][self._lang]
