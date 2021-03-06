#FusionAPI_python TSplineBodyDoorway
#Author-kantoku
#Description-import Tsm files

#using Fusion360AddinSkeleton
#https://github.com/tapnair/Fusion360AddinSkeleton
#Special thanks:Patrick Rainsberry

import adsk.core
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase
from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .TSplineBodyImport import TSplineBodyImport
from .TSplineBodyExport import TSplineBodyExport

commands = []
command_definitions = []

# Set to True to display various useful messages when debugging your app
debug = False

def run(context):
    lMsg = LangMsg()

    # Import
    cmd = {
        'cmd_name': 'TSpline Body Import',
        'cmd_description': lMsg.msg('import_cmd_description'),
        'cmd_id': 'tBodyImport',
        'cmd_resources': './resources/import',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'UtilityPanel',
        'class': TSplineBodyImport
    }
    command_definitions.append(cmd)

    # Export
    cmd = {
        'cmd_name': 'TSpline Body Export',
        'cmd_description': lMsg.msg('export_cmd_description'),
        'cmd_id': 'tBodyExport',
        'cmd_resources': './resources/export',
        'workspace': 'FusionSolidEnvironment',
        'toolbar_panel_id': 'UtilityPanel',
        'class': TSplineBodyExport
    }
    command_definitions.append(cmd)

    # Don't change anything below here:
    for cmd_def in command_definitions:
        command = cmd_def['class'](cmd_def, debug)
        commands.append(command)


        for run_command in commands:
            run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()

# -- Support class --
class LangMsg(Fusion360CommandBase):
    _lang = -1
    _msgDict = None

    def __init__(self):
        app = adsk.core.Application.get()
        lang = app.preferences.generalPreferences.userLanguage
    
        langs = adsk.core.UserLanguages
        if lang == langs.JapaneseLanguage:
            self._lang = 0
        else:
            self._lang = 1
        
        self.__setDict__()
    
    def __setDict__(self):
        self._msgDict = {
            'import_cmd_description': (
                'Tsmファイル(Tスプラインボディ)をインポートします',
                'Import Tsm file (T-spline body)'),
            'export_cmd_description': (
                'フォーム(Tスプラインボディ)をエクスポートします',
                'Export Form (T-spline body)')
        }

    def msg(self, key :str) -> str:
        if key not in self._msgDict:
            return 'msg err'
        
        return self._msgDict[key][self._lang]