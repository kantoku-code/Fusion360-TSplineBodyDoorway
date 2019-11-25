#FusionAPI_python TSplineBodyDoorway Ver0.0.1
#Author-kantoku
#Description-import Tsm files

#using Fusion360AddinSkeleton
#https://github.com/tapnair/Fusion360AddinSkeleton
#Special thanks:Patrick Rainsberry

from .TSplineBodyImport import TSplineBodyImport
from .TSplineBodyExport import TSplineBodyExport

commands = []
command_definitions = []

# Import
cmd = {
    'cmd_name': 'TSpline Body Import',
    'cmd_description': 'Import Tsm file (T-spline body)',
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
    'cmd_description': 'Export Form (T-spline body)',
    'cmd_id': 'tBodyExport',
    'cmd_resources': './resources/export',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'UtilityPanel',
    'class': TSplineBodyExport
}
command_definitions.append(cmd)

# Set to True to display various useful messages when debugging your app
debug = False
# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
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